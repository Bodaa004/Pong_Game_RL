import pygame
import random

pygame.init()

# Window dimensions
WIDTH, HEIGHT = 640, 480
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10
PADDLE_SPEED = 10
BALL_SPEED = 5

# Colors
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

# Font for displaying scores and rewards
font = pygame.font.SysFont(None, 36)

# Class to represent a Paddle
class Paddle:
    def __init__(self, x, y):
        self.x = x  
        self.y = y  

    def move_up(self):
        # Move paddle upwards
        self.y -= PADDLE_SPEED
        self.y = max(0, self.y)

    def move_down(self):
        # Move paddle downwards
        self.y += PADDLE_SPEED
        self.y = min(HEIGHT - PADDLE_HEIGHT, self.y)

    def draw(self, surface,color):
        # Draw the paddle on the screen
        pygame.draw.rect(surface, color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Class to represent the Ball
class Ball:
    def __init__(self, x, y):
        self.x = x  
        self.y = y  

# Class to represent the Pong game
class PongGame:
    def __init__(self, ai_mode=True):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))  
        pygame.display.set_caption("Pong - Player vs AI") 
        self.clock = pygame.time.Clock()  # Clock to control frame rate
        self.ai_mode = ai_mode  # Flag to indicate if AI mode is enabled
        self.player_score = 0  # Player's score
        self.enemy_score = 0  # Enemy (AI or second player) score
        self.total_reward = 0  # Total reward in the game
        self.learning_mode = True  # Start in learning mode
        self.button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 50, 120, 40)  # Toggle button for switching modes

        self.reset() 

    def reset(self):
        # Reset the game state to start a new game
        self.paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2) 
        self.enemy_paddle = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2) 
        self.ball = Ball(WIDTH // 2, HEIGHT // 2) 
        self.ball_vel = [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])] 
        self.hits = 0  
        self.frame_iteration = 0  

    def play_step(self, action):
        # Main game loop for each step
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.learning_mode = not self.learning_mode
                    mode = "Training" if self.learning_mode else "Play"
                    print(f"Mode switched to: {mode}")
        
        # Left paddle: Player control
        if not self.learning_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.paddle.move_up()
            elif keys[pygame.K_DOWN]:
                self.paddle.move_down()
        else:
            if action[1]:
                self.paddle.move_up()
            elif action[2]:
                self.paddle.move_down()

        # Right paddle: AI control
        if self.ball.y < self.enemy_paddle.y + PADDLE_HEIGHT // 2:
            self.enemy_paddle.move_up() 
        elif self.ball.y > self.enemy_paddle.y + PADDLE_HEIGHT // 2:
            self.enemy_paddle.move_down()
            
        # Ball movement
        self.ball.x += self.ball_vel[0] 
        self.ball.y += self.ball_vel[1]  

        # Bounce off top/bottom of screen
        if self.ball.y <= 0 or self.ball.y >= HEIGHT - BALL_SIZE:
            self.ball_vel[1] *= -1  # Reverse ball's Y velocity

        reward = 0  # Initialize reward
        game_over = False  # Flag to check if game is over

        # Reward for keeping the ball in play
        if 0 < self.ball.x < WIDTH:
            reward += 0.05  

        # Collision with player paddle = HIT!
        if (self.paddle.x < self.ball.x + BALL_SIZE and
            self.paddle.x + PADDLE_WIDTH > self.ball.x and
            self.paddle.y < self.ball.y + BALL_SIZE and
            self.paddle.y + PADDLE_HEIGHT > self.ball.y):
            self.ball_vel[0] *= -1  
            reward += 1.0  
            self.total_reward += reward  
            self.hits += 1 

        # Collision with enemy paddle (no reward)
        if (self.enemy_paddle.x < self.ball.x + BALL_SIZE and
            self.enemy_paddle.x + PADDLE_WIDTH > self.ball.x and
            self.enemy_paddle.y < self.ball.y + BALL_SIZE and
            self.enemy_paddle.y + PADDLE_HEIGHT > self.ball.y):
            self.ball_vel[0] *= -1  

        # Penalty for poor paddle alignment
        if abs(self.paddle.y + PADDLE_HEIGHT // 2 - self.ball.y) > 50:
            reward -= 0.1  

        # Predictive reward: if paddle is aligned well as ball approaches
        if self.ball.x < WIDTH // 3 and abs(self.paddle.y + PADDLE_HEIGHT // 2 - self.ball.y) < 20:
            reward += 0.2  

        # Left wall: player missed
        if self.ball.x <= 0:
            self.enemy_score += 1  
            reward = -10  
            self.total_reward = reward  
            game_over = True  
            return reward, game_over, self.player_score, self.hits

        # Right wall: AI missed
        if self.ball.x >= WIDTH:
            self.player_score += 1  
            reward = 10  
            self.total_reward += reward  
            game_over = True 
            return reward, game_over, self.player_score, self.hits

        self.total_reward += reward  
        self.update_ui()  
        self.clock.tick(60)  
        return reward, game_over, self.player_score, self.hits

    def update_ui(self):
        # Update the game window with current game state
        self.display.fill(BLACK)  
        self.paddle.draw(self.display,WHITE)  
        self.enemy_paddle.draw(self.display,CYAN)  
        pygame.draw.rect(self.display, WHITE, (self.ball.x, self.ball.y, BALL_SIZE, BALL_SIZE))  

        # Draw the scores and total reward on screen
        player_text = font.render(f"Player: {self.player_score}", True, WHITE)
        enemy_text = font.render(f"{'AI' if self.ai_mode else 'Player 2'}: {self.enemy_score}", True, WHITE)
        reward_text = font.render(f"Total Reward: {self.total_reward:+0.3f}", True, WHITE)

        # Display the score and reward texts at the top of the screen
        self.display.blit(player_text, (20, 10))
        self.display.blit(enemy_text, (WIDTH - 200, 10))
        self.display.blit(reward_text, (WIDTH // 2 - 150, 10))
        
        # Draw the mode toggle button (Training/Play)
        pygame.draw.rect(self.display, WHITE, self.button_rect, 2)  
        mode_text = font.render("Training" if self.learning_mode else "Play", True, WHITE)
        text_rect = mode_text.get_rect(center=self.button_rect.center)  
        self.display.blit(mode_text, text_rect)  

        pygame.display.flip()  
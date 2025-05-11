import pygame
import random
import torch
import numpy as np
from collections import deque
from pong import PongGame, PADDLE_WIDTH, PADDLE_HEIGHT
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, ai_mode=True):
        # Initialize the agent, with hyperparameters for training and model setup        
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(6, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # Extract the current game state (ball position, paddle position, ball velocity)
    def get_state(self, game):
        state = [
            game.ball.x < game.paddle.x,
            game.ball.x > game.paddle.x + PADDLE_WIDTH,
            game.ball.y < game.paddle.y,
            game.ball.y > game.paddle.y + PADDLE_HEIGHT,
            game.ball_vel[0] < 0,
            game.ball_vel[1] < 0,
        ]
        return np.array(state, dtype=int)

    # Store the agent's experience in memory
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # Train the model on a batch of experiences from memory
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    # Train the model on a single step of experience
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    # Choose action based on epsilon-greedy policy
    def get_action(self, state):
        self.epsilon = 50 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        # Exploit learned knowledge
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    total_hits = 0 
    record = 0
    agent = Agent()
    game = PongGame(ai_mode=True)
    MAX_GAMES = 1000  

    while agent.n_games < MAX_GAMES:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score, hits = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            total_hits += game.hits 
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score

            print(f"Game: {agent.n_games} | Score: {score} | Record: {record} | Hits (this game): {hits} | Total Hits: {total_hits} | Last Reward: {reward}")

if __name__ == "__main__":
    train()

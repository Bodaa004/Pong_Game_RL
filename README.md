## 🏓 Pong Game with DQN AI Agent

This project implements a classic Pong game using **Pygame**, where one of the paddles is controlled by an AI agent trained via **Deep Q-Learning (DQN)** using **PyTorch**.

![pong-preview](https://upload.wikimedia.org/wikipedia/commons/1/1b/Pong.gif)

### 🎯 Features

* Classic Pong game built with Pygame
* AI agent trained using Deep Q-Network (DQN)
* Reinforcement Learning with experience replay and epsilon-greedy strategy
* Real-time gameplay between human and AI or AI vs. wall

---

## 📂 Project Structure

```
Pong-DQN-AI/
├── game.py          # Pygame-based Pong game logic
├── model.py         # Neural network model (PyTorch)
├── main.py          # Training loop for DQN agent
├── README.md        # Project documentation
└── requirements.txt # Required dependencies
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Bodaa004/Pong_Game_RL.git
cd Pong_Game_RL
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`**

```
pygame
torch
numpy
```

### 3. Run the game

#### Train AI Agent:

```bash
python main.py
```

#### Play against the wall (with or without AI):

Modify `ai_mode` in `main.py` to `False` for manual play.

---

## 🧠 DQN Overview

* **State:** `[ball_x, ball_y, ball_vx, ball_vy, paddle_y, ball_y - paddle_y]`

* **Action Space:** `[stay, up, down]`

* **Reward:**

  * +1 for hitting the ball
  * -1 for missing the ball
  * Small penalty for idle moves (optional)

* **Training Techniques:**

  * Experience replay (deque memory)
  * Short and long memory training
  * Epsilon decay for exploration/exploitation

---

## 📈 Example Output

```
Game: 1 | Score: 0 | Record: 0 | Hits (this game): 0 | Total Hits: 0 | Last Reward: -10
Game: 2 | Score: 1 | Record: 1 | Hits (this game): 0 | Total Hits: 0 | Last Reward: 10
Game: 3 | Score: 1 | Record: 1 | Hits (this game): 0 | Total Hits: 0 | Last Reward: -10
...
```

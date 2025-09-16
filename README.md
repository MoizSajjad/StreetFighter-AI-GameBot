# StreetFighter-AI-GameBot

## Introduction

This project implements an **AI-powered bot** that can autonomously play the classic **Street Fighter II Turbo** using Python and the **BizHawk emulator**.
The bot collects gameplay data, trains a supervised machine learning model, and predicts in-game actions in real time.

The aim of this project is to explore the use of **machine learning in real-time interactive environments** and demonstrate how AI can be applied to classic retro games.

---

## Key Features

* Complete ML pipeline: **data collection → preprocessing → model training → deployment**.
* Supports **Player 1** and **Player 2** through command-line arguments.
* Allows **Bot vs CPU** and **Bot vs Bot** gameplay.
* Records fight histories and logs states for future training and analysis.
* Uses a **Multi-Layer Perceptron (MLP)** for predicting controller inputs.
* Real-time communication with the BizHawk emulator using sockets.

---

## Project Structure

```
StreetFighter-AI-GameBot/
│
├── bot1.py             # AI bot logic (loads model, predicts next action)
├── controller1.py      # Communication with BizHawk emulator
├── data/               # Logged gameplay data (CSV files)
├── models/             # Trained model and scaler (.pkl files)
├── utils/              # Helper classes: Buttons, Player, GameState
└── README.md           # Project documentation
```

### File Descriptions

* **bot1.py**
  Loads the trained model (`best_mlp_bot_model.pkl`) and scaler, processes the current game state, predicts the next move, and generates button commands.

* **controller1.py**
  Connects to the BizHawk emulator, retrieves game state, logs data, invokes the bot, and sends commands back to the emulator.

* **Buttons / Player / GameState**
  Define the SNES controller, player attributes, and complete game state structure.

---

## Installation

1. Install **Python 3.6.3 or above**.
2. Download and install the **BizHawk emulator** with its prerequisites.
3. Clone this repository:

   ```bash
   git clone https://github.com/your-username/StreetFighter-AI-GameBot.git
   cd StreetFighter-AI-GameBot
   ```
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Launch BizHawk (`EmuHawk.exe`).

2. Load the ROM: *Street Fighter II Turbo (U).smc*.

3. In BizHawk, open **Tools → Tool Box**.

4. Run the bot:

   ```bash
   python controller1.py 1
   ```

   * Use `1` for Player 1 (left side).
   * Use `2` for Player 2 (right side).

5. To run two bots simultaneously:

   ```bash
   python controller1.py 1
   python controller1.py 2
   ```

---

## Model Training

* Data collected by logging game states and actions.
* Features: player health, coordinates, crouch/jump states, current move, and round timer.
* Trained **MLP model** with:

  * Hidden Layer 1: 100 neurons
  * Hidden Layer 2: 50 neurons
* Achieved \~60% accuracy in action prediction.
* Models and scalers are saved as `.pkl` files for runtime use.

---

## Results

* The bot successfully connects with BizHawk and autonomously plays matches.
* Consistent action prediction with \~60% accuracy.
* Demonstrates how AI can be applied to retro games for automation and experimentation.

---

## Future Work

* Collect larger and more diverse datasets.
* Explore advanced models (CNNs, LSTMs, Transformers).
* Perform hyperparameter optimization for higher accuracy.
* Extend framework to other SNES games using the BizHawk API.

---

## Requirements

* Windows 7 or above (64-bit)
* Python 3.6.3 or newer
* BizHawk emulator with prerequisites installed
* Street Fighter II Turbo ROM

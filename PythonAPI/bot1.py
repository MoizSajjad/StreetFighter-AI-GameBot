import joblib
import pandas as pd
import numpy as np
from command import Command
from buttons import Buttons
from sklearn.preprocessing import StandardScaler



target_columns = [
    'player1_left', 'player1_right', 'player1_up', 'player1_down', 'player1_A', 'player1_B', 'player1_X', 'player1_Y', 'player1_L', 'player1_R',
    'player2_left', 'player2_right', 'player2_up', 'player2_down', 'player2_A', 'player2_B', 'player2_X', 'player2_Y', 'player2_L', 'player2_R'
]

class Bot:

    def __init__(self):
        # Load the trained XGBoost model
        self.model = joblib.load('best_mlp_bot_model.pkl')
        self.scaler = joblib.load('scaler.pkl') 
        self.fire_code = ["<", "!<", "v+<", "!v+!<", "v", "!v", "v+>", "!v+!>", ">+Y", "!>+!Y"]
        self.exe_code = 0
        self.start_fire = True
        self.remaining_code = []
        self.my_command = Command()
        self.buttn = Buttons()
        

    def fight(self, current_game_state, player):
        # Convert the current game state to a feature vector
        features = self.get_features(current_game_state)
        df = pd.DataFrame([features], columns=self.scaler.feature_names_in_)
        X = self.scaler.transform(df)

        pred = self.model.predict(X)[0]
        
        p1_btns = Buttons()
        p2_btns = Buttons()

        p1_names = [
            "left", "right", "up", "down", "A", "B", "X", "Y", "L", "R"
        ]

        p2_names = [
            "left", "right", "up", "down", "A", "B", "X", "Y", "L", "R"
        ]

        for i, name in enumerate(p1_names):
            setattr(p1_btns, name, bool(pred[i]))
        for i, name in enumerate(p2_names):
            setattr(p2_btns, name, bool(pred[i]))

        cmd = Command()
        if player == "1":
            cmd.player_buttons = p1_btns
        elif player == "2":
            cmd.player2_buttons = p2_btns  
                  
        # If you used feature scaling in your training, scale the features before passing to the model
        # features_scaled = self.scaler.fit_transform([features])[0]

        # # Predict the action using the trained model
        # action = self.model.predict([features_scaled])[0]  # Get the predicted action


        # Set the command based on the predicted action
        # self.set_command(action, current_game_state, player)

        return cmd

    def get_features(self, game_state):
        # Convert the game state into a feature vector (correct access to buttons)
        features = [
            game_state.timer,
            game_state.has_round_started,
            game_state.is_round_over,
            game_state.player1.player_id,
            game_state.player1.health,
            game_state.player2.player_id,
            game_state.player2.health,
            game_state.player1.x_coord,
            game_state.player1.y_coord,
            game_state.player2.x_coord,
            game_state.player2.y_coord,
            game_state.player1.is_jumping,
            game_state.player1.is_crouching,
            game_state.player2.is_jumping,
            game_state.player2.is_crouching,
        

            # game_state.fight_result
            # Accessing button states from the player1.player_buttons object
            # game_state.player1.player_buttons.left, 
            # game_state.player1.player_buttons.right, 
            # game_state.player1.player_buttons.up, 
            # game_state.player1.player_buttons.down, 
            # game_state.player1.is_jumping,
            # game_state.player1.is_crouching,
            # game_state.player1.player_buttons.A, 
            # game_state.player1.player_buttons.B, 
            # game_state.player1.player_buttons.X, 
            # game_state.player1.player_buttons.Y,
            # game_state.player1.player_buttons.L, 
            # game_state.player1.player_buttons.R,
        
            # Accessing button states from the player2.player_buttons object
            # game_state.player2.player_buttons.left, 
            # game_state.player2.player_buttons.right, 
            # game_state.player2.player_buttons.up, 
            # game_state.player2.player_buttons.down, 
            # game_state.player2.is_jumping,
            # game_state.player2.is_crouching,
            # game_state.player2.player_buttons.A, 
            # game_state.player2.player_buttons.B, 
            # game_state.player2.player_buttons.X, 
            # game_state.player2.player_buttons.Y,
            # game_state.player2.player_buttons.L, 
            # game_state.player2.player_buttons.R
            # game_state.fight_result
        ]
        return features



    def set_command(self, action, game_state, player):
        # Set the command for Player 1 based on the predicted action
        if player == "1":
            self.set_player1_command(action, game_state)
        elif player == "2":
            self.set_player2_command(action, game_state)

    def set_player1_command(self, action, game_state):
        # Set the buttons for player 1 based on the predicted action
        if action == 0:  # Action 0: "move left"
            self.buttn.left = True
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 1:  # Action 1: "move right"
            self.buttn.right = True
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 2:  # Action 2: "press A"
            self.buttn.A = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 3:  # Action 3: "press B"
            self.buttn.B = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 4:  # Action 4: "jump"
            self.buttn.up = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 5:  # Action 5: "crouch"
            self.buttn.down = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False
        
        elif action == 6:  # Action 8: "press X"
            self.buttn.X = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 7:  # Action 9: "press Y"
            self.buttn.Y = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 8:  # Action 10: "press L"
            self.buttn.L = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 9:  # Action 11: "press R"
            self.buttn.R = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False

        elif action == 10: # Combo 1: "left + A"
            self.buttn.left = True
            self.buttn.A = True
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 11: # Combo 2: "right + B"
            self.buttn.right = True
            self.buttn.B = True
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 12: # Combo 3: "up + X"
            self.buttn.up = True
            self.buttn.X = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 13: # Combo 4: "down + Y"
            self.buttn.down = True
            self.buttn.Y = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 14: # Combo 5: "left + L"
            self.buttn.left = True
            self.buttn.L = True
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 15: # Combo 6: "right + R"
            self.buttn.right = True
            self.buttn.R = True
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False

        elif action == 16: # Combo 7: "up + L"
            self.buttn.up = True
            self.buttn.L = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 17: # Combo 8: "down + R"
            self.buttn.down = True
            self.buttn.R = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False

        elif action == 18: # Combo 9: "X + A + B"
            self.buttn.X = True
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 19: # Combo 10: "Y + A + B"
            self.buttn.Y = True
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.X = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 20: # Combo 11: "X + L + R"
            self.buttn.X = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.Y = False

        elif action == 21: # Combo 12: "Y + L + R"
            self.buttn.Y = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False

        elif action == 22: # Combo 13: "A + L + R"
            self.buttn.A = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False

        elif action == 23: # Combo 14: "B + L + R"
            self.buttn.B = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.X = False
            self.buttn.Y = False
        
        elif action == 24: # Combo 15: "A + B + L"
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.L = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 25: # Combo 16: "A + B + R"
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False


        # Set the final command for player 1
        self.my_command.player_buttons = self.buttn

    def set_player2_command(self, action, game_state):
        # Set the buttons for player 2 based on the predicted action
        if action == 0:  # Action 0: "move left"
            self.buttn.left = True
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 1:  # Action 1: "move right"
            self.buttn.right = True
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 2:  # Action 2: "press A"
            self.buttn.A = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 3:  # Action 3: "press B"
            self.buttn.B = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 4:  # Action 4: "jump"
            self.buttn.up = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 5:  # Action 5: "crouch"
            self.buttn.down = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False
        
        elif action == 6:  # Action 6: "press X"
            self.buttn.X = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 7:  # Action 7: "press Y"
            self.buttn.Y = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 8:  # Action 8: "press L"
            self.buttn.L = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 9:  # Action 9: "press R"
            self.buttn.R = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False

        elif action == 10: # Combo 1: "left + A"
            self.buttn.left = True
            self.buttn.A = True
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 11: # Combo 2: "right + B"
            self.buttn.right = True
            self.buttn.B = True
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 12: # Combo 3: "up + X"
            self.buttn.up = True
            self.buttn.X = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 13: # Combo 4: "down + Y"
            self.buttn.down = True
            self.buttn.Y = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 14: # Combo 5: "left + L"
            self.buttn.left = True
            self.buttn.L = True
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 15: # Combo 6: "right + R"
            self.buttn.right = True
            self.buttn.R = True
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False

        elif action == 16: # Combo 7: "up + L"
            self.buttn.up = True
            self.buttn.L = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 17: # Combo 8: "down + R"
            self.buttn.down = True
            self.buttn.R = True
            self.buttn.left = False
            self.buttn.right = False
            self.buttn.up = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False

        elif action == 18: # Combo 9: "X + A + B"
            self.buttn.X = True
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.Y = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 19: # Combo 10: "Y + A + B"
            self.buttn.Y = True
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.X = False
            self.buttn.L = False
            self.buttn.R = False

        elif action == 20: # Combo 11: "X + L + R"
            self.buttn.X = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.Y = False

        elif action == 21: # Combo 12: "Y + L + R"
            self.buttn.Y = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.B = False
            self.buttn.X = False

        elif action == 22: # Combo 13: "A + L + R"
            self.buttn.A = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.B = False
            self.buttn.X = False
            self.buttn.Y = False

        elif action == 23: # Combo 14: "B + L + R"
            self.buttn.B = True
            self.buttn.L = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.A = False
            self.buttn.X = False
            self.buttn.Y = False
        
        elif action == 24: # Combo 15: "A + B + L"
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.L = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.R = False

        elif action == 25: # Combo 16: "A + B + R"
            self.buttn.A = True
            self.buttn.B = True
            self.buttn.R = True
            self.buttn.right = False
            self.buttn.left = False
            self.buttn.up = False
            self.buttn.down = False
            self.buttn.X = False
            self.buttn.Y = False
            self.buttn.L = False


        # Set the final command for player 2
        self.my_command.player2_buttons = self.buttn

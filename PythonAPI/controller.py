import socket
import json
from game_state import GameState
import os
import csv
#from bot import fight
import sys
from bot import Bot
def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

def log_game_state(game_state, bot_command):
    
    csv_file = "game_state1.csv"

    file_exists = os.path.isfile(csv_file)

    header = [
        "timer", 
        "has_round_started", 
        "is_round_over", 
        "player1_ID",
        "player1_health", 
        "player2_ID",
        "player2_health", 
        "player1_x_coord", 
        "player1_y_coord", 
        "player2_x_coord", 
        "player2_y_coord", 
        "player1_left", 
        "player1_right", 
        "player1_up",
        "player1_down",
        "player1_jump", 
        "player1_crouch", 
        "player1_A", 
        "player1_B", 
        "player1_X", 
        "player1_Y", 
        "player1_L", 
        "player1_R", 
        "player2_left", 
        "player2_right",
        "player2_up",
        "player2_down", 
        "player2_jump", 
        "player2_crouch", 
        "player2_A", 
        "player2_B", 
        "player2_X", 
        "player2_Y", 
        "player2_L", 
        "player2_R", 
        "fight_result"
        ]
    player1_buttons = game_state.player1.player_buttons
    player2_buttons = game_state.player2.player_buttons

    row_data= [
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
        player1_buttons.left, 
        player1_buttons.right, 
        player1_buttons.up,
        player1_buttons.down,
        game_state.player1.is_jumping,
        game_state.player1.is_crouching,
        player1_buttons.A, 
        player1_buttons.B, 
        player1_buttons.X,
        player1_buttons.Y,
        player1_buttons.L,
        player1_buttons.R,
        player2_buttons.left, 
        player2_buttons.right,
        player2_buttons.up,
        player2_buttons.down, 
        game_state.player2.is_jumping,
        game_state.player2.is_crouching,
        player2_buttons.A, 
        player2_buttons.B,
        player2_buttons.X,
        player2_buttons.Y,
        player2_buttons.L,
        player2_buttons.R,
        game_state.fight_result
    ]

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header only if the file is new
        if not file_exists:
            writer.writerow(header)

        # Write the data
        writer.writerow(row_data)
        

def main():
    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    #print( current_game_state.is_round_over )
    bot=Bot()
    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state,sys.argv[1])
        log_game_state(current_game_state, bot_command)
        send(client_socket, bot_command)
if __name__ == '__main__':
   main()

import csv
import os
import socket
import json
from game_state import GameState
import time
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

# def receive(client_socket):
#     #receive the game state and return game state
#     pay_load = client_socket.recv(4096)
#     input_dict = json.loads(pay_load.decode())
#     game_state = GameState(input_dict)

#     return game_state

def receive(client_socket: socket) -> GameState:
    # Receive the game state and return game state
    payload = client_socket.recv(4096)
    input_dict = json.loads(payload.decode())
    game_state = GameState(input_dict)
    # Header for the CSV file
    header = [
    'timer',
    'fight_result',
    'has_round_started',
    'is_round_over',
    # 'player1',
    'player1_health',
    'player1_x_coord',
    'player1_y_coord',
    'player1_is_jumping',
    'player1_is_crouching',
    'player1_is_player_in_move',
    'player1_move_id',
    'player1_buttons_up',
    'player1_buttons_down',
    'player1_buttons_right',
    'player1_buttons_left',
    # 'player2',
    'player2_health',
    'player2_x_coord',
    'player2_y_coord',
    'player2_is_jumping',
    'player2_is_crouching',
    'player2_is_player_in_move',
    'player2_move_id',
    'player2_buttons_up',
    'player2_buttons_down',
    'player2_buttons_right',
    'player2_buttons_left'
    ]
    # Ensure the CSV file exists and contains the header
    if not os.path.isfile('game_state.csv'):
        print("Creating New File!!!")
        with open('game_state.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        print("\n\nUpdating game_state File!!!")
        with open('game_state.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            if not next(reader, None):  # The file is empty
                print("File Empty")
                writer = csv.writer(file)
                writer.writerow(header)

        # Write game state to CSV file
        with open('game_state.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
            game_state.timer,
            game_state.fight_result,
            game_state.has_round_started,
            game_state.is_round_over,
            # game_state.player1,
            game_state.player1.health,
            game_state.player1.x_coord,
            game_state.player1.y_coord,
            game_state.player1.is_jumping,
            game_state.player1.is_crouching,
            game_state.player1.is_player_in_move,
            game_state.player1.move_id,
            game_state.player1.player_buttons.up,
            game_state.player1.player_buttons.down,
            game_state.player1.player_buttons.right,
            game_state.player1.player_buttons.left,
            # game_state.player2,
            game_state.player2.health,
            game_state.player2.x_coord,
            game_state.player2.y_coord,
            game_state.player2.is_jumping,
            game_state.player2.is_crouching,
            game_state.player2.is_player_in_move,
            game_state.player2.move_id,
            game_state.player2.player_buttons.up,
            game_state.player2.player_buttons.down,
            game_state.player2.player_buttons.right,
            game_state.player2.player_buttons.left
            ])

    return game_state

# def receive(client_socket):
#     #receive the game state and return game state
#     pay_load = client_socket.recv(4096)
#     input_dict = json.loads(pay_load.decode())
#     game_state = GameState(input_dict)

#     return game_state


def main():
    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    # print( current_game_state.is_round_over )
    bot=Bot()
    while (current_game_state is None) or (not current_game_state.is_round_over):
        # print("\n\n--------------- In main ------------")
        # print("Current Game State:{}".format(current_game_state))
        #time.sleep(1)
        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state,sys.argv[1])
        send(client_socket, bot_command)
if __name__ == '__main__':
   main()

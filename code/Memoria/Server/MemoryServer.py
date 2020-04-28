"""
Will handle all connections and their games
"""

import pickle
from code.Memoria.Client.Game import Game
from _thread import start_new_thread
import socket
from os import strerror
import queue
import time
import threading

# Server Set up

PORT = 5555
HOST = ''
DELAY = 0.5
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((HOST, PORT))
except socket.error as e:
    code = e.errno
    error = strerror(code)
    print(f"Error message corresponding to the code {code}:\n-> {error}")

server.listen(2)

print("[STARTED] -> waiting for connection...")

# Global Variables

games = {}
id_count = 0


def waitTime(s, q):
    time.sleep(s)
    q.put("True")
    print("ended thread")


def threaded_client(conn, pid, game_id):
    """
    Creates a new thread for the client, connecting him to the game instance
    :param conn: str
    :param pid: int (Player id)
    :param game_id: int
    :return: None
    """
    global id_count
    conn.send(bytes(str(pid), encoding='utf-8'))
    q = queue.Queue()

    while True:
        try:

            # RECEIVES DATA

            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                try:

                    # FINISHES THE TURN WHEN THE CARDS ARE FLIPPED AFTER THE DELAY

                    if q.get(block=False):
                        game.block = False

                        if not game.check_pair():
                            game.finished_turn()

                        game.reset_turn()
                        game.reset_selected()
                        print("True")

                except queue.Empty:
                    pass

                # IF THERE'S NO DATA IT ASSUMES FAILURE

                if not data:
                    print("[ERROR] --> No data received")
                    break
                else:

                    if data == "again":

                        # PLAY AGAIN LOGIC
                        if game.ready:
                            print("RESTARTING GAME")
                            game.end = False

                        print("READY")
                        game.ready = True

                    # RESETS

                    elif data == "reset":
                        game.reset_game()

                    # SETS NAME

                    elif 'name' in data:
                        name = data.split(' ')[1]
                        game.set_name(pid, name)

                    # PLAYS

                    elif data != "get":

                        if not game.block:
                            print("play")
                            game.play(int(data))
                            print(game.turn)

                    # ENDS GAME WAITS FOR READY UP
                    if not game.end and len(game.pairs_gotten) == (game.total_pairs * 2):  # TODO:
                        print("Game Ended")
                        game.end = True
                        game.ready = False
                        ready = 0
                        game.reset_game()

                    # STARTS FLIPPING COROUTINE

                    if game.turn == 2 and not game.block:
                        print("blocking")
                        game.block = True
                        t1 = threading.Thread(target=waitTime, args=(DELAY, q))
                        t1.start()

                    # SENDS GAME

                    conn.sendall(pickle.dumps(game))  # sends state of game
            else:
                print("Game not found -> Attempting to quit connection...")
                break
        except socket.error as e:
            code = e.errno
            error = strerror(code)
            print(f"Error message corresponding to the code {code}:\n-> {error}")

    print("Lost connection")
    try:
        del games[game_id]
        print(f"Closing Game --> {game_id}")
    except Exception as e:
        print("[ERROR CLOSING GAME] -> ", e)
    id_count -= 1
    conn.close()


if __name__ == "__main__":
    while True:
        conn, addr = server.accept()

        print(f"[CONNECTED] --> {addr}")

        id_count += 1
        player_id = 0
        game_id = (id_count - 1) // 2  # Pairs of two players will get the same Game

        if id_count % 2 == 1:
            games[game_id] = Game(game_id)
            print(f"[NEW GAME] -> {game_id}")
        else:
            games[game_id].ready = True
            player_id = 1
            print(f"[GAME FULL] -> {game_id}")

        start_new_thread(threaded_client, (conn, player_id, game_id))
        # This way new connections are non blocking, most of the time the connection is waiting.

"""
Will assist Client by connecting and facilitating send and recv requests
"""

import socket
from os import strerror
import pickle


class Network(object):
    def __init__(self):
        """
        Initializes the object
        """
        self.port = 5555
        self.host = ''
        self.addr = (self.host, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p = self.connect()

    def connect(self):
        """
        Connects to the server
        :return: int (player id)
        """
        try:
            self.client.connect(self.addr)
            return int(self.client.recv(2048).decode())  # Receives player id
        except socket.error as e:
            code = e.errno
            error = strerror(code)
            print(f"Error message corresponding to the code {code}:\n-> {error}")

    def send(self, data):
        """
        Sends codes to server
        :return: Game 
        """
        try:
            self.client.send(bytes(data, encoding='utf-8'))
            return pickle.loads(self.client.recv(4096))  # Returns Game Object
        except socket.error as e:
            code = e.errno
            error = strerror(code)
            print(f"Error message corresponding to the code {code}:\n-> {error}")


if __name__ == "__main__":
    n = Network()
    print(n.p)


    game = n.send('1')
    print(game.turn)
    print(game.get_player_move())
    game = n.send('2')
    print(game.turn)
    print(game.get_player_move()) # 1
    game = n.send('3')
    print(game.turn)
    print(game.get_player_move())
    game = n.send('4')
    print(game.selected)
    print(game.back)

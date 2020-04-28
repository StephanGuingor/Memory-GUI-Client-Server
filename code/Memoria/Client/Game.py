"""
Will have the current game state between two players
"""

import random


class Game(object):

    def __init__(self, game_id):
        """
        Initializes the game object

        Variables
        :game_id: int
        :_total_pairs: int
        :board: List
        :turn: int
        :p1_went: Bool
        :p2_went: Bool
        :p1_pairs: Bool
        :p2_pairs: Bool
        :pairs_gotten: List
        :end: Bool
        :selected: [int,int]
        :wins: [int,int]
        :ties: int
        """
        self.game_id = game_id
        self.total_pairs = 8 #TODO:
        self.board = [i for i in range(self.total_pairs)] * 2  # grid 4 x 4 (could use matrix)
        random.shuffle(self.board)
        self.back = [-1 for _ in range(len(self.board))]
        self.turn = 0
        self.p1_went = False
        self.p2_went = True  # switch this values
        self.p1_pairs = 0
        self.p2_pairs = 0
        self.pairs_gotten = []
        self.selected = [None, None]  # keeps idx
        self.p1_name = 'P1'
        self.p2_name = 'P2'
        self.ready = False
        self.block = False
        self.end = False #TODO:
        self.wins = [0, 0]
        self.ties = 0

        # LAST WIN
        self.last = None

    def play(self, idx):
        """
        Player chooses a card and reveals it
        """
        try:
            if self.turn == 0:
                move = self.board[idx]  # get move 0

                if self.validate_card(idx):
                    self.back[idx] = move  # Flips card
                    self.selected[0] = idx  # Locks move
                    self.turn += 1

            elif self.turn == 1:
                move = self.board[idx]  # get move 1

                if self.validate_card(self.selected[0], idx):
                    self.back[idx] = move  # Flips card
                    self.selected[1] = idx  # Locks move
                    self.turn += 1

                # self.finished_turn()  # ends turn
            else:
                # self.check_pair()  # points to other player
                # self.reset_turn()
                # self.reset_selected()
                self.play(idx)  # plays after reset

        except IndexError as e:
            print("[ERROR] -> Invalid Index", e)

    def reset_selected(self):
        """
        Resets the selected cards
        """
        self.selected = [None, None]

    def validate_card(self, *cards):
        """"
        Validates the cards
        :*cards: [int,...]
        """
        # Checks if cards are not the same index and that index is not repeated
        if len(cards) == 2:
            if cards[0] == cards[1] or cards[1] in self.pairs_gotten:
                return False
        else:
            # Checks if card was chosen before
            if cards[0] in self.pairs_gotten:
                return False
        # No Issues
        return True

    def check_pair(self):
        """
        Checks if a player got a pair and updates the pairs gotten appropriately
        """
        idx1 = self.selected[0]
        idx2 = self.selected[1]

        print(self.selected)
        if self.board[idx1] != self.board[idx2]:
            self.back[idx1], self.back[idx2] = (-1, -1)  # Resets cards
        else:
            if self.get_player_move() != 0:
                self.p1_pairs += 1
            else:
                self.p2_pairs += 1
            # Appends the card indexes
            self.pairs_gotten.append(idx1)
            self.pairs_gotten.append(idx2)
            return True

    def winner(self):
        """
        Returns an integer (representing the winner) depending on the number of pairs of each player.
        :Codes:
        2 -> equal
        0 -> p1
        1 -> p2
        :return: int
        """
        if self.p1_pairs == self.p2_pairs:
            return 2  # equal
        elif self.p1_pairs > self.p2_pairs:
            return 0
        else:
            return 1

    def finished_turn(self):
        """
        Switches the played status of each player
        """
        self.p1_went, self.p2_went = self.p2_went, self.p1_went

    def get_player_move(self):
        """
        Returns the active player

        :return: int
        """
        # print("getp")
        return 1 if self.p1_went else 0  # 0 == p1, 1 == p2

    def reset_turn(self):
        """
        Resets turn variable
        """
        self.turn = 0

    def set_name(self, pid, name):
        """
        Sets player name
        """
        if pid == 0:
            self.p1_name = name
        else:
            self.p2_name = name

    def reset_game(self):
        """
        Reset all the variables needed to re-start a new game
        """
        # Adds win to player
        winner = self.winner()

        # Saves the last value
        self.last = winner

        if winner == 0:
            self.wins[0] += 1

        elif winner == 1:
            self.wins[1] += 1
        else:
            self.ties += 1

        # Resets variables
        self.p1_went = False
        self.p2_went = True
        self.board = [i for i in range(self.total_pairs)] * 2
        random.shuffle(self.board)
        self.back = [-1 for _ in range(len(self.board))]
        self.p1_pairs = 0
        self.p2_pairs = 0
        self.reset_turn()
        self.selected = [None, None]
        self.pairs_gotten = []

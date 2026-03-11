import random

class randomPlayer:
    def __init__(self, player='X'):
       self.player = 1 if player == 'X' else -1

    def play(self, board):
        moves = board.validMoves()
        choice = random.choice(moves)
        return int(choice)

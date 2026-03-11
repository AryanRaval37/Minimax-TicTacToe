import numpy as np
import warnings

#####################################################
# Board class for the game:
# 1 for X
# -1 for O
# 0 for empty
######################################################
class Board():
    def __init__(self):
        self.dim = 3
        self.arr = np.zeros(self.dim**2)

    # always give numbers from 1 to 9 instead of 0 to 8
    def get(self, pos):
        return self.arr[pos - 1]
    
    def remove(self, pos):
        self.arr[pos - 1] = 0
    
    def isLegalMove(self, pos):
        return self.arr[pos - 1] == 0
    
    # always give numbers from 1 to 9 instead of 0 to 8
    def place(self, pos, val):
        if (self.arr[pos - 1] != 0):
            warnings.warn("Board Class Warning: You trying to play a move on the board which is already filled... That move will be replaced.")
        self.arr[pos - 1] = val

    def validMoves(self):
        return np.where(self.arr == 0)[0] + 1

    def copy(self):
        new_board = Board()
        new_board.arr = self.arr.copy()
        return new_board


    # provide numbers from 1 to 3, (2, 3) meaning second row third column or position 6
    def TwoDtoOne(self, t):
        return self.dim * (t[0] - 1) + t[1]
    
    # provide numbers from 1 to 3, (2, 3) meaning second row third column or position 6
    def OneDtoTwo(self, pos):
        return (int(pos / self.dim), pos % self.dim)
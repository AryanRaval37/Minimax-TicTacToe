from board import *

#####################################################
# Main engine that will run the game
class Engine:
    def __init__(self, player1, player2):
        self.board = Board()
        self.p1 = player1 # X
        self.p2 = player2 # O

    # Returns the current state of the game
    # 1 if X = player1 won
    # -1 if O = player2 won
    # 0 if draw
    # 2 if game is still not over
    @staticmethod
    def state(board):
        a = board.arr
        # horizontal
        if (a[0] == a[1] == a[2]):
            if (a[0] != 0): return a[0]
        if (a[3] == a[4] == a[5]):
            if (a[3] != 0): return a[3]
        if (a[6] == a[7] == a[8]):
            if (a[6] != 0): return a[6]

        # vertical
        if (a[0] == a[3] == a[6]):
            if (a[0] != 0): return a[0]
        if (a[1] == a[4] == a[7]):
            if (a[1] != 0): return a[1]
        if (a[2] == a[5] == a[8]):
            if (a[2] != 0): return a[2]

        # diagonals
        if (a[0] == a[4] == a[8]):
            if (a[0] != 0): return a[0]
        if (a[2] == a[4] == a[6]):
            if (a[2] != 0): return a[2]
        
        # if here then no one has won yet
        if len(board.validMoves()) == 0:  # no empty cells left → draw
            return 0
        else:
            return 2  # game still in progress


    # Returns the result of the game
    # 1 if X = player1 won
    # -1 if O = player2 won
    # 0 if draw
    # 2 if game not finished because player made illegal move   
    def playGame(self):
        move = 1 # p1 goes first
        while (self.state(self.board) == 2):
            if (move == 1):
                # passing the copy of the board to the player so that he does not cheat by modifying the board
                pos = self.p1.play(self.board.copy())
                if (self.board.isLegalMove(pos)):
                    self.board.place(pos, 1) # 1 is for X = Player 1
                else: return 2

            # elif important here as we want only one move per iteration of while
            elif (move == -1):
                # passing the copy of the board to the player so that he does not cheat by modifying the board
                pos = self.p2.play(self.board.copy())
                if (self.board.isLegalMove(pos)):
                    self.board.place(pos, -1) # -1 is for O = Player 2
                else: return 2

            move *= -1

        result = self.state(self.board)

        # Notify players if they implement onResult(result, board)
        for player in (self.p1, self.p2):
            if hasattr(player, "onResult"):
                player.onResult(result, self.board)

        return result
        
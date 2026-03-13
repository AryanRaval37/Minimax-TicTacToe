from engine import *

class minimaxPlayer:
    def __init__(self, player='X'):
        self.player = 1 if player == 'X' else -1

    ######################################################
    # Evaluation function
    # 1 if X = player1 won
    # -1 if O = player2 won
    # 0 if draw
    # if nothing goes wrong then 2 will be return here.
    ######################################################
    def eval(self, board):
        return Engine.state(board) * self.player

    #########################################################
    # Returns [bestMove, bestScore]
    def minimax(self, board, alpha, beta, maximising = True):
        # first check if game is over or not
        if Engine.state(board) != 2: # game is over
            return -1, self.eval(board)
    
        # game is not over, turn of maximising player
        if maximising:
            bestScore = -100
            bestMove = -1
            # try out the valid moves
            for move in board.validMoves():
                board.place(move, self.player) # place that move
                # get evaluation of this move 
                curEval = self.minimax(board, alpha, beta, maximising=False)
                board.remove(move)
                if (curEval[1] > bestScore):
                    bestScore = curEval[1]
                    bestMove = move
                    alpha = max(alpha, bestScore)
                if beta <= alpha:
                    break
            # now that we know the best move here,
            return bestMove, bestScore

        if not maximising:
            bestScore = 100 # minimizing player tries to minize score
            bestMove = -1
            # try out the valid moves
            for move in board.validMoves():
                board.place(move, -self.player) # place that move
                # get evaluation of this move 
                curEval = self.minimax(board, alpha, beta, maximising=True)
                board.remove(move)
                if (curEval[1] < bestScore):
                    bestScore = curEval[1]
                    bestMove = move
                    beta = min(beta, bestScore)
                if beta <= alpha:
                    break
            # now that we know the best move here,
            return bestMove, bestScore
        

    def play(self, board):
        # finding the best move
        bestMove, bestScore = self.minimax(board, -100, 100)
        return bestMove
        

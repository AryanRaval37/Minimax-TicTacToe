from engine import Engine
from players.randomPlayer import randomPlayer
from players.humanPlayer import HumanPlayer
from players.minimax import minimaxPlayer

human  = HumanPlayer(player='O')
ai     = minimaxPlayer(player='X')

engine = Engine(ai, human)
result = engine.playGame()
print(result)

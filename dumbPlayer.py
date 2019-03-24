from player import Player
class DumbPlayer(Player):
    def __init__(self, mySymbol, opponentSymbol):
        super().__init__(mySymbol, opponentSymbol)
    def makeMove(self, board):
        for row in range(len(board)):
            for col in range(len(board[0])):
                if not board[row][col]:
                    return row,col
    def __str__(self):
        return "Dumb Player"


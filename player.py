class Player:
    """ a generic player class. All players implemented should inherit this class """
    def __init__(self, mySymbol, opponentSymbol):
        self.mySymbol = mySymbol
        self.opponentSymbol = opponentSymbol
    def makeMove(self, board):
        pass
    def __str__(self):
        return "Generic Player"

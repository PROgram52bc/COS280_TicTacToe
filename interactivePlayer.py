from player import Player
from utility import printBoard
class InteractivePlayer(Player):
    def __init__(self, mySymbol, opponentSymbol):
        super().__init__(mySymbol, opponentSymbol)
    def makeMove(self, board):
        printBoard(board)
        print("Your symbol: {:.3}".format(self.mySymbol))
        while True:
            row = input("Enter row number(0-2): ")
            try:
                row = int(row)
                break;
            except ValueError as e:
                print("Please enter a valid integer!")
                continue;

        while True:
            col = input("Enter col number(0-2): ")
            try:
                col = int(col)
                break;
            except ValueError as e:
                print("Please enter a valid integer!")
                continue;
        return row, col
    def __str__(self):
        return "Interactive Player"


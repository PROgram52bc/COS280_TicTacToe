from random import randint
class Player:
    def __init__(self, mySymbol, opponentSymbol):
        self.mySymbol = mySymbol
        self.opponentSymbol = opponentSymbol
    def makeMove(self, board):
        pass
    def __str__(self):
        return "Generic Player"

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

def printBoard(board):
    for row in board:
        print("{:-^19}".format(""))
        print("|", end="")
        for col in row:
            if col:
                print("{:^5.3}".format(col), end="|")
            else:
                print("{:5}".format(""), end="|")
        print("")
    print("{:-^19}".format(""))


class TicTacToe:
    """ class representing a tic-tac-toe game. """
    def __init__(self, Player1, Player2, symbolPlayer1="x", symbolPlayer2="o"):
        self.board = [
                [None,None,None],
                [None,None,None],
                [None,None,None]
                ]
        print("TicTacToe initiated.")
        self.playerSymbols = (symbolPlayer1, symbolPlayer2)
        player1 = Player1(symbolPlayer1, symbolPlayer2)
        print("Set {:s} with symbol {:.3s}".format(player1.__str__(), symbolPlayer1))
        player2 = Player2(symbolPlayer2, symbolPlayer1)
        print("Set {:s} with symbol {:.3s}".format(player2.__str__(), symbolPlayer2))
        self.playerObjects = (player1, player2)
        self.currentPlayerIdx = randint(0,1)
        self.winner = None
    def getWinner(self):
        #print("Get Winner ran.")
# check for row
        for row in self.board:
            if row[0]: # if first element in row is occupied
                rowEqual = [x == row[0] for x in row[1:]]
                if all(rowEqual): # and if row is all the same
                    #print("Row equal:",row)
                    return row[0]
# check for col
        for colidx in range(len(self.board[0])):
            col = [row[colidx] for row in self.board] # generate a list of the column
            if col[0]: # if first element in col is occupied
                colEqual = [x == col[0] for x in col[1:]]
                if all(colEqual): # and if row is all the same
                    #print("Col equal:",col)
                    return col[0]
# check for diagonal
        tlbrDiag = [self.board[i][i] for i in range(len(self.board))] # tlbr = Top Left Bottom Right
        if tlbrDiag[0]:
            tlbrEqual = [x == tlbrDiag[0] for x in tlbrDiag[1:]]
            if all(tlbrEqual):
                #print("tlbr diag equal:",tlbrDiag,tlbrEqual)
                return tlbrDiag[0]

        trblDiag = [self.board[len(self.board)-i-1][i] for i in range(len(self.board))] # trbl = Top Right Bottom Left
        if trblDiag[0]:
            trblEqual = [x == trblDiag[0] for x in trblDiag[1:]]
            if all(trblEqual):
                #print("trbl diag equal:",trblDiag,trblEqual)
                return trblDiag[0]
        return None

    def boardFull(self):
        for row in self.board:
            for col in row:
                if not col:
                    return False
        return True

    def nextRound(self):
        self.currentPlayerIdx = 0 if self.currentPlayerIdx == 1 else 1

    def inBound(self,row,col):
        return row>=0 and col>=0 and row<len(self.board) and col<len(self.board[0])

    def resetBoard(self):
        for rowidx in range(len(self.board)):
            for colidx in range(len(self.board[0])):
                self.board[rowidx][colidx] = None

    def start(self):
        while True:
            print("Player {:.3}'s move".format(self.playerSymbols[self.currentPlayerIdx]))
            row, col = self.playerObjects[self.currentPlayerIdx].makeMove(self.board)
            if not self.inBound(row,col):
                #raise IndexError("Invalid move {:d},{:d} given by player {:.3}".format(row,col,self.playerSymbols[self.currentPlayerIdx]))
                print("Invalid position {:d},{:d} given by player {:.3}, try again...".format(row,col,self.playerSymbols[self.currentPlayerIdx]))
                continue
            if self.board[row][col]:
                #raise ValueError("Invalid move {:d},{:d} given by player {:.3}".format(row,col,self.playerSymbols[self.currentPlayerIdx]))
                print("Already occupied position {:d},{:d} given by player {:.3}, try again...".format(row,col,self.playerSymbols[self.currentPlayerIdx]))
                continue
            print("player {:.3} making a move on {:d},{:d}".format(self.playerSymbols[self.currentPlayerIdx],row,col))
            self.board[row][col] = self.playerSymbols[self.currentPlayerIdx]
            self.nextRound()
            self.winner = self.getWinner()
            if self.winner:
                print("Player {:.3} won!".format(self.winner))
                break;
            if self.boardFull():
                print("Tie!")
                break;
        print("Final board status:")
        printBoard(self.board)




if __name__ == "__main__":
    ttt = TicTacToe(InteractivePlayer, DumbPlayer)
    ttt.start()


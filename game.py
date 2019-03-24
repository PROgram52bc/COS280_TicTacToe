from random import randint
from dumbPlayer import DumbPlayer
from interactivePlayer import InteractivePlayer
from bruteForcePlayer import BruteForcePlayer
from utility import printBoard, getWinner, boardFull
import copy

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
        return getWinner(self.board)
    def boardFull(self):
        return boardFull(self.board)

    def nextRound(self):
        self.currentPlayerIdx = 0 if self.currentPlayerIdx == 1 else 1

    def inBound(self,row,col):
        return row>=0 and col>=0 and row<len(self.board) and col<len(self.board[0])

    def resetBoard(self):
        for rowidx in range(len(self.board)):
            for colidx in range(len(self.board[0])):
                self.board[rowidx][colidx] = None

    def start(self):
        printBoard(self.board)
        while True:
            print("Player {:.3}'s move".format(self.playerSymbols[self.currentPlayerIdx]))
            row, col = self.playerObjects[self.currentPlayerIdx].makeMove(board=copy.deepcopy(self.board))
            printBoard(self.board)
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
    ttt = TicTacToe(BruteForcePlayer, InteractivePlayer, 'b', 'i')
    ttt.start()

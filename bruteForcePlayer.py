from player import Player
from utility import printBoard, getWinner, boardFull
import copy

# Convention in passing object to function call:
# Before modifying the parameter, please make a copy yourself!
class BruteForcePlayer(Player):
    class Move:
        """ A class representing a move on a given board """
        def __init__(self, key, score=None):
            """ board is the current board situation,
            pos is a tuple of (row, col), where 0 <= row, col <= 2
            player is a character representing the player making the move 'pos'
            symbol2Idx is a hash table converting player's characters to a single index
            score is an optional field, representing the score for the current move
            """
            self.key = key
        @staticmethod
        def hash(board, pos, player, symbol2Idx):
            """ this method returns a (very large) integer according to 'board,' 'pos,' and 'player'
            Rationale for this function: each key has a one-to-one correspondence with each move,
            storing the key reduces memory usage comparing to storing a 2d-list + a tuple + a string,
            the key can also be used as the index of an array storing scores"""
            # for each board position, value = BASE VALUE * PLAYER VALUE
            # board position BASE VALUE
            # 3**0 3**1 3**2
            # 3**3 3**4 3**5
            # 3**6 3**7 3**8
            # PLAYER VALUE
            # None: *0
            # me: *1
            # opponent: *2
            key = 0
            # hash the board positions
            for i, row in enumerate(board):
                for j, symbol in enumerate(row):
                    baseValue = 3**(i*3+j)
                    playerValue = symbol2Idx[symbol]+1 if symbol else 0
                    key += baseValue * playerValue

            # for pos, value = row * 3**9 + col * 3**10
            # hash the pos
            key += pos[0] * 3**9
            key += pos[1] * 3**10

            # for player, value = PLAYER VALUE * 3**11
            # PLAYER VALUE
            # me: *0
            # opponent: *1
            key += symbol2Idx[player] * 3**11
            return key

        @staticmethod
        def unhash(key, playerSymbol=[0,1]):
            """ this method returns a tuple (board, pos, player) from the key representing the move. 
            playerSymbol is an array converting index to the player's symbol, default to 0 and 1 as the symbols
            """
            player = key // 3**11
            player = playerSymbol[player]
            key %= 3**11
            col = key // 3**10
            key %= 3**10
            row = key // 3**9
            key %= 3**9
            pos = (row, col)
            board = [
                    [None, None, None],
                    [None, None, None],
                    [None, None, None]
                    ]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    playerValue = key % 3
                    board[i][j] = None if playerValue==0 else playerSymbol[playerValue-1]
                    key //= 3
            return (board, pos, player)

        @classmethod
        def fromBoardPosPlayer(cls, board, pos, player, symbol2Idx):
            return cls(cls.hash(board,pos,player,symbol2Idx))
        def getKey(self):
            return self.key
        def getBoardPosPlayer(self, playerSymbol=[0,1]):
            return self.unhash(self.key, playerSymbol)
        def setScore(self, score):
            self.score = score
        def getScore(self):
            return self.score
        def getPos(self):
            return self.unhash(self.key)[1]

    def __init__(self, mySymbol, opponentSymbol, useCache=True):
        super().__init__(mySymbol, opponentSymbol)
        # print("Initializing cache")
        if useCache:
            self.scoreCache = [None] * 3**11*2
        else:
            self.scoreCache = None
        # print("Initialized cache")
        self.symbol2Idx = {
                mySymbol: 0,
                opponentSymbol: 1
                }
        # define symbols
        self.playerSymbols = (mySymbol, opponentSymbol)
        # define winning scores
        self.playerWinningScores = (1, -1)

        # define score pickers
        def myScorePicker(scores, ceilingScore=None):
            """ scores is an iterable of 'Move's 
            ceilingScore indicates the maximum score possible, where myScorePicker will return immediately """
            it = scores.__iter__()
            try:
                result = it.__next__()
            except StopIteration:
                # print("Error: Empty scores passed to myScorePicker")
                raise Exception("Stopped for debug")

            if ceilingScore and result.getScore() == ceilingScore:
                # print("Ceiling score found, stop iterating")
                return result
            for i in it:
                if ceilingScore and i.getScore() == ceilingScore:
                    # print("Ceiling score found, stop iterating")
                    return i
                if i.getScore() > result.getScore():
                    result = i
            return result
        def opponentScorePicker(scores, floorScore=None):
            """ scores is an iterable of 'Move's 
            floorScore indicates the minimum score possible, where opponentScorePicker will return immediately """
            it = scores.__iter__()
            try:
                result = it.__next__()
            except StopIteration:
                # print("Empty scores passed to opponentScorePicker")
                raise Exception("Stopped for debug")
            if floorScore and result.getScore() == floorScore:
                # print("Floor score found, stop iterating")
                return result
            for i in it:
                if floorScore and i.getScore() == floorScore:
                    # print("Floor score found, stop iterating")
                    return i
                if i.getScore() < result.getScore():
                    result = i
            return result
        self.playerScorePickers = (myScorePicker, opponentScorePicker)

    def getScore(self, board, pos, playerIdx):
        """ Return 1 if it will win, return 0 if it will tie, return -1 if it will lose """
        if self.scoreCache:
            key = self.Move.hash(board, pos, self.playerSymbols[playerIdx], self.symbol2Idx)
            score = self.scoreCache[key]
            if score:
                # if this move is cached
                # print("Finding cached move score {} for {} on {}, with key {}".format(score, self.playerSymbols[playerIdx], pos, key))
                return score
        newBoard = copy.deepcopy(board)
        newBoard[pos[0]][pos[1]] = self.playerSymbols[playerIdx] # place the move
        winner = getWinner(newBoard)
        # someone won
        if winner:
            score = self.playerWinningScores[self.symbol2Idx[winner]]
            # print("Winning Score at {} for {}: {}".format(pos, winner, score))
            if self.scoreCache:
                # print("Storing winning score for {} on {}, with key {} to cache".format(self.playerSymbols[playerIdx], pos, key))
                self.scoreCache[key] = score
            return score
        # board is full
        if boardFull(newBoard):
            # print("Tie Score at {}".format(pos))
            score = 0
            if self.scoreCache:
                # print("Storing tie score for {} on {}, with key {} to cache".format(self.playerSymbols[playerIdx], pos, key))
                self.scoreCache[key] = score
            return score
        # no one win and board not full
        # return the best one among the next moves according to the opponent score picker
        moves = self.availableMoves(newBoard, not playerIdx)
        bestMove = self.playerScorePickers[not playerIdx](moves, self.playerWinningScores[not playerIdx])
        score = bestMove.getScore()
        # print("Score at {} for {}: {}".format(bestMove.getPos(), self.playerSymbols[not playerIdx], score))
        if self.scoreCache:
            # print("Storing calculated score {} for {} on {}, with key {} to cache".format(score, self.playerSymbols[playerIdx], pos, key))
            self.scoreCache[key] = score
        return score

    def availablePos(self, board):
        """ returns an iterable of 'pos's where moves can be made (with value None) """
        for i in range(len(board)):
            for j in range(len(board[0])):
                if not board[i][j]:
                    # print("i: {}, j: {}".format(i,j))
                    yield (i,j)

    def availableMoves(self, board, playerIdx):
        """ returns an iterable of Moves for the 'board' with scores calculated for player with playerIdx """
        for pos in self.availablePos(board):
            # print("getting available pos {}".format(pos))
            m = self.Move.fromBoardPosPlayer(copy.deepcopy(board), pos, self.playerSymbols[playerIdx], self.symbol2Idx)
            # get the score corresponding to the move
            m.setScore(self.getScore(board, pos, playerIdx))
            # yield the Move object
            yield m

    def makeMove(self, board):
        moves = self.availableMoves(board, 0)
        bestMove = self.playerScorePickers[0](moves, self.playerWinningScores[0])
        return bestMove.getPos()


    def __str__(self):
        return "BruteForce Player"

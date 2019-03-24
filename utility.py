def printBoard(board):
    """ print the board in a moderately nice way """
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

def getWinner(board):
    """ return the character representing the winner in 'board', return None if there is no winner """
# check for row
    for row in board:
        if row[0]: # if first element in row is occupied
            rowEqual = [x == row[0] for x in row[1:]]
            if all(rowEqual): # and if row is all the same
                #print("Row equal:",row)
                return row[0]
# check for col
    for colidx in range(len(board[0])):
        col = [row[colidx] for row in board] # generate a list of the column
        if col[0]: # if first element in col is occupied
            colEqual = [x == col[0] for x in col[1:]]
            if all(colEqual): # and if row is all the same
                #print("Col equal:",col)
                return col[0]
# check for diagonal
    tlbrDiag = [board[i][i] for i in range(len(board))] # tlbr = Top Left Bottom Right
    if tlbrDiag[0]:
        tlbrEqual = [x == tlbrDiag[0] for x in tlbrDiag[1:]]
        if all(tlbrEqual):
            #print("tlbr diag equal:",tlbrDiag,tlbrEqual)
            return tlbrDiag[0]

    trblDiag = [board[len(board)-i-1][i] for i in range(len(board))] # trbl = Top Right Bottom Left
    if trblDiag[0]:
        trblEqual = [x == trblDiag[0] for x in trblDiag[1:]]
        if all(trblEqual):
            #print("trbl diag equal:",trblDiag,trblEqual)
            return trblDiag[0]
    return None

def boardFull(board):
    for row in board:
        for col in row:
            if not col:
                return False
    return True

def countFuncall(f):
    def nf(*args,**kwargs):
        nf.count += 1
        return f(*args,**kwargs)
    nf.count = 0
    return nf

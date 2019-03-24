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


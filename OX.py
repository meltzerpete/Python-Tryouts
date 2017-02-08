board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
turn = 0

def printGrid():
    for i in range(3):
        #print top border
        print(('+' + '-' * 9) * 3 + '+')

        # print top of square
        for j in range(3):
            if board[i * 3 + j] == 1:
                cString = '|' + ' ' * 3 + '/"\\' + ' ' * 3
            elif board[i * 3 + j] == 2:
                cString = '|' + ' ' * 3 + '\\ /' + ' ' * 3
            else:
                cString = '|' + ' ' * 9
            print(cString, end="")
        print("|")

        # print middle of square
        for j in range(3):
            if board[i * 3 + j] == 1:
                cString = '|' + ' ' * 2 + '|   |' + ' ' * 2
            elif board[i * 3 + j] == 2:
                cString = '|' + ' ' * 4 + 'X' + ' ' * 4
            else:
                cString = '|' + ' ' * 4 + str(i * 3 + j) + ' ' * 4
            print(cString, end="")
        print("|")

        # print bottom of square
        for j in range(3):
            if board[i * 3 + j] == 1:
                cString = '|' + ' ' * 3 + '\\_/' + ' ' * 3
            elif board[i * 3 + j] == 2:
                cString = '|' + ' ' * 3 + '/ \\' + ' ' * 3
            else:
                cString = '|' + ' ' * 9
            print(cString, end="")
        print("|")

    # print bottom border
    print(('+' + '-' * 9) * 3 + '+')

def validate(move):
    # check in range of board
    if not (int(move) >= 0 and int(move) < 9):
        return False
    # check space is free
    if board[move] > 0:
        return False
    # all checks have passed
    return True

def checkWinner(lastMove):
    row = lastMove // 3
    col = lastMove % 3

    # check row
    if board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
        return True
    # check col
    if board[col] == board[col + 3] == board[col + 6]:
        return True
    # check diagonals (only if necessary)
    if lastMove % 2 == 0:
        if (board[4] != 0) and (board[0] == board[4] == board[8] or board[2] == board[4] == board[6]):
            return True

    return False

# intro spiel
print("\n\n\nWelcome.. type 'q' to quit")

# gameplay
while True:
    printGrid()
    move = input("Enter a move player " + str(turn + 1) + ": ")

    # check for exit
    if move == "q":
        break

    # handle move
    if validate(int(move)):
        # move is valid - make the move
        board[int(move)] = turn + 1

        # check for a winner
        if checkWinner(int(move)):
            print("\n\n\n")
            printGrid()
            print("Player " + str(turn + 1) + " wins!!!!")
            break

        # check for stalemate
        if 0 not in board:
            print("\n\n\n")
            printGrid()
            print("Nobody wins... ever..")
            break

        print("\n\n\n")
    else:
        print("\n\n\nInvalid move")
        continue

    # change turn
    turn = (turn + 1) % 2

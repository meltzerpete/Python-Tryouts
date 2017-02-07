def printGrid(sizeX, sizeY, squareSize):
    for i in range(sizeY):
        print(('+' + '-' * squareSize) * sizeX + '+')
        for j in range(squareSize):
            print(('|' + ' ' * squareSize) * sizeX + '|')
    print(('+' + '-' * squareSize) * sizeX + '+')

printGrid(8, 2, 3)

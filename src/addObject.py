# adds a object to the pixelArray at the specified grid position

def add(pixelArray: list, addArray: list, gridPosX, gridPosY):
    posX = gridPosX*4+4
    posY = gridPosY*4+4

    for x in range(posX-4, posX):
        for y in range(posY-4, posY):
            if addArray[x-posX][y-posY][0] != 0 or addArray[x-posX][y-posY][1] != 0 or addArray[x-posX][y-posY][2] != 0:
                pixelArray[x][y] = addArray[x-posX][y-posY]
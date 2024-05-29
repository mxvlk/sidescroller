import numpy as np
import random
import math

from .frameBuffer import FrameBuffer
from .map import Map
from .spriteReader import readSprite, setPixelColor
from .sprites import Sprites
from .addObject import add
from .pixel import setPixelColor, setClearPixel

# the player class

class Player():

    def __init__(self, pixelArray):
        self.amogus = readSprite(Sprites.player.value, False)
        self.colorR = random.randrange(100, 255)
        self.colorG = random.randrange(100, 255)
        self.colorB = random.randrange(100, 255)
        self.posX = 0
        self.posY = 0
        self.jumpHeight = 4
        self.velocity = 1
        self.lastWalkDirection = 0
        self.isJumping = False
        self.positioningX = 2
        self.positioningY = 0
        add(pixelArray, self.dimensions(), self.positioningX, self.positioningY)


    # sets the color of the player (randomly choosen in init)

    def setPixelColorSelf(self, pixelArray, x, y):
        setPixelColor(pixelArray, x, y, self.colorR, self.colorG, self.colorB, 1)


    # returns the dimensions of the player in a pixel array
    # (and sets the "eye" of the player)

    def dimensions(self):
        pixelArray = np.full((len(self.amogus), len(self.amogus[0]), 4), 0)
        for x in range(len(pixelArray)):
            for y in range(len(pixelArray[0])):
                if int(self.amogus[x][y]) != 0:
                    pixelArray[x][y] = int(self.amogus[x][y])
                    if int(self.amogus[x][y]) == 2:
                        setPixelColor(pixelArray, x, y, 0, 100, 255, 1)
                        self.posX = (4*self.positioningX+y)-1
                        self.posY = (4*self.positioningY+x)+1
                    else:
                        self.setPixelColorSelf(pixelArray, x, y)
        return pixelArray


    # updates the player velocity according to the last walk direction

    def updateVelocity(self, walkDirection):
        lwd = self.lastWalkDirection # 1=right/2=left
        if self.velocity < 4 and not self.isJumping:
            if lwd == walkDirection or lwd == 0:
                self.velocity +=1
            else:
                self.velocity = 1


    # checks if walking right is possible

    def walkingRightPossible(self, pixelArray):
        if pixelArray[self.posX+2][self.posY+2][3] == 0 and pixelArray[self.posX+1][self.posY+2][3] == 0 and pixelArray[self.posX][self.posY+2][3] == 0 and pixelArray[self.posX-1][self.posY+1][3] == 0:
            return True
        else:
            return False


    # walk right 1 pixel

    def walkRight(self, pixelArray):
        if self.posY < 8:
            if self.walkingRightPossible(pixelArray): 
                self.posY += 1
                self.updateVelocity(1)
                self.lastWalkDirection = 1 # 1=right/2=left
                rng = len(pixelArray)
                for x in range(rng):
                    for y in range(rng):
                        y16 = 15-y
                        if (pixelArray[x][y16][3] == 1):
                            pixelArray[x][y16+1] = pixelArray[x][y16]
                            setClearPixel(pixelArray, x, y16)


    # checks if walking left is possible

    def walkingLeftPossible(self, pixelArray):
        if pixelArray[self.posX+2][self.posY-2][3] == 0 and pixelArray[self.posX+1][self.posY-2][3] == 0 and pixelArray[self.posX][self.posY-2][3] == 0 and pixelArray[self.posX-1][self.posY-1][3] == 0:
            return True
        else:
            return False


    # walk left 1 pixel

    def walkLeft(self, pixelArray):
        print(self.posX, self.posY)
        if self.posY > 2:
            if self.walkingLeftPossible(pixelArray):
                self.posY -= 1
                self.updateVelocity(2)
                self.lastWalkDirection = 2 # 1=right/2=left
                rng = len(pixelArray)
                for x in range(rng):
                    for y in range(rng):
                        if (pixelArray[x][y][3] == 1):
                            pixelArray[x][y-1] = pixelArray[x][y]
                            setClearPixel(pixelArray, x, y)


    # checks if going up is possible

    def goingUpPossible(self, pixelArray):
        if self.posX-2 > 0:
            if pixelArray[self.posX-2][self.posY][3] == 0 and pixelArray[self.posX-2][self.posY-1][3] == 0 and pixelArray[self.posX-2][self.posY+1][3] == 0:
                return True
        else:
            return False


    # shifts the player up 1 pixel

    def shiftPlayerUp(self, pixelArray):
        if self.goingUpPossible(pixelArray):
            rng = len(pixelArray)
            self.posX -= 1
            for x in range(rng):
                for y in range(1, rng):
                    if (pixelArray[x][y][3] == 1 and x > 0):
                        pixelArray[x-1][y] = pixelArray[x][y]
                        setClearPixel(pixelArray, x, y)  


    # checks if going down is possible

    def goingDownPossible(self, pixelArray):
        if self.posX+3<16:
            if pixelArray[self.posX+3][self.posY][3] == 0 and pixelArray[self.posX+3][self.posY-1][3] == 0 and pixelArray[self.posX+3][self.posY+1][3] == 0:
                return True


    # shifts the player down 1 pixel    

    def shiftPlayerDown(self, pixelArray):
        if self.goingDownPossible(pixelArray):
            rng = len(pixelArray)
            self.posX += 1
            for x in range(rng):
                for y in range(rng):
                    x16 = 15-x
                    if (pixelArray[x16][y][3] == 1 and x16 < rng-1):
                        pixelArray[x16+1][y] = pixelArray[x16][y]
                        setClearPixel(pixelArray, x16, y)


    # function that returns the jump x/y values

    def jumpFunc(self, x):
        velocity = (self.velocity**-1)+0.3
        if self.velocity == 3:
            velocity = 3
        return round((-((x*velocity)-math.sqrt(self.jumpHeight))**2)+self.jumpHeight)


    # makes the player jump according to the velocity

    def jump(self, pixelArray: list, frameBuffer: FrameBuffer, map: Map):
        self.isJumping = True
        jumpPosX = 0
        jumpPosY = 0
        oldJumpPosX = jumpPosX
        oldJumpPosY = jumpPosY
        pixelArrayCopy = pixelArray.copy()
        jumpsUp = 0
        jumpsDown = 0
        x = 0
        
        while self.jumpFunc(x) >= 0:
            y = self.jumpFunc(x)
            changed = False
            oldJumpPosY = jumpPosY
            oldJumpPosX = jumpPosX
            jumpPosX = x
            jumpPosY = y

            if oldJumpPosX != jumpPosX:
                if self.posX < 7:
                    self.walkRight(pixelArrayCopy)
                else:
                    if self.walkingRightPossible(pixelArrayCopy):
                        map.moveCameraY(pixelArrayCopy)
                changed = True

            if oldJumpPosY < jumpPosY:
                for jmps in range(jumpPosY-oldJumpPosY):
                    jumpsUp += 1
                    self.shiftPlayerUp(pixelArrayCopy)
                changed = True
            elif oldJumpPosY > jumpPosY:
                for jmps in range(oldJumpPosY-jumpPosY):
                    jumpsDown += 1
                    self.shiftPlayerDown(pixelArrayCopy)
                changed = True
                
            if changed:
                frameBuffer.addFrame(pixelArrayCopy)

            x += 1

        if jumpsDown < jumpsUp:
            for jmps in range(jumpsUp-jumpsDown):
                self.shiftPlayerDown(pixelArrayCopy)
                frameBuffer.addFrame(pixelArrayCopy)

        self.isJumping = False
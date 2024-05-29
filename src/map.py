from .spriteReader import dimensions, readSprite
from .sprites import numberToSprite
from .maps import Maps
from .addObject import add
from .pixel import setClearPixel

# map class

class Map:

    def __init__(self, pixelArray):
        self.map = readSprite(Maps.mario.value, True)
        self.length = int(len(self.map[0])/4)*16
        self.movedPixels = 16
        self.pixelArray = pixelArray
        self.initialMap()


    # adds the map to the pixel array

    def addMapToPixelArray(self, pixelArray, start, end):
        grid = 4 #4x4 grid
        for x in range(grid): 
            for y in range(start, end):
                if(end > len(self.map[0])):
                    break
                yPos = y
                spriteNumber = int(self.map[x][y])
                if spriteNumber != 0:
                    sprite = numberToSprite(spriteNumber)
                    if start > grid:
                        yPos -= grid

                    if yPos > 7:
                        while yPos > 7:
                            yPos = yPos-4

                    add(pixelArray, dimensions(sprite), x, yPos)


    # initialises the map

    def initialMap(self):
        self.addMapToPixelArray(self.pixelArray, 0, 4)

    # loads the map in (outside of the players view)


    def updateMap(self, pixelArray):
        grid = 4
        pixel = 16
        if self.movedPixels % pixel == 0 and self.movedPixels > 0:
            pos = int(self.movedPixels/pixel)*grid
            self.addMapToPixelArray(pixelArray, pos, pos+4)


    # moves the camera in negative y direction

    def moveCameraY(self, pixelArray):
        if self.movedPixels < self.length+8:
            self.updateMap(pixelArray)
            self.movedPixels += 1
            for y in range(1, len(pixelArray[0])):
                for x in range(len(pixelArray)):
                    if pixelArray[x][y-1][3] != 1 and pixelArray[x][y][3] != 1:
                        pixelArray[x][y-1] = pixelArray[x][y]
                    if y == len(pixelArray[0])-1:
                        setClearPixel(pixelArray, x, y) 

    






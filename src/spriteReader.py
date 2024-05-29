from pathlib import Path
from .pixel import setPixelColor

import csv
import numpy as np
import random as rand

# reads a sprite and returns a array of the values

def readSprite(fileName, readMap):
    basePath = Path(__file__).parent
    if(readMap):
        filePath = (basePath / ("../maps/"+fileName)).resolve()
    else:
        filePath = (basePath / ("../sprites/"+fileName)).resolve()
    
    with open(filePath) as file:
        sprite = [line for line in csv.reader(file)]
        return sprite

# sets a random pixel color for the sprite

def setRandomPixelColor(pixelArray, x, y):
    setPixelColor(pixelArray, x, y,  rand.randrange(100, 255),  rand.randrange(100, 255),  rand.randrange(100, 255), 2)


# returns a array of the dimensions of the sprite

def dimensions(fileName):
    pixels = 4
    sprite = readSprite(fileName, False)
    pixelArray = np.full((pixels, pixels, 4), 0)
    for x in range(pixels):
        for y in range(pixels):
            if(int(sprite[x][y]) != 0):
                pixelArray[x][y] = int(sprite[x][y])
                setRandomPixelColor(pixelArray, x, y)
    return pixelArray
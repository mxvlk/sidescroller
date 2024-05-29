from enum import Enum

# sprite enum

class Sprites(Enum):
    player = "player.csv"
    mapStairs = "stairs.csv"
    mapPlatformHigh = "platformHigh.csv"
    mapPlatformLow = "platformLow.csv"


# maps sprites to numbers (used in the map)

def numberToSprite(spriteNumber):
        if spriteNumber == 1:
            return Sprites.mapStairs.value
        elif spriteNumber == 2:
            return Sprites.mapPlatformHigh.value
        elif spriteNumber == 3:
            return Sprites.mapPlatformLow.value
        else:
            return None
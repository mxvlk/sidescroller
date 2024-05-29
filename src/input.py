from enum import Enum
from .map import Map
from .frameBuffer import FrameBuffer
from .player import Player

# enum for the directions

class Directions(Enum):
    left = 1
    right = 2
    down = 3
    up = 4


# maps the input to the direction

def inputToDirection(dir, pixelArray, player: Player, frameBuffer: FrameBuffer, map: Map):
        
    if player.goingDownPossible(pixelArray) and not player.isJumping and not frameBuffer.running:
        player.shiftPlayerDown(pixelArray) # gravity

    if player.posX < 13: # dont walk out of frame

        if dir == Directions.right.value:
            if player.posY < 7:
                    player.walkRight(pixelArray)
            else:
                if player.walkingRightPossible(pixelArray) and player.posX < 10:
                    map.moveCameraY(pixelArray)

        elif dir == Directions.left.value:
            player.walkLeft(pixelArray)

        elif dir == Directions.up.value:
            player.jump(pixelArray, frameBuffer, map)

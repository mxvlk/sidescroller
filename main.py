import numpy as np
from src.frameBuffer import FrameBuffer
from src.player import Player
from src.unicornHead import showUH
from src.pixel import sanatizeArray
from src.input import inputToDirection
from src.map import Map
import time

try: 
    from output_framework.output_framework import OutputFramework       # type: ignore
    from input_framework.imu_controller import IMUController            # type: ignore
    from input_framework.interface import ThresholdType, TriggerMode    # type: ignore
except ImportError:
    # shows error if input/output framework was not found
    print("No import/output framework found!") 


PIXELS = 16
pixelArray = np.full((PIXELS, PIXELS*2, 4), 0)
ROTATION_THRESHOLD = 0.2

def main():

    player = Player(pixelArray)    # create Player
    map = Map(pixelArray)          # create Map
    frameBuffer = FrameBuffer()    # create Frame Buffer erer

    running = True

    try:
        # registers the controller and the movements
        controller = IMUController(TriggerMode.CALL_CHECK)
        controller.register_trigger(inputToDirection, { 'dir' : 1, 'pixelArray': pixelArray, 'player' : player, 'frameBuffer': frameBuffer, 'map': map }, controller.mov_x, ROTATION_THRESHOLD, ThresholdType.HIGHER)
        controller.register_trigger(inputToDirection, { 'dir' : 2, 'pixelArray': pixelArray, 'player' : player, 'frameBuffer': frameBuffer, 'map': map }, controller.mov_x, -ROTATION_THRESHOLD, ThresholdType.LOWER)
        controller.register_trigger(inputToDirection, { 'dir' : 3, 'pixelArray': pixelArray, 'player' : player, 'frameBuffer': frameBuffer, 'map': map }, controller.mov_y, -ROTATION_THRESHOLD, ThresholdType.LOWER)
        controller.register_trigger(inputToDirection, { 'dir' : 4, 'pixelArray': pixelArray, 'player' : player, 'frameBuffer': frameBuffer, 'map': map }, controller.mov_y, ROTATION_THRESHOLD, ThresholdType.HIGHER)
    except NameError:
        # shows error if no controller was found
        print("No controller found!") 

    while running:

        # if posX is 13, the player fell out of the map (in x direction)
        if player.posX == 13:
            running = False   # stop running

        # frameBuffer inital state
        frameBuffer.running = False 

        # check for frames in frameBuffer
        if frameBuffer.length() > 0: 
            frameBuffer.running = True
            # show next frame in pixelArray
            frameBuffer.nextFrame(pixelArray) 

        try:
            # sets the window
            OutputFramework.setWindow(sanatizeArray(pixelArray), 180) 
            if not frameBuffer.running and not player.isJumping:
                # check for player movement
                controller.check_triggers() 
        except NameError:
            # shows gui on pc for local development
            showUH(pixelArray, PIXELS)
        
        # 24 frames per second
        time.sleep(1/24) 

if __name__ == "__main__":
    main()
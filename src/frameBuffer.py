# frame buffer for jumping

class FrameBuffer:

    def __init__(self):
        self.buffer = list()
        self.running = False

    def addFrame(self, pixelArray: list):
        self.buffer.append(pixelArray.copy())

    def removeFrame(self):
        return self.buffer.pop(0)

    def length(self):
        return len(self.buffer)

    def nextFrame(self, pixelArray):
        frame = self.removeFrame()
        for x in range(len(frame)):
            for y in range(len(frame[0])):
                pixelArray[x][y] = frame[x][y]
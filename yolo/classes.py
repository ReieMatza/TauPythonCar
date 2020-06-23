class Detection:
    def __init__(self, coneColor = None, camDistance = None, depthDistance = None, relHeading = None, firstPoint = None, secondPoint = None, camPosition = None, camOrientation = None):
        self.coneColor = coneColor
        self.camDistance = camDistance
        self.depthDistance = depthDistance
        self.relHeading = relHeading
        self.firstPoint = firstPoint
        self.secondPoint = secondPoint
        self.camPosition = camPosition
        self.camOrientation = camOrientation

class zedFrame:
    def __init__(self, image = None, depthMat = None, camOrientation = None, camPosition = None,FPS = None):
        self.image = image
        self.depthMat = depthMat
        self.camOrientation = camOrientation
        self.camPosition = camPosition
        self.FPS = FPS


class outputData:
    def __init__(self, image = None, camOrientation = None, camPosition = None):
        self.image = image
        self.camOrientation = camOrientation
        self.camPosition = camPosition




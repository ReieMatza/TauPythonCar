class Detection:
    def __init__(self, coneColor = None, camDistance = None, depthDistance = None, relHeading = None, firstPoint = None, secondPoint = None, camPosition = None, camOrientation = None, frameID = None):
        self.coneColor = coneColor
        self.camDistance = camDistance
        self.depthDistance = depthDistance
        self.relHeading = relHeading
        self.firstPoint = firstPoint
        self.secondPoint = secondPoint
        self.camPosition = camPosition
        self.camOrientation = camOrientation
        self.frameID = frameID
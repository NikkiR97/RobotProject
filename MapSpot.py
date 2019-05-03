class MapSpot:

    def __init__(self):
        self.detected = False
        self.traveled = False
        self.obstacle = False

    def setDetected(self, detected):
        self.detected = detected

    def getDetected(self):
        return self.detected

    def setTraveled(self, traveled):
        self.traveled = traveled

    def getTraveled(self):
        return self.traveled

    def setObstacle(self, obstacle):
        self.obstacle = obstacle

    def getObstacle(self):
        return self.obstacle
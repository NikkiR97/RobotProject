from MapSpot import MapSpot

class Map:

    def __init__(self):
        self.mapList = list()
        for i in range(100):
            subMap = list()
            for j in range(100):
                subMap.append(MapSpot())
            self.mapList.append(subMap)

    def printMap(self):
        for m in self.mapList:
            for s in m:
                print(str(s.detected), end=" ")
            print(" ")

    def generateMapFrom1Point4BlockStatic(self, positionX, positionY, ultrasonicFD,
                              ultrasonicRD, ultrasonicLD, ultrasonicBD):

        if mapList[positionX][positionY + 1].getDetected() is False:
            mapList[positionX][positionY + 1].setDetected(true)  # front
            if(ultrasonicFD >=30):
                mapList[positionX][positionY + 1].setObstacle(False)
            else:
                mapList[positionX][positionY + 1].setObstacle(True)

        if mapList[positionX + 1][positionY].getDetected() is False:
            mapList[positionX + 1][positionY].setDetected(True)  # right
            if (ultrasonicRD >= 30):
                mapList[positionX + 1][positionY].setObstacle(False)
            else:
                mapList[positionX + 1][positionY].setObstacle(True)

        if mapList[positionX][positionY - 1].getDetected() is False:
            mapList[positionX][positionY - 1].setDetected(True)  # back
            if (ultrasonicBD >= 30):
                mapList[positionX][positionY - 1].setObstacle(False)
            else:
                mapList[positionX][positionY - 1].setObstacle(True)

        if mapList[positionX - 1][positionY].getDetected() is False:
            mapList[positionX - 1][positionY].setDetected(True)  # left
            if (ultrasonicLD >= 30):
                mapList[positionX - 1][positionY].setObstacle(False)
            else:
                mapList[positionX - 1][positionY].setObstacle(True)

    def generateMapFrom1Point4Block(self, positionX, positionY, ultrasonicFD,
                              ultrasonicRD, ultrasonicLD, ultrasonicBD,
                              orientation):
        f = (0, 1) #(x, y)
        r = (1, 0)
        b = (-1, 0)
        l = (0, -1)
        if orientation == "front":
            f = (0, 1)
            r = (1, 0)
            b = (0, -1)
            l = (-1, 0)
        elif orientation == "right":
            l = (0, 1)
            f = (1, 0)
            r = (0, -1)
            b = (-1, 0)
        elif orientation == "back":
            b = (0, 1)
            l = (1, 0)
            f = (0, -1)
            r = (-1, 0)
        elif orientation == "left":
            r = (0, 1)
            b = (1, 0)
            l = (0, -1)
            f = (-1, 0)

        if mapList[positionX + f[0]][positionY + f[1]].getDetected() is False:
            mapList[positionX + f[0]][positionY + f[1]].setDetected(true)  # front
            if(ultrasonicFD >=30):
                mapList[positionX+ f[0]][positionY + f[1]].setObstacle(False)
            else:
                mapList[positionX + f[0]][positionY + + f[1]].setObstacle(True)

        if mapList[positionX + r[0]][positionY + r[1]].getDetected() is False:
            mapList[positionX + r[0]][positionY + r[1]].setDetected(True)  # right
            if (ultrasonicRD >= 30):
                mapList[positionX + r[0]][positionY + r[1]].setObstacle(False)
            else:
                mapList[positionX + r[0]][positionY + r[1]].setObstacle(True)

        if mapList[positionX + b[0]][positionY  + b[1]].getDetected() is False:
            mapList[positionX  + b[0]][positionY  + b[1]].setDetected(True)  # back
            if (ultrasonicBD >= 30):
                mapList[positionX + b[0]][positionY + b[1]].setObstacle(False)
            else:
                mapList[positionX + b[0]][positionY + b[1]].setObstacle(True)

        if mapList[positionX + l[0]][positionY + l[1]].getDetected() is False:
            mapList[positionX + l[0]][positionY + l[1]].setDetected(True)  # left
            if (ultrasonicLD >= 30):
                mapList[positionX + l[0]][positionY + l[1]].setObstacle(False)
            else:
                mapList[positionX + l[0]][positionY + l[1]].setObstacle(True)

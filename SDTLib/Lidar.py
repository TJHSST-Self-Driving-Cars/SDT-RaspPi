import os
import math
import threading
from adafruit_rplidar import RPLidar

# TODO 
# once we get an imu, start updating the relative positions to be absolute positions in space where 0,0 is the position the car started at
# add in a set of all of the points that have been hit by the lidar ever to start to create a map of the environment

class Lidar:

    _PORT_NAME = None
    _lidar = None

    # controls whether the lidar is on or off
    _lidarStopped = False

    _scan_thread = None


    # maps all of the lidar angles to a distance away from the lidar
    data = dict()

    # contains all of the positions that the lidar hit as a list of 2d points
    relativePositions = []

    # refers to the lidar's current angle of orientation; useful for error correction
    curAngle = 0


    def __init__(self, portname):
        # Setup the RPLidar
        self._PORT_NAME = portname
        self._lidar = RPLidar(None, self._PORT_NAME)
        

        # Setup the threading system
        self._scan_thread = threading.Thread(target=self._startScan, name="lidar scan")

        # initialize the data to an empty dictionary
        self.data = {angle: 0 for angle in range(360)}

        # intialize the relativePositions to an empty list of tuples
        self.relativePositions = [() for angle in range(360)]


    # helper method for _startScan()
    def _processData(self, angle: int) -> None:
        distance = self.data[angle]

        # math's functions only take in radians and not degrees
        radianAngle = angle * math.pi / 180.0

        # calculate the x, y relative positions of the data from the car
        x = distance * math.cos(radianAngle)
        y = distance * math.sin(radianAngle)

        self.relativePositions[angle] = (x, y)

    #helper method for start()
    def _startScan(self) -> None:

        # go through every data point and note its angle and distance pair
        # then, we can do some calculations with it and save it to data and relativePositions
        for scan in self._lidar.iter_scans():
            if self._lidarStopped == False:
                for (_, angle, distance) in scan:
                    self.curAngle = angle
                    self.data[min([359, math.floor(angle)])] = distance
                    self._processData(min([359, math.floor(angle)]))
                    
            else: break

        # stops the lidar if the boolean _lidarStopped is True
        self._lidar.stop()
        self._lidar.disconnect()

    def start(self) -> None:
        # resets this boolean to notify all other members of this class that that the lidar is moving
        self._lidarStopped = False
        
        # start scanning if you aren't already
        if not self._scan_thread.is_alive():
            self._scan_thread.start()



    def stop(self) -> None:
        self._lidarStopped = True


if __name__ == "__main__":
    portname = "/dev/serial0"
    lidar = Lidar(portname)
    lidar.start()
    print(lidar.data)
    


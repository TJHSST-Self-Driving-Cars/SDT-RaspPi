import os
from math import floor, pi
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt

PORT_NAME = '/dev/serial0'
lidar = RPLidar(None, PORT_NAME, baudrate=115200, timeout=3)
print(lidar)
max_distance = 3

def plot_hc():
    def process_data(data):
        print(max(data), min(data), data.count(0))

    scan_data = [0] * 360

    radians = [i * pi / 180 for i in range(360)]

    latestscan = {} # angle, distance

    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    # ax = fig.add_subplot()
    i = 0
    try:
        print(lidar.info)
        for scan in lidar.iter_scans(min_len=100, max_buf_meas=5000):
            latestscan = {}
            for (_, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance/1000
                latestscan[angle] = distance
            print(len(latestscan))
            # if i % 4 == 0:
            process_data(scan_data)
            ax.cla()
            ax.set_ylim([0,5])
            # c = ax.scatter(radians, scan_data, cmap='hsv', alpha=0.75, s=[1 for i in range(360)])
            c = ax.scatter(latestscan.keys(), latestscan.values(), cmap='hsv', alpha=0.75, s=[1 for i in range(len(latestscan))])
            # ax.hist(scan_data, bins=360)
            plt.pause(1)
            i += 1
    except KeyboardInterrupt:
        print("Stopping")
        lidar.stop()
        lidar.disconnect()

def plot_measurements():
    # plots using iter_measurements instead!
    pass

if __name__ == "__main__":
    plot_hc()

plt.show()
lidar.stop()
lidar.disconnect()

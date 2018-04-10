from string import ascii_lowercase
import time
from numpy import median

WRITE_PATH = "/home/alexanga/Projects/SpeedTest/data/write_storage"

data_storage = open(WRITE_PATH, "w", 0)
speed = []

for j in range(0, 100):
    time_start = time.time()
    for i in range(0, 60000):
        inp = ascii_lowercase * 50 # 1300 bytes
        data_storage.write(inp)
        # Write in this loop: 78 MB

    total_time = time.time() - time_start
    speed.append(78 / total_time)
    print "Speed", 78 / total_time, "MB/s"

data_storage.close()

avg_speed = sum(speed) / 100
print "Average speed:", avg_speed, "MB/s"
print "Median speed:", median(speed), "MB/s"

# Total write: 7800 MB

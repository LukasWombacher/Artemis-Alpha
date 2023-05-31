import time
import json
import os
from mpu9250_i2c import *

time.sleep(1)

time.sleep(1) # delay necessary to allow mpu9250 to settle
counter = {"round": 0, "sum_x": 0, "sum_y": 0, "sum_z": 0}
start = time.time()
end = start

while (end-start < 10):
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        
    except:
        continue
    counter["round"] += 1
    counter["sum_x"] += wx
    counter["sum_y"] += wy
    counter["sum_z"] += wz
    end = time.time()

drift_x = counter["sum_x"] / counter["round"]
drift_y = counter["sum_y"] / counter["round"]
drift_z = counter["sum_z"] / counter["round"]


def new_func(settings_file):
    return settings_file

with open("/home/pi/Artemis-Alpha/Code/settings.json", "r") as settings_file:
    settings_data = json.load(new_func(settings_file))
    settings_data["gyroscope_drift"]["x"] = drift_x
    settings_data["gyroscope_drift"]["y"] = drift_y
    settings_data["gyroscope_drift"]["z"] = drift_z
os.remove("/home/pi/Artemis-Alpha/Code/settings.json")
with open("/home/pi/Artemis-Alpha/Code/settings.json", "w") as new_settings_file:
    json.dump(settings_data, new_settings_file, indent=4)

time.sleep(1)
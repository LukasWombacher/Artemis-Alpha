import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import json
import time
from mpu9250_i2c import *
from threading import Thread
time.sleep(1) # delay necessary to allow mpu9250 to settle

with open("/home/pi/Artemis-Alpha/Code/settings.json", "r") as settings_file:
    settings_data = json.load(settings_file)
    bias_x = settings_data["gyroscope_drift"]["x"]
    bias_y = settings_data["gyroscope_drift"]["y"]
    bias_z = settings_data["gyroscope_drift"]["z"]

counter = {"round": 0, "sum_x": 0, "sum_y": 0, "sum_z": 0}
recording = True
stop_recording = False
start = 0
end = 0
wz = 1

def record_degree():
    while True:
        global counter, wz, start, recording, stop_recording
        counter = {"round": 0, "sum_x": 0, "sum_y": 0, "sum_z": 0}
        start = time.time()
        while recording:
            try:
                ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
                wz -= bias_z
                #if -0.3 < wz < 0.3:
                #    wz = 0
                    
            except:
                continue
            counter["round"] += 1
            counter["sum_z"] += wz
            time.sleep(0.04)
        stop_recording = True

def get_abs_degree():
    end = time.time()
    global start, counter, degree_z
    if counter["round"] != 0:
        degree_z = (counter["sum_z"] / counter["round"]) * (end - start)
    else:
        degree_z = 0
    return degree_z

def get_current_dps():
    print('gyro [dps]: z = ' + str(wz))
    return wz

def restart():
    global stop_recording, recording
    recording = False
    while not(stop_recording):
        time.sleep(0.01)
    stop_recording = False
    recording = True


def test():
    while True:
        print(get_abs_degree())
    

#thread_1 = Thread(target=record_degree)
#thread_2 = Thread(target=test)
#thread_1.start()
#thread_2.start()

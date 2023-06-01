import time
import ultrasonic
print("start")
while True:
    print(ultrasonic.get_distance("ultrasonic_front"))
    time.sleep(0.3)
"""
import time, ultrasonic, gyroscope
from threading import Thread
direction = 2
d_switch = ["left", "right", "error"]
curve_count = 0
running = True
true_count_bigger = [0, 0, 0, 0, 0, 0, 0, 0]
true_count_smaler = [0, 0, 0, 0, 0, 0, 0, 0]
distance_left = [0]*8
distance_right = [0]*8
curve_goal = 4*1

def get_start_direction():
    while True:
        distance = 150
        len = 8
        pos = 0
        while direction == 2:
            time.sleep(0.1)
            distance_left[pos % len], distance_right[pos % len] = 20, ultrasonic.get_distance("ultrasonic_right") #ultrasonic.get_distance("ultrasonic_left")
            pos += 1
            if pos >= len:
                left_big = 0
                right_big = 0
                for i in distance_left:
                    if 150 < i < 400:
                        left_big += 1
                for i in distance_right:
                    if 150 < i < 400:
                        right_big += 1
                print(left_big, right_big)
            print(distance_right)
            print(distance_left)
            
            
thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=get_start_direction)

thread_1.start()
thread_2.start()
"""
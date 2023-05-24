import time
import ultrasonic
print("start")
while True:
    print(ultrasonic.get_distance("ultrasonic_left", 3))
    time.sleep(0.2)
    
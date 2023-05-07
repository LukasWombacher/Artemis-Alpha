import ultrasonic
import time
kp = 0
#while True:
#    print(ultrasonic.get_distance("ultrasonic_right"))
#    time.sleep(0.1)

def neu():
    global kp
    kp += 1
    print(kp)

neu()
neu()
neu()
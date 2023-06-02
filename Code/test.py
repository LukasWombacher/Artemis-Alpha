import time, ultrasonic, gyroscope
from threading import Thread


def main():
    print("start")
    while True:
        print(ultrasonic.get_distance("ultrasonic_left"))
        #time.sleep(0.3)
            
thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=main)

thread_1.start()
thread_2.start()

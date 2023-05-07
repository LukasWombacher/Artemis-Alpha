import stepper_motor
import ultrasonic
import drive_motor
import time
import gyroscope
from threading import Thread

direction = 2
d_switch = ["left", "right", "error"]
curve_count = 0
running = True
true_count_bigger = [0, 0, 0, 0, 0, 0, 0, 0]
true_count_smaler = [0, 0, 0, 0, 0, 0, 0, 0]
curve_goal = 4

def ultrasonic_savety_bigger(sensor, distance, num=0):
    global true_count_bigger
    if ultrasonic.get_distance(sensor) > distance:
        true_count_bigger[num] += 1
    else:
        true_count_bigger[num] = 0
    if true_count_bigger[num] >= 3:
        true_count_bigger[num] = 0
        return True
    else:
        return False

def ultrasonic_savety_smaler(sensor, distance, num=0):
    global true_count_smaler
    if ultrasonic.get_distance(sensor) < distance:
        true_count_smaler[num] += 1
    else:
        true_count_smaler[num] = 0
    if true_count_smaler[num] >= 3:
        true_count_smaler[num] = 0
        return True
    else:
        return False

def accurate():
    global curve_count, direction
    temp_deg = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))*0.25
    lenk = (abs(temp_deg))
    if temp_deg < -1:
        stepper_motor.turn_distance(100, lenk, "left")
        stepper_motor.turn_distance(100, lenk, "right")
    elif temp_deg > 1:
        stepper_motor.turn_distance(100, lenk, "right")
        stepper_motor.turn_distance(100, lenk, "left")

def curve():
    global direction, d_switch, curve_count
    print("Kurve")
    curve_count += 1
    """
    drive_motor.speed = 0
    stepper_motor.turn_distance(100, 45, d_switch[direction])
    drive_motor.speed = 100
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 90:
        time.sleep(0.01)
    drive_motor.speed = 0
    stepper_motor.turn_distance(100, 45, d_switch[not direction])
    drive_motor.speed = 100"""

    i = 0
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 45:
        stepper_motor.turn_distance(100, 1, d_switch[direction])
        i += 1
    for j in range(0, i):
        stepper_motor.turn_distance(100, 1, d_switch[not direction])
    print("lenk fertig")

def main():
    global direction, d_switch, curve_count, running, curve_goal
    gyroscope.restart()
    drive_motor.speed = 100
    print("start")
    while direction == 2:
        if ultrasonic_savety_bigger("ultrasonic_left", 200, 0):
            direction = 0
        elif ultrasonic_savety_bigger("ultrasonic_right", 200, 1):
            direction = 1
    print(d_switch[direction])
    while running:
        while (not ultrasonic_savety_smaler("ultrasonic_front", 100, 0)) or (not ultrasonic_savety_bigger("ultrasonic_"+d_switch[direction], 200, 2)):
            time.sleep(0.001)
            #accurate()
        curve()
        if curve_count >= curve_goal:
            while not ultrasonic_savety_smaler("ultrasonic_front", 150, 1):
                time.sleep(0.1)
            drive_motor.speed = 0
            running = False

    import reset
    print("ENDE")


def main2():
    gyroscope.restart()
    print("Ready")
    #time.sleep(3)
    drive_motor.speed = 100
    while True:
        accurate()

thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=main)
thread_3 = Thread(target=drive_motor.on)

#thread_1.start()
#thread_2.start()
#thread_3.start()
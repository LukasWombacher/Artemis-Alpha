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
distance_left = [0]*8
distance_right = [0]*8
distance_front = [0]*8
distance_side = [0]*8
next_len = 8
next_pos = 0
curve_goal = 4*3
correction_degree = 4

def get_start_direction(distance):
    global direction, distance_left, distance_right, correction_degree
    len = 8
    pos = 0
    while direction == 2:
        time.sleep(0.1)
        distance_left[pos % len], distance_right[pos % len] = ultrasonic.get_distance("ultrasonic_left"), ultrasonic.get_distance("ultrasonic_right")
        pos += 1
        if pos >= len:
            left_big = 0
            right_big = 0
            for i in distance_left:
                if distance < i < 500:
                    left_big += 1
            for i in distance_right:
                if distance < i < 500:
                    right_big += 1
            print(left_big, right_big)
            if left_big >= 4:
                direction = 0
            if right_big >= 4:
                direction = 1
                correction_degree *= -1
        print(distance_left)
        print(distance_right)
                
def is_next_curve(opt_front_distance):
    global direction, d_switch, distance_front, distance_side, next_len, next_pos
    distance_front[next_pos % next_len], distance_side[next_pos % next_len] = ultrasonic.get_distance("ultrasonic_front"), ultrasonic.get_distance("ultrasonic_" + d_switch[direction])
    next_pos += 1
    if next_pos >= next_len:
        next_front_smal = 0
        next_side_big = 0
        for i in distance_front:
            if 0 < i < opt_front_distance:
                next_front_smal += 1
        for i in distance_side:
            if 100 < i < 1000:
                next_side_big += 1
        print(distance_side)
        print(next_side_big, next_front_smal)
        if next_front_smal >= 5 and next_side_big >= 5:
            return True
        else:
            return False
    return False
    
    
def ultrasonic_savety_bigger(sensor, distance, num):
    global true_count_bigger
    if ultrasonic.get_distance(sensor) >= distance:
        true_count_bigger[num] += 1
    else:
        true_count_bigger[num] = 0
    if true_count_bigger[num] >= 3:
        true_count_bigger[num] = 0
        print("save bigger")
        return True
    else:
        return False

def ultrasonic_savety_smaler(sensor, distance, num):
    global true_count_smaler
    a = ultrasonic.get_distance(sensor)
    print(a)
    if a <= distance:
        true_count_smaler[num] += 1
    else:
        true_count_smaler[num] = 0
    if true_count_smaler[num] >= 3:
        true_count_smaler[num] = 0
        print("save smaler")
        return True
    else:
        return False

Kp = 0.04  # Proportionalitätskonstante
Ki = 0.015  # Integral-Konstante
Kd = 0  # Differential-Konstante
prev_error = 0  # vorheriger Fehler
integral = 0  # Summe der Fehler über die Zeit

def pid_reset():
    Kp = 0.04  # Proportionalitätskonstante
    Ki = 0.015  # Integral-Konstante
    Kd = 0  # Differential-Konstante
    prev_error = 0  # vorheriger Fehler
    integral = 0  # Summe der Fehler über die Zeit

def accurate():
    global curve_count, direction, d_switch, correction_degree
    lenk = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)-correction_degree))
    lenk_faktor = 1
    print(lenk*lenk_faktor)
    lenk_direction = "right" if lenk > 0 else "left"
    anti_lenk_direction = "left" if lenk > 0 else "right"
    stepper_motor.turn_distance(50, round(abs(lenk*lenk_faktor)), lenk_direction)
    stepper_motor.turn_distance(50, round(abs(lenk*lenk_faktor)), anti_lenk_direction)

def curve():
    global direction, d_switch, curve_count, correction_degree
    print("Kurve" + str(curve_count))
    curve_count += 1
    stepper_motor.turn_distance(100, 50, d_switch[direction])
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)-correction_degree) < 77:
        time.sleep(0.001)
    stepper_motor.turn_distance(100, 50, d_switch[not direction])
    """i = 0
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 40:
        stepper_motor.turn_distance(100, 1, d_switch[direction])
        i += 1
    for j in range(0, i):
        stepper_motor.turn_distance(100, 1, d_switch[not direction])"""
    print("lenk fertig")

def main():
    global direction, d_switch, curve_count, running, curve_goal, distance_side, distance_front
    gyroscope.restart()
    drive_motor.speed = 20
    print("start")
    get_start_direction(150)
    print(d_switch[direction])
    while not is_next_curve(80):
        time.sleep(0.01)
    drive_motor.speed = 35
    curve()
    drive_motor.speed = 20
    while running:
        distance_front, distance_side = [0]*8, [0]*8
        while not is_next_curve(110):
            accurate()
            time.sleep(0.01)
        print("Korrektur Ende")
        while not is_next_curve(80):
            time.sleep(0.01)
        drive_motor.speed = 35
        curve()
        drive_motor.speed = 20
        if curve_count >= curve_goal:
            while not ultrasonic_savety_smaler("ultrasonic_front", 150, 2):
                accurate()
                time.sleep(0.01)
            drive_motor.speed = 0
            running = False

    import reset
    print("ENDE")



thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=main)
thread_3 = Thread(target=drive_motor.on)

thread_1.start()
thread_2.start()
thread_3.start()
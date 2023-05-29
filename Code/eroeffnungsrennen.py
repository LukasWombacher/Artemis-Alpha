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
curve_goal = 4*1

def get_start_direction(distance):
    global direction, distance_left, distance_right
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
        print(distance_left)
        print(distance_right)
                
                
    
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
    global curve_count, direction, d_switch, Kp, Ki, Kd, prev_error, integral
    lenk = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))
    print(lenk*0.15)
    lenk_direction = "right" if lenk > 0 else "left"
    stepper_motor.turn_distance(50, round(abs(lenk*0.15)), lenk_direction)
    """lenk = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))
    error = lenk  # aktueller Fehler
    derivative = error - prev_error  # Ableitung des Fehlers
    integral = integral*0.5 + error  # Summe der Fehler aktualisieren
    prev_error = error  # vorherigen Fehler aktualisieren
    correction = Kp * error + Ki * integral + Kd * derivative  # Korrekturwert berechnen
    pid_direction = "right" if correction > 0 else "left"  # Richtung basierend auf der Korrektur wählen
    stepper_motor.turn_distance(45, abs(correction), pid_direction)  # Ansteuerung des Lenkmotors"""

def curve():
    global direction, d_switch, curve_count
    print("Kurve")
    curve_count += 1
    stepper_motor.turn_distance(100, 50, d_switch[direction])
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 75:
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
    global direction, d_switch, curve_count, running, curve_goal
    gyroscope.restart()
    drive_motor.speed = 20
    print("start")
    get_start_direction(150)
    print(d_switch[direction])
    curve()
    #drive_motor.speed = 0
    #time.sleep(1000000)
    while running:
        pid_reset()
        while (not ultrasonic_savety_smaler("ultrasonic_front", 100, 4)) and (not ultrasonic_savety_bigger("ultrasonic_"+d_switch[direction], 200, 2)):
            accurate()
            time.sleep(0.01)
        print("Korrektur Ende")
        while (not ultrasonic_savety_smaler("ultrasonic_"+d_switch[direction], 200, 3)): #(not ultrasonic_savety_smaler("ultrasonic_front", 50, 1)) or 
            time.sleep(0.01)
        curve()
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
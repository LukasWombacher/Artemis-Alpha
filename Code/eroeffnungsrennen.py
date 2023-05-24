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
                if 150 < i < 400:
                    left_big += 1
            for i in distance_right:
                if 150 < i < 400:
                    right_big += 1
            print(left_big, right_big)
        print(distance_right)
                
                
    
def ultrasonic_savety_bigger(sensor, distance, num):
    global true_count_bigger
    a = ultrasonic.get_distance(sensor)
    print(sensor, distance, num, a)
    if a >= distance:
        true_count_bigger[num] += 1
    else:
        true_count_bigger[num] = 0
    if true_count_bigger[num] >= 3:
        true_count_bigger[num] = 0
        return True
    else:
        return False

def ultrasonic_savety_smaler(sensor, distance, num):
    global true_count_smaler
    if ultrasonic.get_distance(sensor) <= distance:
        true_count_smaler[num] += 1
    else:
        true_count_smaler[num] = 0
    if true_count_smaler[num] >= 3:
        true_count_smaler[num] = 0
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
    global curve_count, direction, Kp, Ki, Kd, prev_error, integral
    print("PID start")
    lenk = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))
    error = lenk  # aktueller Fehler
    derivative = error - prev_error  # Ableitung des Fehlers
    integral = integral*0.5 + error  # Summe der Fehler aktualisieren
    prev_error = error  # vorherigen Fehler aktualisieren
    correction = Kp * error + Ki * integral + Kd * derivative  # Korrekturwert berechnen
    pid_direction = "right" if correction > 0 else "left"  # Richtung basierend auf der Korrektur wählen
    stepper_motor.turn_distance(45, abs(correction), pid_direction)  # Ansteuerung des Lenkmotors
    print("PID end")

def curve():
    global direction, d_switch, curve_count
    print("Kurve")
    curve_count += 1
    i = 0
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 45:
        stepper_motor.turn_distance(100, 1, d_switch[direction])
        i += 1
    for j in range(0, i):
        stepper_motor.turn_distance(100, 1, d_switch[not direction])
    print("lenk fertig")

def main():
    global direction, d_switch, curve_count, running, curve_goal
    #gyroscope.restart()
    #drive_motor.speed = 75
    print("start")
    get_start_direction(150)
    print(d_switch[direction])
        #print(ultrasonic.get_distance("ultrasonic_rigt"))
    curve()
    while running:
        pid_reset()
        #while (not ultrasonic_savety_smaler("ultrasonic_front", 150, 0)) or (not ultrasonic_savety_bigger("ultrasonic_"+d_switch[direction], 200, 2)):
            #accurate()
        while (not ultrasonic_savety_smaler("ultrasonic_front", 50, 1)) or (not ultrasonic_savety_bigger("ultrasonic_"+d_switch[direction], 200, 3)):
            time.sleep(0.01)
        curve()
        if curve_count >= curve_goal:
            while not ultrasonic_savety_smaler("ultrasonic_front", 150, 2):
                accurate()
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
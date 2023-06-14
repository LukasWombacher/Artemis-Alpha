import stepper_motor
import ultrasonic
import drive_motor
import time
import gyroscope
from threading import Thread
import edit_json
#import display
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)

pins_rotary_encoder = edit_json.get_pin_ports("rotary_encoder")
sw_Pin = pins_rotary_encoder[0]
dt_Pin = pins_rotary_encoder[1]
clk_Pin = pins_rotary_encoder[2]
GPIO.setup(dt_Pin, GPIO.IN)
GPIO.setup(clk_Pin, GPIO.IN)
GPIO.setup(sw_Pin, GPIO.IN)
last_status = (GPIO.input(dt_Pin) << 2) | (GPIO.input(clk_Pin) << 1) | GPIO.input(sw_Pin)
encoder_val = 0
encoder_pressed = False


def rotary_Change(wait_time):
    global last_status, encoder_val, encoder_pressed
    new_status = (GPIO.input(dt_Pin) << 2) | (GPIO.input(clk_Pin) << 1) | GPIO.input(sw_Pin)
    if new_status == last_status:
        return
    if new_status == 5:
        encoder_val += 1
    elif new_status == 3:
        encoder_val -= 1
    elif new_status == 6:
        encoder_pressed = True
    else:
        encoder_pressed = False
    last_status = new_status
    time.sleep(wait_time)

"""
setzt alle wichtigen Konstanten und Variabeln
"""

direction = 2
d_switch = ["left", "right", "error"]
curve_count = 0
running = True
true_count_smaler = [0, 0]
distance_left = [0]*2
distance_right = [0]*2
distance_front = [0]*2
distance_side = [0]*2
next_len = 2
next_pos = 0
curve_goal = 4*3
v_kurve = 100
v_gerade = 100
v_start = v_gerade
last_curve_timer = time.time()

"""
überprüft in welche Richtung das Auto ausgerichtet ist und ob in oder gegen den Uhrzeigersinn gefahren wird
"""

def get_start_direction(distance):
    global direction, distance_left, distance_right
    len = 2
    pos = 0
    while direction == 2:
        #time.sleep(0.1)
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
            if left_big >= 2:
                direction = 0
            if right_big >= 2:
                direction = 1
        print(distance_left)
        print(distance_right)

"""
prüft ob die nächste Kurve gefahren werden kann
"""
      
def is_next_curve(opt_front_distance):
    global direction, d_switch, distance_front, distance_side, next_len, next_pos
    """distance_front[next_pos % next_len], distance_side[next_pos % next_len] = ultrasonic.get_distance("ultrasonic_front"), ultrasonic.get_distance("ultrasonic_" + d_switch[direction])
    next_pos += 1
    if next_pos >= next_len:
        next_front_smal = 0
        next_side_big = 0
        for i in distance_front:
            if 0 < i < opt_front_distance:
                next_front_smal += 1
        for i in distance_side:
            if 120 < i < 1000:
                next_side_big += 1
        print(distance_side)
        print(next_side_big, next_front_smal)
        if next_front_smal >= 2 and next_side_big >= 2:
            return True
        else:
            return False
    return False"""
    a = ultrasonic.get_distance("ultrasonic_front")
    if (0 < a < opt_front_distance) and (120 < ultrasonic.get_distance("ultrasonic_" + d_switch[direction]) < 1000):
        return True
    else:
        return False
    
"""
überprüft ob die letzten 3 Messungen eines Ultraschallsensors über dem Schwellwert lagen, um nicht von Fehlerwerten beeinflusst zu werden
"""

def ultrasonic_savety_smaler(sensor, distance, num):
    global true_count_smaler
    for savety_smaler_count in range(0, 2):
        a = ultrasonic.get_distance(sensor)
        print(a)
        if a <= distance:
            true_count_smaler[num] += 1
        else:
            true_count_smaler[num] = 0
        time.sleep(0.01)
    if true_count_smaler[num] >= 2:
        true_count_smaler[num] = 0
        print("save smaler")
        return True
    else:
        return False

"""
stellt sicher das in den geraden ABschnitten geradeaus gefahren wird und korigiert falls schief oder gegen eine Wand gesteuert wird
"""
def side_lenk(lenk, lenk_direction, anti_lenk_direction, side_lenk_speed):
    stepper_motor.turn_distance(60, round(abs(lenk)), lenk_direction)
    time.sleep(side_lenk_speed)
    stepper_motor.turn_distance(100, round(abs(lenk)), anti_lenk_direction)

def accurate():
    global curve_count, direction, d_switch
    side_lenk_distance_close = 12
    lenk_close = 26
    side_lenk_speed_close = 0.4
    if (ultrasonic.get_distance("ultrasonic_left") + ultrasonic.get_distance("ultrasonic_right")) <= 70:
        side_lenk_distance = 18
        lenk = 22
        side_lenk_speed = 0.35
    else:
        side_lenk_distance = 26
        lenk = 26
        side_lenk_speed = 0.4
    if ultrasonic.get_distance("ultrasonic_left") <= side_lenk_distance_close:
        lenk_direction, anti_lenk_direction = "right", "left"
        print("wand links close")
        side_lenk(lenk_close, lenk_direction, anti_lenk_direction, side_lenk_speed_close)
    elif ultrasonic.get_distance("ultrasonic_left") <= side_lenk_distance:
        lenk_direction, anti_lenk_direction = "right", "left"
        print("wand links")
        side_lenk(lenk, lenk_direction, anti_lenk_direction, side_lenk_speed)
    elif ultrasonic.get_distance("ultrasonic_right") <= side_lenk_distance_close:
        lenk_direction, anti_lenk_direction = "left", "right"
        print("wand rechts close")
        side_lenk(lenk_close, lenk_direction, anti_lenk_direction, side_lenk_speed_close)
    elif ultrasonic.get_distance("ultrasonic_right") <= side_lenk_distance:
        lenk_direction, anti_lenk_direction = "left", "right" 
        print("wand rechts")
        side_lenk(lenk, lenk_direction, anti_lenk_direction, side_lenk_speed)
    else:
        lenk = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))
        lenk_faktor = 0.5
        lenk *= lenk_faktor
        if lenk > 50: lenk = 50
        print(lenk)
        lenk_direction = "right" if lenk > 0 else "left"
        anti_lenk_direction = "left" if lenk > 0 else "right"
        stepper_motor.turn_distance(60, round(abs(lenk)), lenk_direction)
        stepper_motor.turn_distance(60, round(abs(lenk)), anti_lenk_direction)

"""
fährt eine 90° Kurve
"""

def curve():
    global direction, d_switch, curve_count, last_curve_timer
    curve_count += 1
    print("Kurve " + str(curve_count))
    stepper_motor.turn_distance(100, 50, d_switch[direction])
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 65:
        time.sleep(0.001)
    stepper_motor.turn_distance(100, 50, d_switch[not direction])
    print("lenk fertig")
    last_curve_timer = time.time()

"""
Main ist die Hauptroutine des Programms die standardmäßig ausgeführt wird und die die anderen Funktionen aufruft und koordiniert.
"""

def main():
    global direction, d_switch, curve_count, running, curve_goal, distance_side, distance_front
    print("start 1")
    """while not encoder_pressed:
        rotary_Change(0.1)
    display.icon("icon_settings.png")
    time.sleep(1)
    gyroscope.restart()
    time.sleep(0.5)
    display.icon("icon_programs.png")
    while not encoder_pressed:
        rotary_Change(0.1)
    display.logo("Artemis_Alpha.png")
    time.sleep(1)"""
    gyroscope.restart()
    drive_motor.speed = v_start
    print("start")
    get_start_direction(150)
    print(d_switch[direction])
    drive_motor.speed = v_gerade
    while not is_next_curve(60):
        time.sleep(0.01)
    drive_motor.speed = v_kurve
    curve()
    drive_motor.speed = v_gerade
    while running:
        distance_front, distance_side = [0]*3, [0]*3
        while not is_next_curve(60) or ((time.time() - last_curve_timer) < 5):
            accurate()
            time.sleep(0.01)
        drive_motor.speed = v_kurve
        curve()
        drive_motor.speed = v_gerade
        if curve_count >= curve_goal:
            while not ultrasonic_savety_smaler("ultrasonic_front", 150, 1):
                accurate()
                time.sleep(0.01)
            drive_motor.speed = 0
            running = False

    import reset
    print("ENDE")

"""
es werden Threads gestartet um mehrere Messungen und Abläufe in Echtzeit parallel ausführen zu können
"""

thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=main)
thread_3 = Thread(target=drive_motor.on)

thread_1.start()
thread_2.start()
thread_3.start()
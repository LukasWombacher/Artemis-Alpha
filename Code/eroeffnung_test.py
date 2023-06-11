import stepper_motor
import ultrasonic
import drive_motor
import time
from threading import Thread
import edit_json
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
v_kurve = 60
v_gerade = 100
v_start = 50

left = 50
right= 50
front = 100

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
      
def is_next_curve():
    global direction, d_switch, distance_front, distance_side, next_len, next_pos
    curve_front_distance = 60

    a = ultrasonic.get_distance("ultrasonic_front")
    print(a)
    if (0 < a < curve_front_distance) and (120 < ultrasonic.get_distance("ultrasonic_" + d_switch[direction]) < 1000):
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
    global left, right, front
    if left < 90 and right < 90:
        correction = ""
        correct_angle = 12
        tolerance = 3
        ## geradenkorrektur
        if right - left > tolerance:
            correction = "right"
            correct_back = "left"
        if left - right > tolerance:
            correction = "left"
            correct_back = "right"
        if correction != "":
            print("korrektur:" + correction)
            stepper_motor.turn_distance(100, correct_angle, correction) 
            time.sleep(0.1)
            stepper_motor.turn_distance(100, correct_angle, correct_back) 

"""
fährt eine 90° Kurve
"""

def curve():
    global direction, d_switch, curve_count
    curve_count += 1
    print("Kurve " + str(curve_count))

    stepper_motor.turn_distance(100, 45, d_switch[direction])
    time.sleep(1.3)
    stepper_motor.turn_distance(100, 45, d_switch[not direction])
    print("kurve ende:")

"""
Main ist die Hauptroutine des Programms die standardmäßig ausgeführt wird und die die anderen Funktionen aufruft und koordiniert.
"""
curvecount = 0
direction = ""
curve_back = ""

def sensor():
    global left, right, front
    front = ultrasonic.get_distance("ultrasonic_front")
    left = ultrasonic.get_distance("ultrasonic_left")
    right = ultrasonic.get_distance("ultrasonic_right")
    print('lfr: %10.2f %10.1f %10.2f' % (left , front , right))


def main():
    global direction, d_switch, curve_count, running, curve_goal, distance_side, distance_front

    print("start 1")

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
        while not is_next_curve(60):
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
    
        
    print("start 1")
    drive_motor.speed = 100
    while running:
        kurvestart = 0
        
        time.sleep(0.1)
        ## print("lfr:" + float(left):.1f}|{front:.2f}|{right:.1f}")

        
        if front < 40 :
            # kurve start
            drive_motor.speed = 100
            if right > left:
                direction = "right"
                curve_back = "left"
            else:
                direction = "left"
                curve_back = "right"
            print("front  => kurve:" + direction)
       
            stepper_motor.turn_distance(100, 45, direction)
            kurve = ""
            time.sleep(1.3)
            curvecount = 1
            print("kurve ende:")
            stepper_motor.turn_distance(100, 45, curve_back)
            
        

        if front < 20:
            # no t stop
            print("front < 20 ")
            drive_motor.speed = 0
            running = False

    import reset
    print("ENDE")

"""
es werden Threads gestartet um mehrere Messungen und Abläufe in Echtzeit parallel ausführen zu können
"""

thread_1 = Thread(target=main)
thread_2 = Thread(target=drive_motor.on)

thread_1.start()
thread_2.start()
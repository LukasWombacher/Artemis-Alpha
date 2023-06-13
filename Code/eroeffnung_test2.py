import stepper_motor
import ultrasonic
import drive_motor
import time
from threading import Thread
import edit_json
#import display
import RPi.GPIO as GPIO
import os


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

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
last_curve_time = time.time()

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
current_steer = 0

"""
überprüft in welche Richtung das Auto ausgerichtet ist und ob in oder gegen den Uhrzeigersinn gefahren wird
"""

def get_start_direction():
    global direction, distance_left, distance_right
    distance = 150
    len = 2
    pos = 0
    while direction == 2:
        time.sleep(0.01)
        sensor_left = ultrasonic.get_safe_distance("ultrasonic_left")
        sensor_right = ultrasonic.get_safe_distance("ultrasonic_right")
        distance_left[pos % len], distance_right[pos % len] = sensor_left, sensor_right
        logging.debug('get_start_direction : sensor_left:'+str(sensor_left) + ", sensor_right:" + str(sensor_right))

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
            ## print(left_big, right_big)
            if left_big >= 2:
                direction = 0
            if right_big >= 2:
                direction = 1
            logging.debug('get_start_direction : left_big:'+str(left_big) + ", right_big:" + str(right_big))
    
    logging.info("direction:"+ d_switch[direction])

"""
prüft ob die nächste Kurve gefahren werden kann
"""
      
def is_next_curve():
    global direction, d_switch, distance_front, distance_side, next_len, next_pos

    if (time.time() - last_curve_time) < 3:
        return False

    
    distance_front = ultrasonic.get_safe_distance("ultrasonic_front")
    distance_side = ultrasonic.get_safe_distance("ultrasonic_" + d_switch[direction])

    ## print('is_next_curve - front: %10.2f side:%10.2f' %  (distance_front,  distance_side))
 
    if (0 < distance_front < 90) and (120 < distance_side < 500):
        print("is_next_curve true, direction:" + d_switch[direction] + ", front:" + str(distance_front) + ", side:" + str(distance_side))
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

def sensor():
    global left, right, front
    front = ultrasonic.get_distance("ultrasonic_front")
    left = ultrasonic.get_distance("ultrasonic_left")
    right = ultrasonic.get_distance("ultrasonic_right")
    print('sensor - direction:' + d_switch[direction] + ' - lfr: %10.2f %10.1f %10.2f' % (left , front , right))

"""
geradenkorrektur
"""

def accurate():
    global curve_count, direction, d_switch
    global left, right, front
    ## sensor()
    
    time.sleep(0.1)

    left = ultrasonic.get_safe_distance("ultrasonic_left")
    right = ultrasonic.get_safe_distance("ultrasonic_right")
    
    correction_delta = 0
    correction_direction = 2
    correct_angle = 0
    correct_time = 0
    
    if left < 150 and right < 150:
        correction_delta = int(abs(right - left))
        
        if (right > left):
            correction_direction = 1
        else:
            correction_direction = 0
            
    if correction_delta > 15:
        correct_time = 0.5
        correct_angle = 20

    #if correction_delta > 30:
    #    correct_time = 0.2
    #    correct_angle = 20

    debug = '(accurate)correction_direction:' + d_switch[correction_direction]
    debug += ', correct_time:' + str (correct_time)
    debug += ', correct_angle:' + str (correct_angle) + ', delta:' + str(correction_delta) 
    debug += ', left:' + str (left) + ', right:' + str(right) 
    print( debug )
        
    if (correct_time > 0):    
        stepper_motor.turn_distance(100, correct_angle, d_switch[correction_direction]) 
        time.sleep(correct_time)
        stepper_motor.turn_distance(100, correct_angle, d_switch[not correction_direction]) 
        ## stepper_motor.turn_distance(100, correct_angle + 2, d_switch[not correction_direction]) 
        ## time.sleep(0.1)
        ##stepper_motor.turn_distance(100, 2, d_switch[correction_direction]) 


"""
fährt eine 90° Kurve
"""

def curve():
    global direction, d_switch, curve_count
    curve_count += 1
    steer_angle = 45
    steer_time = 1.3
    drive_time = 1.0
    
    print("Kurve " + str(curve_count))
    stepper_motor.turn_distance(100, steer_angle, d_switch[direction])
    time.sleep(steer_time)
    stepper_motor.turn_distance(100, steer_angle, d_switch[not direction])
    print("lenk fertig")

    time.sleep(drive_time)
    print("kurve fertig")

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
    time.sleep(0.5)
    display.icon("icon_programs.png")
    while not encoder_pressed:
        rotary_Change(0.1)
    display.logo("Artemis_Alpha.png")
    time.sleep(1)"""
    drive_motor.speed = v_start
    print("start")
    get_start_direction()
    ## print(d_switch[direction])
    drive_motor.speed = v_gerade
    while not is_next_curve():
        time.sleep(0.01)
    drive_motor.speed = v_kurve
    curve()

    drive_motor.speed = v_gerade
    while running:
        distance_front, distance_side = [0]*3, [0]*3
        while not is_next_curve():
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

thread_1 = Thread(target=main)
thread_2 = Thread(target=drive_motor.on)

thread_1.start()
thread_2.start()

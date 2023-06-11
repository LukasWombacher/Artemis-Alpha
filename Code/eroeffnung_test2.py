import stepper_motor
import ultrasonic
import drive_motor
import time
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
v_start = 100

sensor_front = 0
sensor_left = 0
sensor_right = 0

starttime = time.time_ns()

"""
überprüft in welche Richtung das Auto ausgerichtet ist und ob in oder gegen den Uhrzeigersinn gefahren wird
"""
def log (str):
    duration  = time.time_ns() - starttime
    
    # print (duration.str())
    print(str)

def get_start_direction():
    global direction, distance_left, distance_right
    distance = 150
    len = 2
    pos = 0
    while direction == 2:
        time.sleep(0.01)
        sensor()
        distance_left[pos % len], distance_right[pos % len] = ultrasonic.get_distance("ultrasonic_left"), ultrasonic.get_distance("ultrasonic_right")
        ## print('get_start_direction - distance: %10.2f %10.2f' %  (distance_left[pos % len],  distance_right[pos % len]))

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
            print('get_start_direction : left_big:'+str(left_big) + ", right_big:" + str(right_big))
    
    print("direction:"+ d_switch[direction])

"""
prüft ob die nächste Kurve gefahren werden kann
"""
      
def is_next_curve():
    global direction, d_switch

    ##sensor()
    
    sensor_front = ultrasonic.get_distance("ultrasonic_front")
    sensor_side = ultrasonic.get_distance("ultrasonic_" + d_switch[direction])

 
    if (10 < sensor_front < 60) and (150 < sensor_side < 1000):
        print("is_next_curve true, direction:" + d_switch[direction] + ", sensor_front:" + str(sensor_front) + ", sensor_side:" + str(sensor_side))
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
    global sensor_left, sensor_right, sensor_front
    sensor_front = ultrasonic.get_distance("ultrasonic_front")
    sensor_left = ultrasonic.get_distance("ultrasonic_left")
    sensor_right = ultrasonic.get_distance("ultrasonic_right")
    print('sensor - direction:' + d_switch[direction] + ' - lfr: %6.1f %6.1f %6.1f' % (sensor_left , sensor_front , sensor_right))

def accurate():
    global curve_count, direction, d_switch
    global sensor_left, sensor_right,sensor_front

    sensor_left = ultrasonic.get_distance("ultrasonic_left")
    sensor_right = ultrasonic.get_distance("ultrasonic_right")
    
    correction_delta = 0
    correct_time = 0
    
    if sensor_left < 90 and sensor_right < 90:
        correction_direction = 2
        correct_angle = 0
        correct_time = 0

        
        if (sensor_right > sensor_left):
            correction_direction = 1
            correction_delta = sensor_right - sensor_left
        else:
            correction_direction = 0
            correction_delta = sensor_left - sensor_right
            
    ## geradenkorrektur
    if correction_delta > 5:
        correct_time = 0.2
        correct_angle = 5

    if correction_delta > 30:
        correct_time = 0.4
        correct_angle = 15
        
    if (correct_time > 0):    
        print('correction_direction:' + d_switch[correction_direction]  + ', correct_angle:' + str (correct_angle) + ', delta:' + str(correction_delta))
        stepper_motor.turn_distance(100, correct_angle, d_switch[correction_direction]) 
        time.sleep(correct_time)
        stepper_motor.turn_distance(100, correct_angle*2, d_switch[not correction_direction]) 
        time.sleep(0.1)
        stepper_motor.turn_distance(100, correct_angle, d_switch[correction_direction]) 


"""
fährt eine 90° Kurve
"""

def curve():
    global direction, d_switch, curve_count
    curve_count += 1
    steer_angle = 30
    steer_time = 2.3
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
    global starttime
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
    starttime = time.time_ns()    
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
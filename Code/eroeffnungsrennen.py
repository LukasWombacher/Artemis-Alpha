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
import logger

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
last_curve_timer = time.time() - 5

"""
überprüft in welche Richtung das Auto ausgerichtet ist und ob in oder gegen den Uhrzeigersinn gefahren wird
"""

def get_start_direction(distance):
    global direction, distance_left, distance_right
    len = 2
    pos = 0
    while direction == 2:
        #time.sleep(0.1)
        distance_left[pos % len], distance_right[pos % len] = ultrasonic.get_safe_distance("ultrasonic_left"), ultrasonic.get_safe_distance("ultrasonic_right")
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
        print("get_start_direction:", distance_left, distance_right)

"""
prüft ob die nächste Kurve gefahren werden kann
"""
      
def is_next_curve(opt_front_distance):
    global direction, d_switch, last_curve_timer

    if (time.time() - last_curve_timer) < 5:
        return False


    sensor_front = ultrasonic.get_distance("ultrasonic_front")
    sensor_side = ultrasonic.get_distance("ultrasonic_" + d_switch[direction])
    
    if (5 < sensor_front < opt_front_distance) and (120 < sensor_side < 500):
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
def side_lenk(lenk_angle, lenk_direction, lenk_time):
    global d_switch
    print ("side_lenk", "lenk_angle", lenk_angle, "lenk_direction:", d_switch[lenk_direction], "lenk_time:", lenk_time)
    stepper_motor.turn_distance(100, round(abs(lenk_angle)), d_switch[lenk_direction])
    time.sleep(lenk_time)
    stepper_motor.turn_distance(100, round(abs(lenk_angle)), d_switch[not lenk_direction])

def accurate():
    global curve_count, direction, d_switch

    sensor_left = ultrasonic.get_safe_distance("ultrasonic_left")
    sensor_right = ultrasonic.get_safe_distance("ultrasonic_right")
    
    correction_delta = 0
    correction_direction = 2
    correct_angle = 0
    correct_time = 0
    stepper_speed = 60
    
    smaller_distance = 0
    
    if sensor_left < 40 or sensor_right < 40:
        correction_delta = abs(sensor_right - sensor_left)
        
        if (sensor_left < 30):
            correction_direction = 1
            smaller_distance = sensor_left
        if (sensor_right < 30):
            correction_direction = 0
            smaller_distance = sensor_right
    
    # no correction possible       
    if 2 == correction_direction:
        return
    
    #if correction_delta > 30:
    #    correct_time = 0.4
    #    correct_angle = 20
    #elif correction_delta > 20:
    #    correct_time = 0.4
    #    correct_angle = 15
    #elif correction_delta > 15:
    #    correct_time = 0.3
    #    correct_angle = 10

    if smaller_distance < 10:
        correct_time = 0.5
        correct_angle = 20
    elif smaller_distance < 20:
        correct_time = 0.4
        correct_angle = 15
    elif smaller_distance < 30:
        correct_time = 0.3
        correct_angle = 10
        
    if (correct_time > 0):    
        debug = "START correction " + d_switch[correction_direction]  
        debug += " - sensor: " + str(sensor_left) + "," + str(sensor_right)
        debug += " , correct_angle:" + str (correct_angle) + ', delta:' + str(correction_delta)
        logger.log(logger.INFO, "(drive_straight) - " + debug)

        stepper_motor.turn_distance(stepper_speed, correct_angle, d_switch[correction_direction]) 
        time.sleep(correct_time)
        stepper_motor.turn_distance(stepper_speed, correct_angle, d_switch[not correction_direction]) 

        sensor_left = ultrasonic.get_safe_distance("ultrasonic_left")
        sensor_right = ultrasonic.get_safe_distance("ultrasonic_right")
        debug = "  END correction " + d_switch[correction_direction]  
        debug += " - sensor: " + str(sensor_left) + "," + str(sensor_right)
        logger.log(logger.INFO, "(drive_straight) - " + debug)
        
def accurate_test():
    global curve_count, direction, d_switch

    side_lenk_time = 0.4
    side_lenk_distance = 30
    side_lenk_angle = 20

    sensor_left = ultrasonic.get_safe_distance("ultrasonic_left")
    sensor_right = ultrasonic.get_safe_distance("ultrasonic_right")
    log_sensor = " - sensor_left:" + str(sensor_left) + ", sensor_right:" + str(sensor_right)
    
    # narrow ? 
    if (sensor_left + sensor_right) <= 70:
        side_lenk_distance = 15
        side_lenk_angle = 20
        side_lenk_time = 0.4
        
    if sensor_left <= side_lenk_distance:
        print("wand links distance:" , side_lenk_distance, log_sensor)
        side_lenk(side_lenk_angle, 1, side_lenk_time)
    elif sensor_right <= side_lenk_distance:
        print("wand rechts", log_sensor)
        side_lenk(side_lenk_angle, 0, side_lenk_time)
    else:
        side_lenk_angle = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))
        lenk_faktor = 0.2
        side_lenk_angle *= lenk_faktor
        if side_lenk_angle > 10: side_lenk_angle = 10
        
        lenk_direction = "right" if side_lenk_angle > 0 else "left"
        anti_lenk_direction = "left" if side_lenk_angle > 0 else "right"
        return
    
        if abs(side_lenk_angle) > 4:
            print("gyro korrektur:", side_lenk_angle, log_sensor)
            stepper_motor.turn_distance(60, round(abs(side_lenk_angle)), lenk_direction)
            time.sleep(0.05)
            stepper_motor.turn_distance(60, round(abs(side_lenk_angle)), anti_lenk_direction)

"""
fährt eine 90° Kurve
"""

def curve():
    global direction, d_switch, curve_count, last_curve_timer
    curve_count += 1
    steer_angle = 45
    steer_time = 1.3
    drive_time = 1.0
    
    print("Kurve " + str(curve_count))
    stepper_motor.turn_distance(100, steer_angle, d_switch[direction])
    time.sleep(steer_time)
    stepper_motor.turn_distance(100, steer_angle, d_switch[not direction])
    print("lenk fertig")
    last_curve_timer = time.time()


def curve_gyro():
    global direction, d_switch, curve_count, last_curve_timer
    curve_count += 1
    print("Kurve " + str(curve_count))
    stepper_motor.turn_distance(100, 50, d_switch[direction])
    while abs(gyroscope.get_abs_degree()) - (90*(curve_count-1)) < 60:
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

"""
es werden Threads gestartet um mehrere Messungen und Abläufe in Echtzeit parallel ausführen zu können
"""

thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=main)
thread_3 = Thread(target=drive_motor.on)

thread_1.start()
thread_2.start()
thread_3.start()
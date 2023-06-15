import time, camera, drive_motor, stepper_motor, gyroscope, ultrasonic
from threading import Thread

biggest_object = ["", 0, 0]

curve_count = 0
direction = 0 #2

def side_lenk(lenk, lenk_direction, anti_lenk_direction, side_lenk_speed):
    stepper_motor.turn_distance(60, round(abs(lenk)), lenk_direction)
    time.sleep(side_lenk_speed)
    stepper_motor.turn_distance(100, round(abs(lenk)), anti_lenk_direction)

def accurate():
    objects = camera.find_objects()
    #print(objects)
    biggest_object = ["", 0, 0]
    for object in objects:
        if object[2] > biggest_object[2] and object[0] == "rot":
            biggest_object = object
    print(biggest_object)
    print(biggest_object[1]*biggest_object[2])
    if (biggest_object[1]*biggest_object[2]) > 6000 and biggest_object[0] == "rot":
        print("ausweichen rot")
        lenk = round((biggest_object[1]*biggest_object[2])/300)
        if lenk > 35:
            lenk = 35
        print(lenk)
        stepper_motor.turn_distance(80, lenk, "right")
        time.sleep(1.5)
        stepper_motor.turn_distance(80, 2*lenk, "left")
        while abs(gyroscope.get_abs_degree()) - (90*(curve_count)) > 12:
            time.sleep(0.001)
        stepper_motor.turn_distance(100, lenk, "right")
    elif (biggest_object[1]*(640-biggest_object[2])) > 6000 and biggest_object[0] == "grün":
        print("ausweichen grün")
        lenk = round((biggest_object[1]*(640-biggest_object[2]))/300)
        if lenk > 35:
            lenk = 35
        print(lenk)
        stepper_motor.turn_distance(80, lenk, "left")
        time.sleep(1.5)
        stepper_motor.turn_distance(80, 2*lenk, "right")
        while abs(gyroscope.get_abs_degree()) - (90*(curve_count)) > 12:
            time.sleep(0.001)
        stepper_motor.turn_distance(100, lenk, "left")
    """elif ultrasonic.get_distance("ultrasonic_left") <= 16:
        lenk_direction, anti_lenk_direction = "right", "left"
        print("wand links")
        side_lenk(28, lenk_direction, anti_lenk_direction, 0.4)
    elif ultrasonic.get_distance("ultrasonic_right") <= 16:
        lenk_direction, anti_lenk_direction = "left", "right"
        print("wand links")
        side_lenk(28, lenk_direction, anti_lenk_direction, 0.4)
    else:
        lenk = (gyroscope.get_abs_degree() + (90*curve_count*((2*direction)-1)))
        lenk_faktor = 0.8
        lenk *= lenk_faktor
        print(lenk)
        lenk_direction = "right" if lenk > 0 else "left"
        anti_lenk_direction = "left" if lenk > 0 else "right"
        stepper_motor.turn_distance(45, round(abs(lenk)), lenk_direction)
        stepper_motor.turn_distance(45, round(abs(lenk)), anti_lenk_direction)"""

def main():
    global biggest_object
    thread_3.start()
    print("start")
    gyroscope.restart()
    time.sleep(0.5)
    drive_motor.speed = 100
    while True:
        accurate()
        #time.sleep(1)
        #drive_motor.speed = 0
         
thread_1 = Thread(target=gyroscope.record_degree)
thread_2 = Thread(target=main)
thread_3 = Thread(target=drive_motor.on)

#thread_1.start()
#thread_2.start()
#thread_3.start()
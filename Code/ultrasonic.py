from pydoc import tempfilepager
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import edit_json
import math


#setup ultrasonic sensors

pin_trigger = {
"ultrasonic_front": edit_json.get_pin_ports("ultrasonic_front")[1],
"ultrasonic_left": edit_json.get_pin_ports("ultrasonic_left")[0],
"ultrasonic_right": edit_json.get_pin_ports("ultrasonic_right")[0]
}
pin_echo = {
"ultrasonic_front": edit_json.get_pin_ports("ultrasonic_front")[0],
"ultrasonic_left": edit_json.get_pin_ports("ultrasonic_left")[1],
"ultrasonic_right": edit_json.get_pin_ports("ultrasonic_right")[1]
}

for single_pin_trigger in pin_trigger.items():
    GPIO.setup(single_pin_trigger[1], GPIO.OUT)
    GPIO.output(single_pin_trigger[1], 0)

for single_pin_echo in pin_echo.items():
    GPIO.setup(single_pin_echo[1], GPIO.IN)

#calibrate speed of sound

temperature = edit_json.get_variable("temperature")
speed_of_sound = 33150 * math.sqrt(1 + (temperature / 273.15))

"""
return the distance of the given sensor in cm with decimal places [default value = 1]
"""

def get_distance(sensor, decimal_places=1):
    GPIO.output(pin_trigger[sensor], True)
    time.sleep(0.00001)
    GPIO.output(pin_trigger[sensor], False)
    
    init_time = time.time()
    start_time = init_time
    end_time = init_time
    
    # print("sensor:" + sensor + " - Start : " + str(time.time()- end_time))
    while GPIO.input(pin_echo[sensor]) == 0 and time.time() - init_time < 0.1:
        start_time = time.time()
    # print("sensor:" + sensor + " - 0 " + str(time.time()- start_time))        
    while GPIO.input(pin_echo[sensor]) == 1 and time.time() - init_time < 0.2:
        end_time = time.time()
    # print("sensor:" + sensor + " - 1 " + str(time.time()- start_time))        
        
    delay = end_time - start_time
    # print("sensor:" + sensor + " delay " + str(delay))        
    distance = (delay * speed_of_sound) / 2
    ## TODO eliminate wrong meassures (1 < distance < 4000)
    # print("sensor:" + sensor + " distance " + str(distance))        
    return round(distance, decimal_places)

def get_safe_distance(sensor):
    distance = int(get_distance(sensor))
    
    if distance < 1:
        print("ERROR **** get_safe_distance:" + sensor + ", distance:" + str(distance))
        distance = 0

    if distance > 500:
        print("ERROR **** get_safe_distance:" + sensor + ", distance:" + str(distance))
        distance = 500
    
    return distance
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import edit_json
import time

speed = 0
on_bool = True


#setup drive_motor

pin_drive = edit_json.get_pin_ports("drive_motor")[0]
GPIO.setup(pin_drive, GPIO.OUT)
pwm_drive = GPIO.PWM(pin_drive, 50)
pwm_drive.start(0)

"""
start drive motor with speed [0 - 100]
"""

def on():
    global speed
    while on_bool:
        pwm_drive.ChangeDutyCycle(speed)
        time.sleep(0.25)

"""
stop drive motor
"""

pwm_drive.ChangeDutyCycle(0)

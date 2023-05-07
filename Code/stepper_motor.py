import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import edit_json


#setup stepper_motor

stepper_motor_pins = edit_json.get_pin_ports("stepper_motor")
for pin in stepper_motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

stepper_motor_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

"""
move stepper motor for distance
parameters: speed[0-100], degree, direction["left", "right"]
"""

def turn_distance(speed, degree, direction):
    if speed == 0:
        return
    steps = int((degree/360) * 512)
    if direction == "left":
        for step in range(0, steps * len(stepper_motor_seq)):
            for i in range(0, 4):
                GPIO.output(stepper_motor_pins[i], stepper_motor_seq[step % len(stepper_motor_seq)][i])
            time.sleep(0.001 * (100/speed))
    elif direction == "right":
        for step in range(0, steps * len(stepper_motor_seq)):
            for i in range(0, 4):
                GPIO.output(stepper_motor_pins[i], stepper_motor_seq[len(stepper_motor_seq)-1-(step % len(stepper_motor_seq))][i])
            time.sleep(0.001 * (100/speed))
    stop()

def test():
    turn_distance(100, 50, "right")
    while True:
        turn_distance(100, 100, "left")
        turn_distance(100, 100, "right")


def stop():
    for i in range(0, 4):
        GPIO.output(stepper_motor_pins[i], 0)

stop()
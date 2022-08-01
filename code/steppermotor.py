import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#setup stepmotor
stepmotor_pins = [24, 25, 8, 7]
for pin in stepmotor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

stepmotor_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def stepmotor_move(speed, degree, direction):
    if speed == 0:
        return
    steps = int((degree/360) * 512)
    if direction == "left":
        for step in range(0, steps * len(stepmotor_seq)):
            for i in range(0, 4):
                GPIO.output(stepmotor_pins[i], stepmotor_seq[step % len(stepmotor_seq)][i])
            time.sleep(0.001 * (100/speed))
    elif direction == "right":
        for step in range(0, steps * len(stepmotor_seq)):
            for i in range(0, 4):
                GPIO.output(stepmotor_pins[i], stepmotor_seq[len(stepmotor_seq)-1-(step % len(stepmotor_seq))][i])
            time.sleep(0.001 * (100/speed))

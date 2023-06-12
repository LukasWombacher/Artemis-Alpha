import stepper_motor
import drive_motor
import time
#import led

stepper_motor.stop()
drive_motor.speed = 0
time.sleep(0.5)
drive_motor.on_bool = False
#led.clear()


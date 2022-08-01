import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#setup ultrasonic sensor
trigger_pin = 21
echo_pin = 20
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def ultrasonic_get_distance():
    # Trig High setzen
    GPIO.output(trigger_pin, True)
 
    # Trig Low setzen (nach 0.01ms)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)
 
    Startzeit = time.time()
    Endzeit = time.time()
 
    # Start/Stop Zeit ermitteln
    while GPIO.input(echo_pin) == 0:
        Startzeit = time.time()
 
    while GPIO.input(echo_pin) == 1:
        Endzeit = time.time()
 
    # Vergangene Zeit
    Zeitdifferenz = Endzeit - Startzeit
	
    # Schallgeschwindigkeit (34300 cm/s) einbeziehen
    distance = (Zeitdifferenz * 34300) / 2
 
    return distance
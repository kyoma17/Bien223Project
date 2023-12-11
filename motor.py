#move a stepper motor in gpio 20 and 21(step and direction) pin 38 and 40
# Stepper controller is an A4988

import RPi.GPIO as GPIO
import time
import sys

DIR_PIN = 20
STEP_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Set direction clockwise
GPIO.output(DIR_PIN, GPIO.HIGH)

# rotate 200 steps
for i in range(600):
    print(i)
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(0.005)

# Go in reverse
GPIO.output(DIR_PIN, GPIO.LOW)

# rotate 200 steps
for i in range(600):
    print(i)
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(0.005)``\\

GPIO.cleanup()
# Rasbperry GPIO for Temperature Probe
'''
This project is to control a stepper motor as a peristaltic pump.
The persistalis pump will pump coldwater into a vessel to cool it down.
The temperature of the vessel will be monitored by a temperature probe.
This is to model an insulin pump.
The temperature prob will be analogous to a Continuous Glucose Monitor (CGM)
We will wrap the temperature probe in a layer of electrical tape
to simulate the delay in the CGM reading the blood glucose. 
The stepper motor will be analogous to an insulin pump.
The temperature will be analogous to blood glucose.
The vessel will be analogous to the body.

We will use a transfer function to convert the temperature to a number of steps
needed to move the stepper motor to pump the correct amount of cold water into
the vessel to cool it down to the desired temperature.

Our Desired temperature will be 37 degrees celcius analogous to a blood glucose at 100 mg/dl.

Pouring hot water into the vessel will simulate a high blood glucose event.
'''
import time
import RPi.GPIO as GPIO
import os
import glob

DIR_PIN = 20
STEP_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Set direction clockwise
GPIO.output(DIR_PIN, GPIO.HIGH)

# 400 steps is approximately 1 ml of water


# GPIO for Temperature Probe is on pin 4
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + "/w1_slave"
temp_target = 30

def main():
    while True:
        temp_c, temp_f = read_temp()
        print(temp_c, temp_f)
        ml_needed = temp_c - temp_target
        print(ml_needed)
        deliver_insulin(ml_needed)
        time.sleep(1)

def transfer_function(temp_c):
    '''Convert temperature to number of steps needed to move stepper motor'''
    ml_needed = temp_c - temp_target
    steps = ml_needed * 400
    return steps

def deliver_insulin(ml_needed):
    '''Deliver 1 ml of ice water at 0 degrees celcius'''
    steps = ml_needed * 400
    steps =  int(steps)
    GPIO.output(DIR_PIN, GPIO.HIGH)
    for i in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.005)

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
        return lines
    
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()    
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]        
        temp_c = float(temp_string) / 1000.0        
        temp_f = temp_c * 9.0 / 5.0 + 32.0        
        return temp_c, temp_f
    
if __name__ == '__main__':
    main()

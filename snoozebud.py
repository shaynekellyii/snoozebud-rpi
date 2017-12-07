from threading import Timer
import RPi.GPIO as GPIO
import time
import spidev
import json
from notif import send_notif

DELAY_SEC = 3
SENSITIVITY = 9
DEBUG = 1

spi = spidev.SpiDev()
spi.open(0,0)

# Setup sensor and motor pins
motorPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin, GPIO.OUT)
GPIO.output(motorPin, GPIO.LOW)

# Read config file
with open('config.json') as data_file:
    data = json.load(data_file)
    SENSITIVITY = data["sensitivity"]
    FCM_ID = data["firebase_id"]
    print("Sensitivity: {0}".format(SENSITIVITY))
    print("FCM ID: {0}".format(FCM_ID))

def read_adc(adc_num):
    r = spi.xfer2([1,(8+adc_num)<<4,0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

def monitorForTime():
    timeout = time.time() + DELAY_SEC
    max_reading_1 = 0
    max_reading_2 = 0
    min_reading_1 = 1000
    min_reading_2 = 1000
    
    while True:
        time.sleep(0.2)
        reading_1 = read_adc(1)
        #print("1 {0}".format(reading_1))
        reading_2 = read_adc(2)
        #print("2 {0}".format(reading_2))
        #print reading

        # reading 1
        if reading_1 > max_reading_1:
            max_reading_1 = reading_1
        elif reading_1 < min_reading_1:
            min_reading_1 = reading_1

        # reading 2
        if reading_2 > max_reading_2:
            max_reading_2 = reading_2
        elif reading_2 < min_reading_2:
            min_reading_2 = reading_2
            
        if time.time() > timeout:
            print("Sensor 1 - Max reading was {0}, min reading was {1}".format(max_reading_1, min_reading_1))
            print("Sensor 2 - Max reading was {0}, min reading was {1}".format(max_reading_2, min_reading_2))
            print("Difference 1: {0}".format(max_reading_1-min_reading_1))
            print("Difference 2: {0}".format(max_reading_2-min_reading_2))
            print("")
            return max(max_reading_1-min_reading_1, max_reading_2-min_reading_2)

def noMovementForTime():
    print("Starting to monitor")
    timeout = time.time() + DELAY_SEC
    while True:
        max_reading = monitorForTime();
        if max_reading >= SENSITIVITY:
            print("Movement detected, monitoring done.")
            return False
        else:
            print("Timer expired with no movement detected")
            return True

##def noMovementForTime():
##    print("Starting to monitor")
##    timeout = time.time() + DELAY_SEC
##    while True:
##        time.sleep(0.1)
##        #reading = mcp.read_adc(0)
##        reading = read_adc(0)
##        if reading is 0:
##            continue
##        print reading
##        if reading > SENSITIVITY:
##            print("Movement detected, monitoring done")
##            print(reading)
##            return False
##        if time.time() > timeout:
##            print("Timer expired with no movement detected")
##            return True

def vibrateForTime(seconds):
    print("Vibrating...")
    GPIO.output(motorPin, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(motorPin, GPIO.LOW)

def main():
    miss_count = 0
    while True:
        #print("Voltage level: {0}".format(read_adc(1)))
        #time.sleep(0.2)
        noMovement = noMovementForTime()
        if noMovement == True:
            miss_count += 1
            if miss_count >= 3:
                vibrateForTime(3)
                print("Firebase response:")
                send_notif(FCM_ID)
                time.sleep(1)
                miss_count = 0
        else:
            miss_count = 0

try:
    main()
except KeyboardInterrupt:
    pass
finally:
   GPIO.cleanup()

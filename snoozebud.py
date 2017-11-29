from threading import Timer
import RPi.GPIO as GPIO
import time
import spidev

DELAY_SEC = 3
SENSITIVITY = 3
DEBUG = 1

spi = spidev.SpiDev()
spi.open(0,0)

# Setup sensor and motor pins
motorPin = 17
inputPin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin, GPIO.OUT)
GPIO.output(motorPin, GPIO.LOW)

def read_adc(adc_num):
    r = spi.xfer2([1,(8+adc_num)<<4,0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

def monitorForTime():
    timeout = time.time() + DELAY_SEC
    max_reading = 0
    while True:
        time.sleep(0.1)
        reading = read_adc(0)
        print reading
        if reading > max_reading:
            max_reading = reading
        if time.time() > timeout:
            return max_reading

def noMovementForTime():
    print("Starting to monitor")
    timeout = time.time() + DELAY_SEC
    while True:
        max_reading = monitorForTime();
        if max_reading > SENSITIVITY:
            print("Movement detected, monitoring done. Max reading was {0}".format(max_reading))
            #print(max_reading)
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
    while True:
        print("Voltage level: {0}".format(read_adc(1)))
        time.sleep(0.2)
        #noMovement = noMovementForTime()
        #if noMovement == True:
        #    vibrateForTime(3)
	#    time.sleep(1)

try:
    main()
except KeyboardInterrupt:
    pass
finally:
   GPIO.cleanup()

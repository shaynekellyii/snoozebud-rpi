from threading import Timer
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

DELAY_SEC = 5

# Setup sensor and motor pins
motorPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin, GPIO.OUT)
GPIO.cleanup()
GPIO.output(motorPin, GPIO.LOW)

# Setup MCP3008 SPI configuration
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def noMovementForTime():
    print("Starting to monitor")
    timeout = time.time() + DELAY_SEC
    while True:
        if mcp.read_adc(0) > 10:
            print("Movement detected, monitoring done")
            return False
        if time.time() > timeout:
            print("Timer expired with no movement detected")
            return True

def vibrateForTime(seconds):
    print("Starting to vibrate")
#    timeout = time.time() + seconds
    GPIO.output(motorPin, GPIO.HIGH)
 #   while True:
  #      if (time.time() > timeout):
   #         break
    #    time.sleep(0.5)
    time.sleep(seconds)
    print("Done vibrating")
    GPIO.output(motorPin, GPIO.LOW)

def main():
    while True:
        print("Main program loop beginning")
        noMovement = noMovementForTime()
        if noMovement == True:
            vibrateForTime(3)
	    time.sleep(1)

try:
    main()
except KeyboardInterrupt:
    pass
finally:
   GPIO.cleanup()

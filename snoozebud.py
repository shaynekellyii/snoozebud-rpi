from threading import Timer
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

DELAY_SEC = 5

# Setup sensor and motor pins
motorPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin, GPIO.OUT)
GPIO.output(motorPin, GPIO.LOW)

# Setup MCP3008 SPI configuration
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def noMovementForTime():
    timeout = time.time() + DELAY_SEC
    while True:
        if mcp.read_adc(0) > 10:
            return False
        if time.time() > timeout:
            return True

def vibrateForTime(seconds):
    timeout = time.time() + seconds
    GPIO.output(motorPin, GPIO.HIGH)
    while True:
        if (time.time() > timeout):
            break
        time.sleep(0.5)
    GPIO.output(motorPin, GPIO.LOW)

while True:
    if noMovementForTime() == True:
        vibrateForTime(3)


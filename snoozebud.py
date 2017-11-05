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
    if mcp.read_adc(0) <= 1:
        countdownStart = time.time()
        while (time.time() - countdownStart) < DELAY_SEC:
            if mcp.read_adc(0) > 1:
                return False
    return True

def vibrateForTime(seconds):
    GPIO.output(motorPin, GPIO.HIGH)
    countdownStart = time.time()
    while (time.time() - countdownStart) < seconds:
        continue
    GPIO.output(motorPin, GPIO.LOW)

while True:
    vibrateForTime(3)
    if noMovementForTime() == True:
        vibrateForTime(3)

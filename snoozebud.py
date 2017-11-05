import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Setup sensor and motor pins
sensorPin = 2
motorPin = 3
GPIO.setmode(GPIO.BCM)
#GPIO.setup(sensorPin, GPIO.IN)
#GPIO.setup(motorPin, GPIO.OUT)
#GPIO.output(motorPin, GPIO.LOW)
#print("Pins setup done")

# Setup MCP3008 SPI configuration
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Read MCP3008 inputs
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
#print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
#    values = [0]*8
#    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
#        values[i] = mcp.read_adc(i)
    # Print the ADC values.
#    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
   print(mcp.read_adc(0)) 
   time.sleep(0.1)

#while True:
#    if movementDetected() == True:
#        GPIO.output(motorPin, GPIO.HIGH)

def movementDetected():
    return True

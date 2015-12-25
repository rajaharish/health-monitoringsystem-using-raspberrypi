import time
import RPi.GPIO as GPIO
 

GPIO.setmode(GPIO.BCM)
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if ( (adcnum > 7) or (adcnum < 0) ):
		return -1
	GPIO.output(cspin, True)
 
	GPIO.output(clockpin, False) # start clock low
	GPIO.output(cspin, False) # bring CS low
 
	commandout = adcnum
	commandout |= 0x18 # start bit + single-ended bit
	commandout <<= 3 # we only need to send 5 bits here
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
	commandout <<= 1
	GPIO.output(clockpin, True)
	GPIO.output(clockpin, False)
 
	adcout = 0
# read in one empty bit, one null bit and 10 ADC bits
	for i in range(12):
		GPIO.output(clockpin, True)
GPIO.output(clockpin, False)
adcout <<= 1
if (GPIO.input(misopin)):
	adcout |= 0x1
 
GPIO.output(cspin, True)
 
adcout >>= 1 # first bit is 'null' so drop it
return adcout
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Raspberry Pi</h1>
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
GPIO.setwarnings(False)
#set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
#pulse sensor connected to adc #0
pulse_adc = 0
#Threshold for pulse sensing (half of values between 0-1023)
THRESH = 512
#pulse detection
pulse = False
 
while True:
	#read the analog pin
	analog_value = readadc(pulse_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	#draw the equivalent number of points in an attempt to draw a vertical pulse sensing graph
	for i in range(analog_value / 100):
		print ".",
		#detect beats
		if (analog_value > THRESH):
			if (pulse == False):
				pulse = True
				print "Beat"
			else:	
				print ""
		else:
			pulse = False
			print ""
			#hang out and do nothing for a tenth of a second
		time.sleep(0.1)

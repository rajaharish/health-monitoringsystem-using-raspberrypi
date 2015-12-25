import time
import datetime
import sqlite3
import spidev3
import RPi.GPIO as GPIO

con= sqlite3.connect('databse.sqlite')
cur=con.cursor()

LIGHT_CHANNEL=0

GPIO.setmode(GPIO.BCM)

LIGHT_PIN=25

#OPEN SPI BUS

spi=spidev.SpiDev()
spi.open(0,0)

threshold=200

def readLDR():
	light_level=ReadChannel(LIGHT_CHANNEL)
	lux=ConvertLux(light_level,2)
	return lux

def ConvertLux(data,places):
	R=10
	volts=(data*3.3)/1023
	volts=round(volts,places)
	lux=500*(3.3-volts)/(R*volts)
	return lux

def ReadChannel(channel):
	adc=spi.xfer2([1,(8+channel)<<4,0])
	data=((adc[1]&3)<<8)+adc[2]
	return data

def getCurrentMode():
	cur.execute('SELECT * FROM SMARTHOMEAPP_mode')
	data=cur.fetchone()
	return data[1]

def getCurrentState():
	cur.execute('SELECT * FROM SMARTHOMEAPP_state')
	data=cur.fetchone()
	return data[1]

def setCurrentState(val):
	query='UPDATE smarthomeapp_state set name="'+val+'"'
	cur.execute(query)

def switchOnLight(PIN):
	GPIO.setup(PIN,GPIO.OUT)
	GPIO.output(PIN,True)


def switchOffLight(PIN):	
	GPIO.setup(PIN,GPIO.OUT)
	GPIO.output(PIN,False)


def runManualMode():
	currentState=getCurrentState()
	if currentState=='On':
		switchOnLight(LIGHT_PIN)
	if currentState=='Off':
		switchOffLight(LIGHT_PIN)

def runAutoMode():
	lightlevel=readLDR()
	if lightlevel<ldr_threshold
		switchOnLight(LIGHT_PIN)
	else:
		switchOffLight(LIGHT_PIN)

	print 'Manual '+' - '+getCurrentState()

def runController():
	currentMode=getCurrentMode()
	if currentMode=='auto':
		runAutoMode()
	elif currentMode=='Manual':
		runManualMode()

	return true

while True:
	runController()
	time.sleep(5)

# Pool control functions
#

import RPi.GPIO as GPIO
import time
from datetime import datetime
import subprocess

skimmer=17	# Pi GPIO skimmer port
vacuum=27	# Pi GPIO vacuum port
power=22	# Pi GPIO transformer port
x10power=10	# x10 power line module
waterfall=5	# Pi GPIO waterfall valve
filter=6	# Pi GPIO filter valve

skimmer_name="Skimmer"
vacuum_name="Vacuum"
power_name="24VAC_transformer"

# Turn on 24V AC valve actuator transformer
#
def powerOn():
  print "24VAC_xformer;func=power:state=on"
  GPIO.output(power,GPIO.HIGH)

# Turn off 24VAC valve actuator transformer
#
def powerOff():
  print "24VAC_xformer;func=power:state=off"
  GPIO.output(power,GPIO.LOW)

# Turn on 24V AC valve actuator transformer
#
def x10PowerOn():
  print "x10PowerLineModule;func=power:state=on"
  GPIO.output(x10power,GPIO.HIGH)

# Turn off 24VAC valve actuator transformer
#
def x10PowerOff():
  print "x10PowerLineModule;func=power:state=off"
  GPIO.output(x10power,GPIO.LOW)


# Begin valve actuator rotation cycle
#
def startRotateSkimmer():
  stopRotateAll
  _logValveOn('skimmer')
  #print "valve;name=skimmer:func=rotate:state=on"
  GPIO.output(skimmer,GPIO.HIGH)

# End valve actuator rotation cycle
#
def stopRotateSkimmer():
  #print "valve;name=skimmer:func=rotate:state=off"
  _logValveOff('skimmer')
  GPIO.output(skimmer,GPIO.LOW)

# Begin valve actuator rotation cycle
#
def startRotateVacuum():
  stopRotateAll
  _logValveOn('vacuum')
  #print "valve;name=vacuum:func=rotate:state=on"
  GPIO.output(vacuum,GPIO.HIGH)

# End valve actuator rotation cycle
#
def stopRotateVacuum():
  _logValveOff('vacuum')
  #print "valve;name=vacuum:func=rotate:state=off"
  GPIO.output(vacuum,GPIO.LOW)

# End valve actuator rotation cycle
#
def stopRotateWaterfall():
  _logValveOff('waterfall')
  GPIO.output(waterfall,GPIO.LOW)

# End valve actuator rotation cycle
#
def stopRotateFilter():
  _logValveOff('filter')
  GPIO.output(filter,GPIO.LOW)


# Stop all valve actuator rotation cycle
#  
def stopRotateAll():
  stopRotateVacuum()
  stopRotateSkimmer()
  stopRotateWaterfall()
  stopRotateFilter()

# Turn on actuator transformer.  Used for manual valve operation
#
def startManualMode():
  stopRotateAll
  powerOn()
  startRotateSkimmer()

# Turn on actuator transformer.  Used to disable manual valve operation
#  
def stopManualMode():
  stopRotateAll()
  stopRotateSkimmer
  powerOff()
  
# Rotate the filter valve actuator to the skimmer
#
def filter_valve_to_skimmer():
	try:
		initializeAll()
		powerOn()
		startRotateSkimmer()
		time.sleep(36)
	finally:
		stopRotateSkimmer()
		powerOff()
		cleanupAll()

# Rotate the filter valve actuator to the vacuum
#
def filter_valve_to_vacuum():
	try:
		initializeAll()
		powerOn()
		startRotateVacuum()
		time.sleep(36)
	finally:
		stopRotateVacuum()
		powerOff()
		cleanupAll()

# Enable manual actuator mode
#
def filter_valve_on():
   initializeAll()
   startManualMode()

# Disable manual actuator mode
#
def filter_valve_off():
   initializeAll()
   stopManualMode()
   cleanupAll()
   
def lightall_on():
   initializeAll()
   x10PowerOn()
   time.sleep(2)
   subprocess.check_output(["lightall-on"], stderr=subprocess.STDOUT)
   time.sleep(2)
   x10PowerOff()
   cleanupAll()

def lightall_off():
   initializeAll()
   x10PowerOn()
   time.sleep(2)
   subprocess.check_output(["lightall-off"], stderr=subprocess.STDOUT)
   time.sleep(2)
   x10PowerOff()
   cleanupAll()
   

# Enable PI GPIO for use
#
def initializeAll():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(power,GPIO.OUT) 
  GPIO.setup(skimmer,GPIO.OUT)
  GPIO.setup(vacuum,GPIO.OUT)
  GPIO.setup(x10power,GPIO.OUT)
  GPIO.setup(waterfall,GPIO.OUT)
  GPIO.setup(filter,GPIO.OUT)
  stopRotateAll()
  
# Called to cleanup Pi GPIO state
# 
def cleanupAll():
  GPIO.cleanup()

# Rotate the function valve to waterfall
def function_valve_to_waterfall():
	try:
		initializeAll()
		powerOn()
		_logValveOn('waterfall')
		GPIO.output(waterfall,GPIO.HIGH)
		time.sleep(36)
	except KeyboardInterrupt:
		print "SIGINT"
	finally:
		_logValveOff('waterfall')
		GPIO.output(waterfall,GPIO.LOW)
		powerOff()
		cleanupAll()

# Rotate the function valve to filter
def function_valve_to_filter():
	try:
		initializeAll()
		powerOn()
		_logValveOn('filter')
		GPIO.output(filter,GPIO.HIGH)
		time.sleep(36)
	except KeyboardInterrupt:
		print "SIGINT"
	finally:
		_logValveOff('filter')
		GPIO.output(filter,GPIO.LOW)
		powerOff()
		cleanupAll()

def testWf():
	try:
		initializeAll()
		_logValveOn('waterfall')
		GPIO.output(waterfall,GPIO.HIGH)
		time.sleep(36)
	except KeyboardInterrupt:
		print "SIGINT"
	finally:
		_logValveOff('waterfall')
		GPIO.output(waterfall,GPIO.LOW)
		cleanupAll()
	
def testFilter():
	try:
		initializeAll()
		_logValveOn('filter')
		GPIO.output(filter,GPIO.HIGH)
		time.sleep(36)
	except KeyboardInterrupt:
		print "SIGINT"
	finally:
		_logValveOff('filter')
		GPIO.output(filter,GPIO.LOW)
		cleanupAll()

def _dt():
	return str(datetime.now())
def _logValveOn( name ):
	print "["+_dt()+"]control=valve:name="+name+":func=rotate:state=on"
def _logValveOff( name ):
	print "["+_dt()+"]control=valve:name="+name+":func=rotate:state=off"

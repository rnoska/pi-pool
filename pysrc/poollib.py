# Pool control functions
#

import RPi.GPIO as GPIO
import time
from datetime import datetime
import subprocess

skimmer = 17        # Pi GPIO skimmer port
vacuum = 27	        # Pi GPIO vacuum port
power = 22          # Pi GPIO transformer port
x10power = 10       # x10 power line module
waterfall = 5       # Pi GPIO waterfall valve
filtervalve = 6     # Pi GPIO filter valve
fill = 13           # Pi GPIO water filler valve

skimmer_name = "Skimmer"
vacuum_name = "Vacuum"
power_name = "24VAC_transformer"
water_name = "Fill"


def powerOn():
    '''Turn on 24V AC valve actuator transformer
    '''
    print("24VAC_xformer;func=power:state=on")
    GPIO.output(power, GPIO.HIGH)


def powerOff():
    ''' Turn off 24VAC valve actuator transformer
    '''
    print("24VAC_xformer;func=power:state=off")
    GPIO.output(power, GPIO.LOW)


def x10PowerOn():
    ''' Turn on 24V AC valve actuator transformer
    '''
    print("x10PowerLineModule;func=power:state=on")
    GPIO.output(x10power, GPIO.HIGH)


def x10PowerOff():
    ''' Turn off 24VAC valve actuator transformer
    '''
    print("x10PowerLineModule;func=power:state=off")
    GPIO.output(x10power, GPIO.LOW)


def startRotateSkimmer():
    ''' Begin valve actuator rotation cycle
    '''
    stopRotateAll
    _logValveOn('skimmer')
    GPIO.output(skimmer, GPIO.HIGH)


def stopRotateSkimmer():
    ''' End valve actuator rotation cycle
    '''
    _logValveOff('skimmer')
    GPIO.output(skimmer, GPIO.LOW)


def startRotateVacuum():
    ''' Begin valve actuator rotation cycle
    '''
    stopRotateAll
    _logValveOn('vacuum')
    GPIO.output(vacuum, GPIO.HIGH)


def stopRotateVacuum():
    ''' End valve actuator rotation cycle
    '''
    _logValveOff('vacuum')
    GPIO.output(vacuum, GPIO.LOW)


def stopRotateWaterfall():
    ''' End valve actuator rotation cycle
    '''
    _logValveOff('waterfall')
    GPIO.output(waterfall, GPIO.LOW)


def stopRotateFilter():
    ''' End valve actuator rotation cycle
    '''
    _logValveOff('filter')
    GPIO.output(filtervalve, GPIO.LOW)


def stopRotateAll():
    ''' Stop all valve actuator rotation cycle
    '''
    stopRotateVacuum()
    stopRotateSkimmer()
    stopRotateWaterfall()
    stopRotateFilter()


def startManualMode():
    ''' Turn on actuator transformer.  Used for manual valve operation
    '''
    stopRotateAll
    powerOn()
    startRotateSkimmer()


def stopManualMode():
    ''' Turn on actuator transformer.  Used to disable manual valve operation
    '''
    stopRotateAll()
    stopRotateSkimmer
    powerOff()


def filter_valve_to_skimmer():
    ''' Rotate the filter valve actuator to the skimmer
    '''
    try:
        initializeAll()
        powerOn()
        startRotateSkimmer()
        time.sleep(36)
    finally:
        stopRotateSkimmer()
        powerOff()
        cleanupAll()


def filter_valve_to_vacuum():
    ''' Rotate the filter valve actuator to the vacuum
    '''
    try:
        initializeAll()
        powerOn()
        startRotateVacuum()
        time.sleep(36)
    finally:
        stopRotateVacuum()
        powerOff()
        cleanupAll()


def filter_valve_on():
    ''' Enable manual actuator mode
    '''
    initializeAll()
    startManualMode()


def filter_valve_off():
    ''' Disable manual actuator mode
    '''
    initializeAll()
    stopManualMode()
    cleanupAll()


def lightall_on():
    ''' Turn on lights
    '''
    initializeAll()
    x10PowerOn()
    time.sleep(2)
    subprocess.check_output(["/root/rnoska/pool/lightall-on"],
                            stderr=subprocess.STDOUT)
    time.sleep(2)
    x10PowerOff()
    cleanupAll()


def lightall_off():
    ''' Turn off lights
    '''
    initializeAll()
    x10PowerOn()
    time.sleep(2)
    subprocess.check_output(["/root/rnoska/pool/lightall-off"],
                            stderr=subprocess.STDOUT)
    time.sleep(2)
    x10PowerOff()
    cleanupAll()


def initializeAll():
    ''' Enable PI GPIO for use
    '''
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power, GPIO.OUT)
    GPIO.setup(skimmer, GPIO.OUT)
    GPIO.setup(vacuum, GPIO.OUT)
    GPIO.setup(x10power, GPIO.OUT)
    GPIO.setup(waterfall, GPIO.OUT)
    GPIO.setup(filtervalve, GPIO.OUT)
    GPIO.setup(fill, GPIO.OUT)
    stopRotateAll()


def cleanupAll():
    ''' Called to cleanup Pi GPIO state
    '''
    GPIO.cleanup()


def fill_valve_on():
    ''' Turn on the fill valve.
    '''
    try:
        initializeAll()
        powerOn()
        _logFillOn()
        GPIO.output(fill, GPIO.HIGH)
    except KeyboardInterrupt:
        print("SIGINT")


def fill_valve_off():
    ''' Turn off the fill valve.
    '''
    try:
        initializeAll()
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        GPIO.output(fill, GPIO.LOW)
        _logFillOff()
        powerOff()
        cleanupAll()


def function_valve_to_waterfall():
    ''' Rotate the function valve to waterfall
    '''
    try:
        initializeAll()
        powerOn()
        _logValveOn('waterfall')
        GPIO.output(waterfall, GPIO.HIGH)
        time.sleep(36)
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        _logValveOff('waterfall')
        GPIO.output(waterfall, GPIO.LOW)
        powerOff()
        cleanupAll()


def function_valve_to_filter():
    ''' Rotate the function valve to filter.
    '''
    try:
        initializeAll()
        powerOn()
        _logValveOn('filter')
        GPIO.output(filtervalve, GPIO.HIGH)
        time.sleep(36)
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        _logValveOff('filter')
        GPIO.output(filtervalve, GPIO.LOW)
        powerOff()
        cleanupAll()


def testWf():
    try:
        initializeAll()
        _logValveOn('waterfall')
        GPIO.output(waterfall, GPIO.HIGH)
        time.sleep(36)
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        _logValveOff('waterfall')
        GPIO.output(waterfall, GPIO.LOW)
        cleanupAll()


def testFilter():
    try:
        initializeAll()
        _logValveOn('filter')
        GPIO.output(filtervalve, GPIO.HIGH)
        time.sleep(36)
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        _logValveOff('filter')
        GPIO.output(filtervalve, GPIO.LOW)
        cleanupAll()


def _dt():
    return str(datetime.now())


def _logValveOn(name):
    print("["+_dt()+"]control=valve:name="+name+":func=rotate:state=on")


def _logValveOff(name):
    print("["+_dt()+"]control=valve:name="+name+":func=rotate:state=off")


def _logFillOn():
    print("["+_dt()+"]control=fill:state=on")


def _logFillOff():
    print("["+_dt()+"]control=fill:state=off")

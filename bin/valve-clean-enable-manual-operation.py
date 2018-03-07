#!/usr/bin/python
import time
import poollib as poollib

poollib.initializeAll()
poollib.startManualMode()

print poollib.power_name + " remains on for manual operation at the actuator switch"
print "to return to normal operation set the switch to the down position and run valve-clean-disable-manual-operation.py"

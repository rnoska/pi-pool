#!/usr/bin/python3

import time
from datetime import datetime
import poollib as poollib
from ETape import ETape
import serial

class AutoFillExec:
    maxFillMinutes = 25              # The maximum number of minutes to fill regardless of level measurements
    
    startTime=None
    maxFillTimeSecs=60*maxFillMinutes       # Safety stop.  Do not fill longer regardless of measured level.
    #maxFillTimeSecs=15
    
    fillCheckInterval=5000          # During filling check measured level at this interval in ms
    minLevelAsMeasured=515          # Minimum eTape reading (fill at or below this level)
    maxLevelAsMeasured=590          # Maximum etape reading (fill stops at or above this level)
    
    fillValveOn=False               # Track the state of the fill valve
    
    etape=ETape()   
    
    def getCurrentMeasuredLevel(self):
        ''' Measure and return the current water level ''' 
        return self.etape.read()
    
    def startFill(self):
        ''' Turn on the fill valve '''
        self._log('AutoFill:turning on water valve now')
        self.fillValveOn=True
        poollib.fill_valve_on()        
    
    def stopFill(self):
        ''' Turn off the fill valve '''
        self._log('AutoFill:ensuring water valve is off now')
        poollib.fill_valve_off()
        self.fillValveOn=False
    
    def checkShouldFill(self):
        elapsedTime=time.time() - self.startTime
        self._log('AutoFill:elapsed-time=' + str(elapsedTime))
        if elapsedTime >= self.maxFillTimeSecs:
            self._log('AutoFill:Fill time of '+str(elapsedTime/60)+' minutes has exceeded max fill time of ' + str(self.maxFillTimeSecs/60)+ ' minutes')
            self._log('AutoFill:Fill will stop')
            return False
        
        currentFillLevel=self.getCurrentMeasuredLevel()
        if currentFillLevel >= self.maxLevelAsMeasured:
            self._log('AutoFill:Fill water level of '+str(currentFillLevel)+' >= ' + str(self.maxLevelAsMeasured))
            if self.fillValveOn:
                self._log('AutoFill:Fill will stop')
            else:
                self._log('AutoFill:Will not run')
            return False

        self._log('AutoFill:Current water level ('+str(currentFillLevel)+') is below the max level ('+str(self.maxLevelAsMeasured)+')')
        if self.fillValveOn:
            self._log('AutoFill:Fill will continue to run')
        else:
            self._log('AutoFill:Fill will start')
        return True
    
    def startTimer(self):
        self.startTime=time.time()
        self._log('AutoFill:start-time=' + str(self.startTime))
    
    def main(self):
        self._log('AutoFill:Main process started')
        self.startTimer()
        try:
            if self.checkShouldFill():
                self.startFill()
            else:
                return

            while self.checkShouldFill() is True:
                time.sleep(60)
        except Exception as e:
            self._log('AutoFill:Caught exception: '+str(e))
            raise e        
        except KeyboardInterrupt as e:
            self._log('AutoFill:Caught exception: KeyboardInterrupt')
            raise e        
        finally:
            try:
                self._log('AutoFill:fill cycle ending now')
                # Paranoid: ignore the flag and always try to turn the valve off
                # This will stop the filler valve
                self.stopFill()
                self._log('AutoFill:done. Exiting now.')
            except Exception as e:
                # If we do get an exception then try to shut off the transformer
                self._log('AutoFill:Caught exception while trying to turn off the fill valve:', e)
                self._log('AutoFill:PANIC trying to power down valve transformer now!')
                try:
                    # last ditch attempt to ensure the transformer is off to force the valve off
                    # poollib.initializeAll()
                    # poollib.powerOff()
                    #poollib.cleanupAll()
                    self._log('AutoFill:PANIC powered down valve transformer')
                    # SMS message me
                except Exception as e:
                    # If we failed to stop the transformer then notify the operator to pull the power
                    self._log('AutoFill:unable to force the power off.  Manually disable transformer power!')
                    # SMS message me at this point
                    # Put the transformer on insteon appliance module to the AC line voltage can be switched remotely if needed
                    raise e
            
    def _dt(self):
        return str(datetime.now())
    def _log(self,message):
        print("["+self._dt()+"]"+message)
        
if __name__ == "__main__":
    e=AutoFillExec()
    e.main()

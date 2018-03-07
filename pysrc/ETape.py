import serial
import time
import logging

class ETape():
    ''' Set up some defaults '''
    devName='/dev/ttyUSB0'
    bdrate=57600
    devSerial=None
    logger=logging.getLogger("ETape")
    
    def __init__(self,devName='/dev/ttyUSB0',bdRate=57600):
        if devName is not None:
            self.devName = devName
            
        if bdRate is not None:
            self.bdRate = bdRate
            
        try:
            self.logger.info("devName=",self.devName)
            self.devSerial=serial.Serial(self.devName,baudrate=self.bdRate,timeout=2)
            time.sleep(2)
        except Exception as ex:
            self.devSerial=None
            raise
    
    def read(self):
        assert(self.devSerial)
        try:
            self.devSerial.write(b'0')
            etapeBytes=self.devSerial.readline()
            if etapeBytes is None:
                raise Exception('no data received from ETape on ' + self.devName)
            
            etapeResultStr=etapeBytes.decode()
            print(etapeResultStr)
            levelStr=etapeResultStr.split(sep=';')[1].split(sep=',')[2].split(sep='=')[1]
            levelReadingInt=int(levelStr)    
            return levelReadingInt
        
        except Exception as ex:
            self.devSerial=None
            raise
        
    def close(self):
        
        if self.devSerial:
            self.devSerial.close()
            self.devSerial=None
        

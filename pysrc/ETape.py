#!/usr/bin/env python3
import serial
import time
import logging


class ETape():
    ''' Set up some defaults '''
    devName = '/dev/ttyUSB0'
    bdrate = 57600
    devSerial = None
    logger = logging.getLogger("ETape")

    def __init__(self, devName='/dev/ttyUSB0', bdRate=57600):
        if devName is not None:
            self.devName = devName

        if bdRate is not None:
            self.bdRate = bdRate

    def read(self):
        try:
            self.logger.info("devName=", self.devName)
            self.devSerial = serial.Serial(self. devName,
                                           baudrate=self.bdRate, timeout=2)
        except Exception as ex:
            self.devSerial = None
            raise

        etapeResultStr = None
        while True:
            try:
                self.devSerial.write(b'0')
                time.sleep(2)
                etapeBytes = self.devSerial.readline()
                if etapeBytes is None:
                    print('No data received from ETape on {}.  Trying again.'.format(self.devName))  # noqa E501
                    continue
                etapeResultStr = etapeBytes.decode()
                if etapeResultStr:
                    print("ETape.read() got back {}".format(etapeResultStr))
                    break
                else:
                    print("ETape.read() got back empty string.  Trying again.")
            except BlockingIOError as ex:
                self.logger.error('Caught BlockingIOError %s. Trying again.'
                                  % str(ex))
            except Exception as ex:
                self.logger.error('Caught Exception %s. Trying again.'
                                  % str(ex))

        levelStr = etapeResultStr.split(';')[1].split(',')[2].split('=')[1]
        levelReadingInt = int(levelStr)
        self.close()
        return levelReadingInt

    def close(self):
        if self.devSerial:
            self.devSerial.close()
            self.devSerial = None


def main():
    et = ETape()
    et.read()

if __name__ == "__main__":
    main()

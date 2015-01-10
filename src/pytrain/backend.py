'''
Created on 06.01.2015

@author: kinders
'''

try:
    import RPi.GPIO as GPIO
except ImportError:
    from pytrain.GPIOStub import GPIO

import logging
 
log = logging.getLogger('pytrain.backend')
   
class Backend(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.switchState = [ 0,0,0,0,0,0,0,0,0 ]
        # GPIO PIN numbers of the switches
        # first is the 8-port breakout board, second the 4-port breakout board
        GPIO.setmode(GPIO.BOARD)
        self.gpioMap = [ 3,5,7,11,13,15,19,21,  10,12,16,18 ]
        for pinid in self.gpioMap:
            log.info("Initializing PIN {}".format(pinid))
            GPIO.setup(pinid,GPIO.OUT)
            GPIO.output(pinid,0);
        
    def toggleSwitch(self,i):
        pinid = self.gpioMap[i]
        self.switchState[i] = 1-self.switchState[i]
        log.info("switched number [{}], pinid [{}] new state is {}".format(i,pinid,self.switchState))
        GPIO.output(pinid,self.switchState[i]);
        

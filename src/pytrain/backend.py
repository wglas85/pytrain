'''
Created on 06.01.2015

@author: kinders
'''

try:
    import RPi.GPIO as GPIO
except ImportError:
    from pytrain.GPIOStub import GPIO
  
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
        self.gpioMap = [ 3,5,7,11,13,15,19,21,  14,15,18,23 ]
        for pinid in self.gpioMap:
            GPIO.output(pinid,0);
        
    def toggleSwitch(self,i):
        pinid = self.gpioMap[i]
        self.switchState[i] = 1-self.switchState[i]
        print("switched number [",i,"], pinid [",pinid,"] new state is ",self.switchState)
        GPIO.output(pinid,self.switchState[i]);
        
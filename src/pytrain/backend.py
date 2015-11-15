'''
Created on 06.01.2015

@author: kinders
'''

try:
    from RPi import GPIO
except ImportError:
    from pytrain.GPIOStub import GPIO

from threading import Timer
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
        self.switchState = [ 0,0,0,0,0,0,0,0,0,0,1,1 ]
        self.coupling = [[1,9],[0,9],[3],[2],[5],[4],[-11],[8],[7],[0,1],[-7],None ]
        # GPIO PIN numbers of the switches
        # first is the 8-port breakout board, second the 4-port breakout board
        GPIO.setmode(GPIO.BOARD)
        self.gpioMap = [ 3,5,7,11,13,15,19,21,  10,12,16,18 ]
        for i in range(0,len(self.switchState)):
            pinid = self.gpioMap[i]
            log.info("Initializing PIN {}".format(pinid))
            GPIO.setup(pinid,GPIO.OUT)
            GPIO.output(pinid,self.switchState[i]);
        
    def reset(self):
        for i in range(0,len(self.switchState)):
            if self.switchState[i] != 0:
                pinid = self.gpioMap[i]
                log.info("Resetting PIN {}".format(pinid))
                GPIO.output(pinid,0);
        
    def setSwitch(self,i,switchState):
        if self.switchState[i] != switchState:
            self.toggleSwitch(i)
        
    def toggleSwitchInternal(self,i):
        pinid = self.gpioMap[i]
        self.switchState[i] = 1-self.switchState[i]
        log.info("switched number [{}], pinid [{}] new state is {}".format(i,pinid,self.switchState))
        GPIO.output(pinid,self.switchState[i]);

    def toggleSwitch(self,i):
        self.toggleSwitchInternal(i)
        cpl = self.coupling[i]
        if cpl != None:
            for j in cpl:
                if j < 0:
                    if self.switchState[i] != 1-self.switchState[-1-j]:
                        self.toggleSwitchInternal(-1-j)
                else:
                    if self.switchState[i] != self.switchState[j]:
                        self.toggleSwitchInternal(j)
        if i == 11:
            def timerfunc():
                if self.switchState[11]==0:
                    log.info("Resetting special purpose switch [11]")
                    self.toggleSwitchInternal(11)
            timer = Timer(10.0,timerfunc)
            timer.start()
            


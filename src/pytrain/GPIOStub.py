'''
Created on 06.01.2015

@author: kinders
'''
import logging
 
log = logging.getLogger('pytrain.GPIOStub')

class GPIO(object):
    '''
    classdocs
    '''
    BCM = "BCM"
    BOARD = "BOARD"

    IN = "IN"
    OUT = "OUT"
    
    LOW = 0
    HIGH = 1

    @staticmethod
    def setmode(mode):
        log.info("GPIOStub.setmode({}) called.".format(mode))
    
    @staticmethod
    def setup(pinid,direction):
        log.info("GPIOStub.setup({},{}) called.".format(pinid,direction))
        
    @staticmethod
    def output(pinid,state):
        log.info("GPIOStub.output({},{}) called.".format(pinid,state))

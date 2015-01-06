'''
Created on 06.01.2015

@author: kinders
'''

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
        print("GPIOStub.setmode(",mode,") called.")
    
    @staticmethod
    def setup(pinid,direction):
        print("GPIOStub.setup(",pinid,",",direction,") called.")
        
    @staticmethod
    def output(pinid,state):
        print("GPIOStub.output(",pinid,",",state,") called.")

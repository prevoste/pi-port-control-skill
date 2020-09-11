import os
import time
import RPi.GPIO as GPIO
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.parse import extract_number

LED_STATE = 1

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up the GPIO channels - one input and one output
GPIO.setup(3, GPIO.OUT)			# SDA
GPIO.setup(5, GPIO.OUT)			# SCL
GPIO.setup(8, GPIO.OUT)			# TXD
GPIO.output(3, GPIO.LOW)
GPIO.output(5, GPIO.LOW)
GPIO.output(8, GPIO.LOW)

LOGGER = getLogger(__name__)

def PiPortState(port):
    if GPIO.input(port) == 0:
        return("Off")
    else:
        return("On")

class PiPortControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)


    def initialize(self):
        self.register_intent_file('what.state.intent', self.handle_what_state)
        self.register_intent_file('action2.port.intent', self.handle_action2_port)
        self.register_intent_file('action.port.intent', self.handle_action_port)
        self.register_entity_file('state.entity')
        self.register_entity_file('nums.entity')


    def handle_what_state(self, message):
        LOGGER.info("In what state")
        utterance = message.data.get('utterance')
        LOGGER.info("utterance: {0}".format(utterance))
        number =  message.data.get('nums')
        state = message.data.get('state')
        num1 =  int(extract_number(utterance))

        if number == '3' or number == '5' or number == '8':
            self.speak_dialog('portstatus', {'num': num1, 'state': PiPortState(num1)})
        else:
            self.speak_dialog('invalid.port.number', {'num': num1})

    def handle_action_port(self, message):
        LOGGER.info("In action port")
        utterance = message.data.get('utterance')
        LOGGER.info("utterance: {0}".format(utterance))
        state = message.data.get('state')
#        if state is not None:
#            LOGGER.info("State === not none")
#        else:
#            LOGGER.info("State === none")
        number = message.data.get('nums')
        num1 =  int(extract_number(utterance))
        if number == '3' or number == '5' or number == '8':
            if (number == '3' or number == '5' or number == '8') and (state == 'On' or state == 'on'): 
                GPIO.output(num1, GPIO.HIGH)
            if (number == '3' or number == '5' or number == '8') and (state == 'Off' or state == 'off'): 
                GPIO.output(num1, GPIO.LOW)
            self.speak_dialog('completed', {'num': number, 'state': state})
        else:
            self.speak_dialog('invalid.port.number', {'num': number})

    def handle_action2_port(self, message):
        LOGGER.info("In action2 port")
        utterance = message.data.get('utterance')
        LOGGER.info("utterance: {0}".format(utterance))
        state = message.data.get('state')
        LOGGER.info("State: {0}".format(state))
				
        xxx = utterance.upper().find("ALL")
        if (xxx != -1):
#            LOGGER.info("xxx: {0}".format(xxx))
            if (state.upper() == 'ON'):
                GPIO.output(3, GPIO.HIGH)
                GPIO.output(5, GPIO.HIGH)
                GPIO.output(8, GPIO.HIGH)
            if (state.upper() == 'OFF'):
                GPIO.output(3, GPIO.LOW)
                GPIO.output(5, GPIO.LOW)
                GPIO.output(8, GPIO.LOW)
            self.speak_dialog('Allcompleted', {'state': state})

			
			
def create_skill():
        return PiPortControl()


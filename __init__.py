from mycroft import MycroftSkill, intent_file_handler


class PiPortControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('control.port.pi.intent')
    def handle_control_port_pi(self, message):
        self.speak_dialog('control.port.pi')


def create_skill():
    return PiPortControl()


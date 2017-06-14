from abc import ABCMeta, abstractmethod


class UserInputMessage(object):

    __metaclass__ = ABCMeta

    __from_user__ = True

    def __init__(self, sender, message, message_type, image, location):
        self.sender = sender
        self.message = message
        self.message_type = message_type
        self.image = image
        self.location = location

    @abstractmethod
    def message_service(self):
        """"Return a string representing the service where message came from."""

# -*- coding: utf-8 -*-


class Robot(object):
    """
    Robot is the base class of user robots. it must implement `step` method.
    """
    def __init__(self):
        self.sock = None

    def step(self, data):
        """
        It must be implemented.
        """
        raise NotImplementedError()

    @classmethod
    def name(cls):
        """
        Returns the name of the class of the robot.
        """
        return cls.__name__

    def run(self):
        """
        Runs the robot.
        """
        if 'sock' not in self.__dict__:
            raise Exception("the socket has not been injected")
        while True:
            data = self.sock.recv(1048576).decode()  # 1 KiB
            res = self.step(data)
            self.sock.send(res.encode())

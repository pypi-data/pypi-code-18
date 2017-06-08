# -*- coding: utf-8 -*-


class Robot(object):
    """
    Robot is a simple class for the game engine to avoid using the original
    robot class. it handles the the robot process, score, and socket to the
    process.
    """

    def __init__(self, id):
        self.id = id
        self.score = 0
        self.sock = None
        self.process = None

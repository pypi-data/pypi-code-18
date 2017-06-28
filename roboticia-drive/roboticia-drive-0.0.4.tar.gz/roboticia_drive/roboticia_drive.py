from pypot.creatures import AbstractPoppyCreature

from .sensor import RPLidarA2, VoiceRecognition

class RoboticiaDrive(AbstractPoppyCreature):
    @classmethod
    def setup(cls, robot):
        for m in robot.motors:
            m.goto_behavior = 'dummy'
            m.moving_speed = 0
            
        sensor1 = RPLidarA2('RPLidar', 'normal')
        robot._sensors.append(sensor1)
        setattr(robot, sensor1.name, sensor1)
        
        sensor2 = VoiceRecognition('speech')
        robot._sensors.append(sensor2)
        setattr(robot, sensor2.name, sensor2)

        if robot.simulated:
            cls.vrep_hack(robot)


    @classmethod
    def vrep_hack(cls, robot):
        # fix vrep orientation bug
        wrong_motor = [robot.m3, robot.m2]
        
        for m in wrong_motor:
            m.direct = not m.direct
            #m.offset = -m.offset
            
        # use minjerk to simulate speed in vrep
        for m in robot.motors:
            m.goto_behavior = 'minjerk'

        

'''
'''

import pybullet as p

__all__ = ['Object', 'reset', 'step']

__version__ = '0.1.3'

shapes = {
    'box': p.GEOM_BOX,
    'sphere': p.GEOM_SPHERE,
    'capsule': p.GEOM_CAPSULE,
    'cylinder': p.GEOM_CYLINDER,
}

joints = {
    'revolute': p.JOINT_REVOLUTE,
    'prismatic': p.JOINT_PRISMATIC,
    'spherical': p.JOINT_SPHERICAL,
    'planar': p.JOINT_PLANAR,
    'fixed': p.JOINT_FIXED,
    'point_to_point': p.JOINT_POINT2POINT,
    'gear': p.JOINT_GEAR,
}

class Object:
    __slots__ = ['obj']

    def __init__(self, shape, mass, position, orientation=(0, 0, 0, 1), **kwargs):
        if 'size' in kwargs:
            width, height, length = kwargs['size']
            kwargs['halfExtents'] = (width / 2, height / 2, length / 2)
            del kwargs['size']

        shape = p.createCollisionShape(shapes[shape], **kwargs)
        self.obj = p.createMultiBody(
            baseMass=mass,
            basePosition=position,
            baseOrientation=orientation,
            baseCollisionShapeIndex=shape,
        )

    @property
    def position(self):
        return p.getBasePositionAndOrientation(self.obj)[0]

    @position.setter
    def position(self, value):
        p.resetBasePositionAndOrientation(self.obj, value, self.orientation)

    @property
    def orientation(self):
        return p.getBasePositionAndOrientation(self.obj)[1]

    @orientation.setter
    def orientation(self, value):
        p.resetBasePositionAndOrientation(self.obj, self.position, value)

    @property
    def velocity(self):
        return p.getBaseVelocity(self.obj)[0]

    @velocity.setter
    def velocity(self, value):
        p.resetBaseVelocity(self.obj, value, self.angular_velocity)

    @property
    def angular_velocity(self):
        return p.getBaseVelocity(self.obj)[1]

    @angular_velocity.setter
    def angular_velocity(self, value):
        p.resetBaseVelocity(self.obj, self.velocity, value)


class Constraint:
    __slots__ = ['obj']

    def __init__(self, joint, body1, body2, **kwargs):
        self.obj = p.createConstraint(body1.obj, -1, body2.obj, -1, joints[joint], **kwargs)


def reset(timestep=1/60, gravity=(0, 0, -9.8), gui=True):
    p.connect(p.GUI if gui else p.DIRECT)
    p.setRealTimeSimulation(0)
    p.resetSimulation()
    p.setTimeStep(timestep)
    p.setGravity(*gravity)


def step():
    p.stepSimulation()

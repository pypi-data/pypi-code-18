import numpy as np
from cyberglove.const import sensors_influence, joint_names
from scipy.optimize import minimize
from mujoco_py import load_model_from_mjb, MjSim

class Mapping():

    def __init__(self):
        self.x_dim = len(sensors_influence)
        self.y_dim = len(joint_names)
        self.mjb = None
        self.W = None
        self.shapes = None

    def train(self, sim, glove_recordings, poses):
        self.mjb = sim.model.get_mjb()
        self.sim = sim

        glove_recordings = [np.stack(g) for g in glove_recordings]

        for g in glove_recordings:
            std = np.max(np.std(g, axis=0))
            assert std > 0, "Recording has no variation. It's buggy"
            assert std < 80, "Recording has too much variation."
            assert g.shape[0] > 10, "Recording is too short."

        all_data = np.concatenate(glove_recordings)

        self.glove_min = np.min(all_data, axis=0, keepdims=True)
        self.glove_max = np.max(all_data, axis=0, keepdims=True)

        x = np.stack([np.mean(g, axis=0) for g in glove_recordings])
        y = np.stack(poses)

        self.limits = (np.min(y, axis=0), np.max(y, axis=1))

        # x is of size [None, 22]
        # W is of size [24, 23]
        # y is of size [None, 24]

        self.mask = np.zeros((self.x_dim + 1, self.y_dim))
        for sensor_idx, active in sensors_influence.items():
            for joint_idx, joint_name in enumerate(joint_names):
                for a in active:
                    if a in joint_name:
                        self.mask[sensor_idx, joint_idx] = 1
        print("Active entries in mask = %d / %d" % (np.sum(self.mask), np.prod(self.mask.shape)))
        self.mask[-1, :] = 1

        def score(W):
            pred = self.map(x, W)
            loss = np.mean(np.square(pred - y))
            print("loss = %f" % loss)
            return loss
        np.random.seed(0)
        W = np.random.randn(self.x_dim + 1, self.y_dim)
        ret = minimize(score, W, tol=1e-4, options={"maxiter": 1e5, "disp": True})
        self.W = ret.x

    def __getstate__(self):
        return {"mjb": self.mjb,
                "W": self.W,
                "glove_min": self.glove_min,
                "glove_max": self.glove_max,
                "mask": self.mask}

    def __setstate__(self, state):
        self.__init__()
        self.mjb = state["mjb"]
        model = load_model_from_mjb(self.mjb)
        self.sim = MjSim(model)
        self.W = state["W"]
        self.glove_min = state["glove_min"]
        self.glove_max = state["glove_max"]
        self.mask = state["mask"]

    def map(self, glove_recording, W=None):
        x = glove_recording
        if isinstance(x, (list, tuple)):
            x = np.array(x)
        if len(x.shape) == 1:
            x = np.expand_dims(x, 0)
        if W is None:
            W = self.W
        x = (x - self.glove_min) / (self.glove_max - self.glove_min)
        x = 2.0 * x - 1.0
        W = np.reshape(W, (self.x_dim + 1, self.y_dim))
        ret = np.matmul(np.concatenate([x, np.ones((x.shape[0], 1))], axis=1), W * self.mask)
        ret = (np.tanh(ret) + 1) / 2
        # Apply limits.
        for idx, name in enumerate(joint_names):
            jnt_range = self.sim.model.jnt_range[self.sim.model.joint_name2id(name)]
            diff = jnt_range[1] - jnt_range[0]
            ret[:, idx] *= diff * 1.2
            ret[:, idx] += jnt_range[0] - diff * 0.1
        return ret.squeeze()

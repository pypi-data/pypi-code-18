import numpy as np
class mabinter(object):
    def __init__(self,data,script):
        self.data = data
        self.script = script

    def inter(self,t,j,v):
        return np.floor(v) + self.v[t,j]

    def train(self,test_fun):
        self.test_fun = test_fun
        self.v = np.ones((self.script.T,self.script.J))
        cur_val = 0.
        for i in range(70):
            new_cur_val = self.bandit(cur_val)
            if new_cur_val == cur_val:
                break
            else:
                cur_val = new_cur_val

    def bandit(self,cur_val):
        T = self.script.T
        J = self.script.J
        
        stage = (T+J)*7
        eps = 0.2
        reward = {}
        pull_num = {}
        for i in range(stage):
            if i == 0:
                arm = (np.random.randint(T), np.random.randint(J))
                self.v[arm[0],arm[1]] = 1 - self.v[arm[0],arm[1]]
                m = np.random.randint(len(self.data)) - 1
                reward[arm] = self.test_fun(self.data[m])
                pull_num[arm] = 1
                self.v[arm[0],arm[1]] = 1 - self.v[arm[0],arm[1]]
                cur_max = reward[arm]
                best = arm
            else:
                if np.random.rand() < 1 - eps:
                    arm = best
                    self.v[arm[0],arm[1]] = 1 - self.v[arm[0],arm[1]]
                    m = np.random.randint(len(self.data)) - 1
                    reward[arm] += self.test_fun(self.data[m])
                    pull_num[arm] += 1
                    self.v[arm[0],arm[1]] = 1 - self.v[arm[0],arm[1]]
                    cur_max = reward[arm] / float(pull_num[arm])
                    for a in reward:
                        if reward[a] / float(pull_num[a]) > cur_max:
                            best = a
                            cur_max = reward[a] / float(pull_num[a])
                else:
                    arm = (np.random.randint(T), np.random.randint(J))
                    while arm == best[0]*T+best[1]:
                        arm = (np.random.randint(T), np.random.randint(J))
                    self.v[arm[0],arm[1]] = 1 - self.v[arm[0],arm[1]]
                    m = np.random.randint(len(self.data)) - 1
                    if arm not in reward.keys():
                        reward[arm] = self.test_fun(self.data[m])
                        pull_num[arm] = 1
                    else:
                        reward[arm] += self.test_fun(self.data[m])
                        pull_num[arm] += 1
                    self.v[arm[0],arm[1]] = 1 - self.v[arm[0],arm[1]]
                    if reward[arm] / float(pull_num[arm]) > cur_max:
                        best = arm
                        cur_max = reward[arm] / float(pull_num[arm])
        if cur_max > cur_val:
            self.v[best[0],best[1]] = 1 - self.v[best[0],best[1]]
            return cur_max
        else:
            return cur_val
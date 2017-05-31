class Progress(object):

    def __init__(self, step_max=0, path=None):
        self.step_max = float(step_max)
        self.path = path

    def step(self, step, percentage=True):
        progress = float(step)/self.step_max
        if percentage:
            progress *= 100.
            threshold = 100.
        else:
            threshold = 1.
        if self.path is not None:
            f = open(self.path, 'w')
            if progress != threshold:
                f.write(str(int(round(progress))))
            else:
                f.write('done')
            f.close()

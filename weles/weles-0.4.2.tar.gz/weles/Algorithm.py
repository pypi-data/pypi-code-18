from abc import ABCMeta, abstractmethod
import numpy as np

class Algorithm:
    __metaclass__ = ABCMeta
    def quickLoop(self):
        folds = xrange(0,5,1)
        acc = []
        bac = []
        for fold in folds:
            self.dataset.setCV(fold)
            self.learn()
            self.dataset.clearSupports()
            self.predict()
            scores = self.dataset.score()
            acc.append(scores['accuracy'])
            bac.append(scores['bac'])
        macc = np.mean(acc)
        mbac = np.mean(bac)
        return {'acc': macc, 'bac': mbac, 'wacc': acc, 'wbac': bac}

    @classmethod
    def __str__(cls):
        return 'NONE'

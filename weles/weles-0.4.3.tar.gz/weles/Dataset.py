from Sample import *
from utils import getType
import csv
import numpy as np
import random
import re

np.seterr(divide='ignore', invalid='ignore')

SEED = 123
FOLDS = 5
random.seed(SEED)

# DATASET
class Dataset(object):
    def __init__(self, filename=0, resample=0, pureLabels = True):
        #print 'PL %i' % pureLabels
        # Load db
        self.db_name = ""
        self.source_samples = []
        self.train = []
        self.test = []
        self.has_header = False
        self.header = []
        self.classes = {}
        self.resample = resample

        maxPureLabel = 0

        if filename:
            wisepath = re.findall(r"[\w']+", filename)
            self.db_name = wisepath[len(wisepath) - 2]

            with open(filename, 'rb') as file:
                csvDataset = csv.reader(file, delimiter=',')
                for row in csvDataset:
                    if getType(row[0]) == str:
                        self.hasHeader = True
                        self.header = row
                    else:
                        label = row[-1]
                        features = row[0:-1]
                        if pureLabels:
                            self.source_samples.append(Sample(features, int(label)))
                            if int(label) > maxPureLabel:
                                maxPureLabel = int(label)
                        else:
                            if not label in self.classes:
                                self.classes.update({label: len(self.classes)})
                            self.source_samples.append(Sample(features, self.classes[label]))

            if pureLabels:
                for i in xrange(maxPureLabel + 1):
                    self.classes.update({i: i})

            #print self.classes


            self.preAnalyze()

    def setFeatureFilter(self, featureFilter):
        #print 'ORIGINAL %s' % featureFilter
        #nFeatureFilter = [i for i in featureFilter]
        #print 'NEGATED %s' % nFeatureFilter
        self.featureFilter = featureFilter
        for sample in self.source_samples:
            sample.setFeatureFilter(self.featureFilter)
        self.preAnalyze()

    def export(self, filename):
        print 'EXPORTING'
        with open(filename, 'wb') as file:
            csvDataset = csv.writer(file, delimiter=',')
            for sample in self.source_samples:
                row = list(sample.getFeatures())
                row.append(sample.label)
                csvDataset.writerow(row)
                # print sample.

    def injectTrain(self, train):
        self.train = train
        self.samples = self.train
        self.scipyPrepare()

    def fill(self, db_name, source_samples, classes):
        self.db_name = db_name
        self.source_samples = source_samples
        self.classes = classes
        self.preAnalyze(normalisation = False)

    def preAnalyze(self, normalisation = True):
        self.confusion_matrix = []
        # normalize
        if normalisation:
            self.normalize()

        # dumb resampling
        if self.resample:
            random.shuffle(self.source_samples)
            self.source_samples = self.source_samples[0:self.resample]

        # Count features
        self.features = len(self.source_samples[0].getFeatures())

        # Initialize supports
        self.clearSupports()

        # Set base sample set
        self.samples = self.source_samples

        self.prepareCV()
        self.scipyPrepare()

    def scipyPrepare(self):
        # Scipy
        self.X = [x.getFeatures() for x in self.samples]
        self.y = [x.label for x in self.samples]
        self.testX = []

    def prepareCV(self):
        # Prepare CV
        indexes = range(0, len(self.source_samples))
        random.shuffle(indexes)

        self.cv = []
        for index, value in enumerate(indexes):
            self.cv.append((value, index % FOLDS))


    def clearSupports(self):
        for sample in self.source_samples:
            sample.support = np.zeros(len(self.classes))

    def __str__(self):
        return "%s dataset (%i samples, %i features, %i classes)" % (
            self.db_name,
            len(self.source_samples),
            self.features,
            len(self.classes)
        )

    def setCV(self,fold):
        self.samples = []
        self.test = []
        for pair in self.cv:
            if pair[1] == fold:
                self.samples.append(self.source_samples[pair[0]])
            else:
                self.test.append(self.source_samples[pair[0]]);

        if len(self.train):
            self.samples = self.train

        # SKL
        self.scipyPrepare()
        self.testX = [x.getFeatures() for x in self.test]

    def score(self):
        self.confusion_matrix = np.zeros((len(self.classes),len(self.classes))).astype(int)

        for sample in self.test:
            # print "\n# FILLING CONFUSION MATRIX"
            # print sample
            # print sample.label
            # print sample.prediction
            self.confusion_matrix[sample.label,sample.prediction] += 1

        true_positives = np.zeros(len(self.classes)).astype(float)
        false_negatives = np.zeros(len(self.classes)).astype(float)
        false_positives = np.zeros(len(self.classes)).astype(float)
        true_negatives = np.zeros(len(self.classes)).astype(float)

        for pro in xrange(0,len(self.classes)):
            true_positives[pro] += self.confusion_matrix[pro,pro]
            for contra in xrange(0,len(self.classes)):
                if pro == contra: continue
                false_negatives[pro] += self.confusion_matrix[pro,contra]
                false_positives[pro] += self.confusion_matrix[contra,pro]
            true_negatives[pro] = sum(sum(self.confusion_matrix)) - true_positives[pro] - false_negatives[pro] - false_positives[pro]

        sensitivity = true_positives / (true_positives + false_negatives)
        specificity = true_negatives / (false_positives + true_negatives)
        ppv = true_positives / (true_positives + false_positives)
        npv = true_negatives / (true_negatives + false_negatives)
        bac = (sensitivity + specificity) / 2

        acc = sum(true_positives + true_negatives) / sum(true_positives + true_negatives + false_positives + false_negatives)

        scores = \
        {
            'sensitivity': sensitivity.mean(),
            'specificity': specificity.mean(),
            'ppv': ppv.mean(),
            'npv': npv.mean(),
            'accuracy': acc,
            'bac': bac.mean()
        }

        return scores

    def normalize(self):
        example = np.array(self.source_samples[0].getFeatures())
        # Check if there are any NaN's
        for index, value in enumerate(example):
            if np.isnan(value):
                for sample in self.source_samples:
                    if not np.isnan(sample.getFeatures()[index]):
                        example[index] = sample.getFeatures()[index]
                        break

        minimum = np.array(list(example))
        maximum = np.array(list(example))

        for index, sample in enumerate(self.source_samples):
            for index, value in enumerate(sample.getFeatures()):
                if value < minimum[index]:
                    minimum[index] = value
                if value > maximum[index]:
                    maximum[index] = value

        self.normA = minimum
        self.normB = maximum - minimum
        foo = maximum - minimum

        # O tu sobie poradzmy z 0/0
        for index, value in enumerate(foo):
            if value == 0:
                foo[index] = 1

        for sample in self.source_samples:
            for index, feature in enumerate(sample.getFeatures()):
                if not np.isnan(feature):
                    normalizedFeature = (feature - minimum[index]) / foo[index]
                    sample.getFeatures()[index] = normalizedFeature

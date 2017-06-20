import random
from collections import defaultdict
from math import ceil

from tqdm import tqdm

from np_utils import append, concatenate


class Data(object):
    def __init__(self, shapes, dtypes, names):
        self.shapes = shapes
        self.dtypes = dtypes
        self.names = names

    @property
    def num_examples(self):
        raise NotImplementedError()

    def num_batches(self, batch_size, allow_partial=True):
        if allow_partial:
            return int(ceil(self.num_examples / batch_size))
        else:
            return int(self.num_examples / batch_size)

    def get(self, i, compact=False):
        raise NotImplementedError()

    def get_many(self, idxs, compact=False):
        raise NotImplementedError()

    def iter_batches(self, batch_size, shuffle=False, cycle=False, allow_partial=True, compact=False, sort_key=None, filter_key=None):
        assert isinstance(self, Data)
        idxs = list(range(self.num_examples))
        if filter_key is not None:
            idxs = [idx for idx in idxs if filter_key(idx)]
            print("Filtered data to yield {}/{} examples".format(len(idxs), self.num_examples))
        starts = list(range(0, len(idxs), batch_size))
        if sort_key is not None:
            if shuffle:
                random.shuffle(idxs)
                random.shuffle(starts)
            idxs.sort(key=sort_key)
        else:
            if shuffle:
                random.shuffle(idxs)
        while True:
            for start in starts:
                end = min(start + batch_size, len(idxs))
                if not allow_partial and (end - start) < batch_size:
                    break
                mini = self.get_many(idxs[start:end], compact=compact)
                yield mini
            if cycle:
                idxs = list(range(len(idxs)))
            else:
                break

    def get_placeholders(self):
        import tensorflow
        # batch size is None
        shapes, dtypes = self.shapes, self.dtypes
        if isinstance(self.shapes, dict):
            shapes = [self.shapes[name] for name in self.names]
        if isinstance(self.dtypes, dict):
            dtypes = [self.dtypes[name] for name in self.names]
        shapes = [None if isinstance(shape, int) else (None, ) + tuple(shape[1:]) for shape in shapes]
        return {name: tensorflow.placeholder(dtype, shape, name=name)
                for name, dtype, shape in zip(self.names, dtypes, shapes)}


class SmallData(Data):
    def __init__(self, shapes, dtypes, names, examples):
        super(SmallData, self).__init__(shapes, dtypes, names)
        self.examples = examples

    @property
    def num_examples(self):
        if len(self.examples) == 0:
            return 0
        return len(next(iter(self.examples.values())))

    def get(self, i, compact=False):
        return {key: each[i] for key, each in self.examples.items()}

    def get_many(self, idxs, compact=False):
        out = defaultdict(list)
        for idx in idxs:
            each = self.get(idx)
            for key, val in each.items():
                out[key].append(val)
        return out


class Evaluation(object):
    def __init__(self, data, inputs=None, outputs=None, loss=None, global_step=None):
        self.data = data
        self.inputs = inputs
        self.outputs = outputs
        self.loss = loss
        self.global_step = global_step

    @property
    def num_examples(self):
        n = 0 if self.inputs is None else len(next(iter(self.inputs.values())))
        return n

    def __repr__(self):
        return "global_step={}: {}".format(self.global_step, ", ".join("{}={:.4f}".format(key, val) for key, val in self.get_summary_values().items()))

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def __add__(self, other):
        if other == 0:
            return self
        assert isinstance(other, self.__class__)
        if self.loss is None or other.loss is None:
            loss = None
        else:
            if self.num_examples + other.num_examples == 0:
                loss = 0
            else:
                loss = (self.loss * self.num_examples + other.loss * other.num_examples) / (self.num_examples + other.num_examples)
        global_step = max(self.global_step, other.global_step)
        inputs, outputs = {}, {}
        if other.inputs is not None:
            for key, vals in other.inputs.items():
                if key in self.inputs:
                    inputs[key] = append(self.inputs[key], vals, axis=0)
                else:
                    inputs[key] = vals
        if other.outputs is not None:
            for key, vals in other.outputs.items():
                if key in self.outputs:
                    outputs[key] = append(self.outputs[key], vals, axis=0)
                else:
                    outputs[key] = vals
        return self.__class__(self.data, inputs=inputs, outputs=outputs, loss=loss, global_step=global_step)

    @classmethod
    def sum(cls, evals):
        inputs, outputs = {}, {}
        for key in evals[0].inputs.keys():
            each = concatenate([eval_.inputs[key] for eval_ in evals], axis=0)
            inputs[key] = each
        for key in evals[0].outputs.keys():
            each = concatenate([eval_.outputs[key] for eval_ in evals], axis=0)
            outputs[key] = each
        loss = sum(eval_.loss * eval_.num_examples for eval_ in evals) / sum(eval_.num_examples for eval_ in evals)
        global_step = evals[-1].global_step
        return cls(evals[-1].data, inputs=inputs, outputs=outputs, loss=loss, global_step=global_step)

    def get_summary_values(self):
        return {'loss': self.loss}

    def get_summaries(self, prefix):
        import tensorflow as tf
        summary_values = self.get_summary_values()
        summaries = [tf.Summary(value=[tf.Summary.Value(tag='{}/{}'.format(prefix, key), simple_value=val)])
                     for key, val in summary_values.items()]
        return summaries


def get_glove(glove_path, draft=False):
    word2vec = {}
    with open(glove_path, 'r') as fp:
        for i, line in tqdm(enumerate(fp), total=400000, desc='glove'):
            if draft and i == 4000:
                break
            tokens = line.strip().split(" ")
            word = tokens[0]
            vec = [float(each) for each in tokens[1:]]
            word2vec[word] = vec
        word2vec['<PAD>'] = word2vec['<UNK>'] = [0.0] * len(vec)
        return word2vec




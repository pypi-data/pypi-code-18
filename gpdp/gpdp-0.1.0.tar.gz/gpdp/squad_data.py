import json
import os
import random
from collections import Counter, defaultdict, OrderedDict
import operator

import logging
import nltk
import numpy as np
from tqdm import tqdm

from gpdp.data import Data, Evaluation
from utils import Color
from squad_evaluator import evaluate


class SquadData(Data):
    def __init__(self, config, train_data=None):
        """
        Data subclass for SQuAD
        :param config: needs to contain
        - serve: True | False
        - data_type: train | dev | test
        - squad_path
        - glove_dir
        - glove_size: 50 | 100 | 150 | 200 | 300
        - fresh: True | False
        - mode: train | eval
        - draft: True | False
        - word_count_th: int
        - out_dir
        :param train_data: SquadData instance
        """
        if train_data is not None:
            assert isinstance(train_data, self.__class__)
        self.data_type = config.data_type
        self.config = config
        self.train_data = train_data
        self.glove_path = os.path.join(config.glove_dir, "glove.6B.{}d.txt".format(config.glove_size))
        self._word2vec_dict = None
        if not os.path.exists(config.out_dir):
            os.makedirs(config.out_dir)
        self._common_path = os.path.join(config.out_dir, "common.json")
        self._metadata_path = os.path.join(config.out_dir, "metadata_{}.json".format(self.data_type))
        self._data_path = os.path.join(config.out_dir, "data_{}.json".format(self.data_type))
        names = ['x', 'xv', 'q', 'qv', 'y1', 'y2', 'x_len', 'q_len', 'idxs']
        if config.serve:
            self._common = dict()
            self._metadata = dict()
            self._data = defaultdict(list)
            self._shared = defaultdict(list)
            self.squad = {'data': []}
            _ = self.word2vec_dict  # for pre-load purpose
        else:
            self.load(update=True)
        self._num_examples = N = len(self._data['q'])
        self.idx2word_dict = {idx: word for word, idx in self._common['word2idx'].items()}
        shapes = {'x': [N, None], 'xv': [N, None],
                  'q': [N, None], 'qv': [N, None], 'y1': [N], 'y2': [N],
                  'x_len': [N], 'q_len': [N], 'idxs': [N]}
        dtypes = {'x': 'int64', 'xv': 'int64', 'q': 'int64', 'qv': 'int64', 'y1': 'int64', 'y2': 'int64',
                  'x_len': 'int64', 'q_len': 'int64', 'idxs': 'int64'}
        super(SquadData, self).__init__(shapes, dtypes, names)

    def load(self, update=False, squad=None):
        config = self.config
        if squad is None:
            with open(config.squad_path, 'r') as fp:
                self.squad = json.load(fp)
        else:
            self.squad = squad
        self._prepro(self.squad)
        self._common = self._get_common(self.squad)
        self._metadata = self._get_metadata(self.squad)
        self._data, self._shared = self._get_data(self.squad, self._metadata)
        # config.vocab_size = len(self._metadata['word2idx'])  # self._common['vocab_size']
        config.vocab_size = self._common['vocab_size']
        config.emb_mat = np.array(self._metadata['emb_mat'], dtype='float32')
        if update:
            config.max_context_size = max(len(xi) for xi in self._shared['x'])  # self._metadata['max_context_size']
            config.max_ques_size = max(len(qi) for qi in self._data['q'])  # self._metadata['max_ques_size']

    @property
    def num_examples(self):
        return self._num_examples

    def last_batch_size(self, batch_size):
        return self.num_examples % batch_size

    def _get(self, i, x_len, q_len):
        each = {}
        for key in self._data:
            val = self._data[key][i]
            if key.startswith("*"):
                key = key[1:]
                val = self._shared[key][val]
            if key in ['x', 'xv']:
                val = idxs2np(val, x_len)
            elif key in ['q', 'qv']:
                val = idxs2np(val, q_len)
            each[key] = val
        each['y1'] = self._data['y1s'][i][0]  # random.choice(self._data['y1s'][i])
        each['y2'] = self._data['y2s'][i][0]  # random.choice(self._data['y2s'][i])
        return each

    def get(self, i, compact=False):
        x_len = self._shared['x_len'][self._data['*x_len'][i]] if compact else self.config.max_context_size
        q_len = self._data['q_len'][i] if compact else self.config.max_ques_size
        return self._get(i, x_len=x_len, q_len=q_len)

    def get_many(self, idxs, compact=False):
        x_len = max(self._shared['x_len'][self._data['*x_len'][i]] for i in idxs) if compact else self.config.max_context_size
        q_len = max(self._data['q_len'][i] for i in idxs) if compact else self.config.max_ques_size
        out = defaultdict(list)
        for idx in idxs:
            each = self._get(idx, x_len, q_len)
            for key, val in each.items():
                out[key].append(val)
        out = dict(out.items())  # just to disable defaultdict
        return out

    def _prepro(self, squad):
        if not self.config.fresh and os.path.exists(self._common_path) and os.path.exists(self._metadata_path) and os.path.exists(self._data_path):
            return

        for article in tqdm(squad['data'], desc="{} prepro".format(self.config.data_type)):
            for para in article['paragraphs']:
                context = process_text(para['context'])
                context_words = word_tokenize(context)
                para['processed_context'] = context
                para['context_words'] = context_words
                for qa in para['qas']:
                    ques = process_text(qa['question'])
                    ques_words = word_tokenize(ques)
                    qa['processed_question'] = ques
                    qa['question_words'] = ques_words
            if self.config.draft:
                break

    def _get_common(self, squad):
        if self.train_data is not None:
            common = self.train_data._common
            return common
        if os.path.exists(self._common_path):
            with open(self._common_path, 'r') as fp:
                print("Loading common info at {}".format(self._common_path))
                common = json.load(fp)
                return common
        assert self.config.mode == 'train', "Need common file at {} for validation or test.".format(self._common_path)

        word_counter = Counter()

        for article in tqdm(squad['data'], desc="{} get_common".format(self.config.data_type)):
            for para in article['paragraphs']:
                context_words = para['context_words']
                for word in context_words:
                    word_counter[word] += len(para['qas'])
                for qa in para['qas']:
                    ques_words = qa['question_words']
                    for word in ques_words:
                        word_counter[word] += 1
            if self.config.draft:
                break

        vocab_words = ['<PAD>', '<UNK>'] + list(set(word for word, count in word_counter.items() if count >= self.config.word_count_th))
        word2idx_dict = {word: idx for idx, word in enumerate(vocab_words)}

        common = {'word2idx': word2idx_dict, 'vocab_size': len(word2idx_dict)}
        print("Dumping common at {}".format(self._common_path))
        with open(self._common_path, 'w') as fp:
            json.dump(common, fp)

        """
        # This is for tensorflow visualization; not used now
        print("Dumping emb_metadata at {}".format(self.config.emb_metadata_path))
        with open(self.config.emb_metadata_path, 'w') as fp:
            writer = csv.writer(fp, delimiter='\t')
            writer.writerows([[word] for word in vocab_words])
        """
        return common

    def _get_metadata(self, squad):
        if not self.config.fresh and os.path.exists(self._metadata_path):
            with open(self._metadata_path, 'r') as fp:
                print("Loading metadata info at {}".format(self._metadata_path))
                metadata = json.load(fp)
                return metadata

        max_context_size = 0
        max_ques_size = 0

        words = set()
        for article in tqdm(squad['data'], desc="{} get_metadata".format(self.config.data_type)):
            for para in article['paragraphs']:
                context_words = para['context_words']
                max_context_size = max(max_context_size, len(context_words))
                words |= set(context_words)
                for qa in para['qas']:
                    ques_words = qa['question_words']
                    max_ques_size = max(max_ques_size, len(ques_words))
                    words |= set(ques_words)
            if self.config.draft:
                break

        word2vec_dict = {word.lower(): self.word2vec_dict[word.lower()] for word in words if word in self.word2vec_dict}
        print("{}/{} words found in GloVe.".format(len(word2vec_dict), len(words)))
        vocab = ['<PAD>', '<UNK>'] + list(word2vec_dict)
        vec_size = len(next(iter(self.word2vec_dict.values())))
        word2vec_dict[vocab[0]] = [0.0] * vec_size
        word2vec_dict[vocab[1]] = [0.0] * vec_size
        idx2word_dict = {idx: word for idx, word in enumerate(vocab)}
        word2idx_dict = {idx: word for word, idx in idx2word_dict.items()}
        emb_mat = [word2vec_dict[idx2word_dict[idx]] for idx in range(len(vocab))]

        metadata = {'emb_mat': emb_mat, 'word2idx': word2idx_dict}
        with open(self._metadata_path, 'w') as fp:
            print("Dumping metadata at {}".format(self._metadata_path))
            json.dump(metadata, fp)
        return metadata

    def _get_data(self, squad, metadata):
        if not self.config.fresh and os.path.exists(self._data_path):
            with open(self._data_path, 'r') as fp:
                print("Loading data at {}".format(self._data_path))
                data, shared = json.load(fp)
                return data, shared

        # Switch this back to commented one for regular word indexing (not using glove)
        # TODO : enable switching between two methods
        word2idx_dict = self._common['word2idx']
        word2idx_dict_v = metadata['word2idx']

        x, rx, xv, rxv, q, qv, y1, y2 = [], [], [], [], [], [], [], []
        x_len, q_len = [], []
        sx, sx_len = [], []
        context_list, ques_list, ans_list, ids, idxs = [], [], [], [], []
        context_words_list, ques_words_list = [], []
        for article in tqdm(squad['data'], desc="{} get_data".format(self.config.data_type)):
            for para in article['paragraphs']:
                context = para['processed_context']
                context_words = para['context_words']
                xj = [word2idx(word2idx_dict, word) for word in context_words]
                xvj = [word2idx(word2idx_dict_v, word) for word in context_words]
                xj_len = len(context_words)
                for qa in para['qas']:
                    ques_list.append(qa['question'])
                    rxi = len(x)
                    ques = qa['processed_question']
                    id_ = qa['id']
                    idx = len(q)
                    ques_words = qa['question_words']
                    qi = [word2idx(word2idx_dict, word) for word in ques_words]
                    qvi = [word2idx(word2idx_dict_v, word) for word in ques_words]
                    qi_len = len(ques_words)

                    ans_text, yi1, yi2 = [], [], []
                    for ans in qa['answers']:
                        each_ans_start = ans['answer_start']
                        each_ans_stop = each_ans_start + len(ans['text'])
                        each_ans_text = context[each_ans_start:each_ans_stop]
                        each_yi1, each_yi2 = get_word_span(context, context_words, each_ans_start, each_ans_stop)
                        ans_text.append(each_ans_text)
                        yi1.append(each_yi1)
                        yi2.append(each_yi2)

                        phrase = get_phrase(context, context_words, (each_yi1, each_yi2))
                        if phrase != each_ans_text:
                            # print("'{}' != '{}'".format(phrase, each_ans_text))
                            logging.log(logging.DEBUG, "'{}' != '{}'".format(phrase, each_ans_text))

                    q.append(qi)
                    qv.append(qvi)
                    q_len.append(qi_len)
                    rx.append(rxi)
                    rxv.append(rxi)
                    ques_list.append(ques)
                    ids.append(id_)
                    idxs.append(idx)
                    ans_list.append(ans_text)
                    y1.append(yi1)
                    y2.append(yi2)
                    ques_words_list.append(ques_words)
                x.append(xj)
                xv.append(xvj)
                x_len.append(xj_len)
                context_list.append(context)
                context_words_list.append(context_words)
            if self.config.draft:
                break

        shared = {'x': x, 'xv': xv, 'x_len': x_len, 'context': context_list, 'context_words': context_words_list}
        data = {'*x': rx, 'q': q, 'y1s': y1, 'y2s': y2, '*x_len': rx, 'q_len': q_len, '*xv': rxv, 'qv': qv,
                '*context': rx, '*context_words': rx, 'ques': ques_list, 'ans': ans_list, 'ques_words': ques_words_list,
                'ids': ids, 'idxs': idxs}

        print("Dumping data at {}".format(self._data_path))
        with open(self._data_path, 'w') as fp:
            json.dump([data, shared], fp)

        return data, shared

    @property
    def word2vec_dict(self):
        if self._word2vec_dict is None:
            if self.train_data is not None:
                self._word2vec_dict = self.train_data.word2vec_dict
            else:
                self._word2vec_dict = get_word2vec(self.glove_path, draft=self.config.draft)
        return self._word2vec_dict

    def iter_batches(self, batch_size, shuffle=False, cycle=False, allow_partial=True, compact=False, sort_key=None, filter_key=None):
        if sort_key is None:
            sort_key = lambda idx: self._shared['x_len'][self._data['*x_len'][idx]]
        if filter_key is None:
            def filter_key(idx):
                x_pass = self._shared['x_len'][self._data['*x_len'][idx]] <= self.config.context_size_th
                q_pass = self._data['q_len'][idx] <= self.config.ques_size_th
                return x_pass and q_pass

        return super(SquadData, self).iter_batches(batch_size, shuffle=shuffle, cycle=cycle,
                                                   allow_partial=allow_partial, compact=compact, sort_key=sort_key, filter_key=filter_key)


def process_text(text):
    return text.replace("``", '" ').replace("''", '" ')


def word_tokenize(text):
    return [token.replace("``", '"').replace("''", '"') for token in nltk.word_tokenize(text)]


def word2idx(word2idx_dict, word):
    if word.lower() not in word2idx_dict:
        return 1
    return word2idx_dict[word.lower()]


def pad(l, size, pad_val=0):
    if len(l) > size:
        raise TooLongError()
    width = size - len(l)
    out = np.lib.pad(l, (0, width), 'constant', constant_values=pad_val)
    return out


class TooLongError(Exception):
    pass


def idxs2np(idxs, size, pad_val=0):
    out = pad(idxs, size, pad_val=pad_val)
    return out


def get_spans(text, tokens):
    """

    :param text:
    :param tokens:
    :return: a list of char-level spans, where each span is an exclusive range, i.e. (start, stop)
    """
    cur_idx = 0
    spans = []
    for token in tokens:
        cur_idx = text.find(token, cur_idx)
        assert cur_idx >= 0, "Text and tokens do not match."
        spans.append((cur_idx, cur_idx + len(token)))
        cur_idx += len(token)
    return spans


def get_word_span(context, words, start, stop):
    spans = get_spans(context, words)
    idxs = []
    for word_idx, span in enumerate(spans):
        if not (stop <= span[0] or start >= span[1]):
            idxs.append(word_idx)
    assert len(idxs) > 0, "context and words do not match, or start and stop are not valid indices."
    return idxs[0], idxs[-1]


def get_phrase(context, words, span):
    start, stop = span
    char_idx = 0
    char_start, char_stop = None, None
    for word_idx, word in enumerate(words):
        char_idx = context.find(word, char_idx)
        assert char_idx >= 0
        if word_idx == start:
            char_start = char_idx
        char_idx += len(word)
        if word_idx == stop:
            char_stop = char_idx
            break
    assert char_start is not None, (span, len(words), context, words, words[span[0]:span[1]+1])
    assert char_stop is not None, (span, len(words), context, words, words[span[0]:span[1]+1])
    phrase = context[char_start:char_stop]
    return phrase


def get_best_span(yp1, yp2, op=None, length=None):
    max_val = -10e9
    best_word_span = None
    best_start_index = 0
    if op is None:
        op = operator.mul
    if length is None:
        length =len(yp1)
    for j in range(length):
        val1 = yp1[best_start_index]
        if val1 <= yp1[j]:
            val1 = yp1[j]
            best_start_index = j

        val2 = yp2[j]
        if op(val1, val2) >= max_val:
            best_word_span = (best_start_index, j)
            max_val = op(val1, val2)

    assert best_word_span is not None
    assert best_start_index is not None
    return best_word_span, float(max_val)


def get_word2vec(glove_path, num_words=400000, draft=False):
    word2vec_dict = {}
    with open(glove_path, 'r') as fp:
        for idx, line in tqdm(enumerate(fp), total=num_words, desc="get_word2vec"):
            tokens = line.strip().split(" ")
            word = tokens[0]
            vec = list(map(float, tokens[1:]))
            word2vec_dict[word] = vec
            if draft and idx + 1 >= num_words / 100:
                break

    return word2vec_dict


class SquadEvaluation(Evaluation):
    def __init__(self, data, inputs=None, outputs=None, loss=None, global_step=None):
        """
        :param data: 
        :param inputs: 
        :param dict outputs: a dictionary  that contains 'yp1' and 'yp2', each with a list of integers. 
        :param float loss:
        :param int global_step: 
        """
        super(SquadEvaluation, self).__init__(data, inputs=inputs, outputs=outputs, loss=loss, global_step=global_step)
        self._acc = None
        self._score = None
        self._ratio = None

    def get_answers(self):
        idxs, xs_len = self.inputs['idxs'], self.inputs['x_len']
        logits1_list, logits2_list = self.outputs['logits1'], self.outputs['logits2']
        answers = {}
        for idx, logits1, logits2, x_len in zip(idxs, logits1_list, logits2_list, xs_len):
            each = self.data.get(idx)
            context, context_words, id_ = [each[key] for key in ['context', 'context_words', 'ids']]
            best_span, best_score = get_best_span(logits1, logits2, op=operator.add, length=x_len)
            # rx = self.data.data['*x'][idx]
            # context, context_words = self.data.shared['context'][rx], self.data.shared['context_words'][rx]
            answer = get_phrase(context, context_words, best_span)
            id_ = each['ids']
            answers[id_] = answer
        return answers

    @property
    def score(self):
        if self._score is not None:
            return self._score
        answers = self.get_answers()
        official = evaluate(self.data.squad['data'], answers)
        self._score = official
        return official

    @property
    def acc(self):
        if self._acc is not None:
            return self._acc
        y1, y2 = self.inputs['y1'], self.inputs['y2']  # [N]
        yp1, yp2 = self.outputs['yp1'], self.outputs['yp2']  # [N]
        acc1 = 100 * np.mean(np.equal(y1, yp1))
        acc2 = 100 * np.mean(np.equal(y2, yp2))
        acc = {'acc1': acc1, 'acc2': acc2}
        self._acc = acc
        return acc

    def get_summary_values(self):
        vals = OrderedDict()
        vals['acc1'] = self.acc['acc1']
        vals['acc2'] = self.acc['acc2']
        vals['loss'] = self.loss
        vals['em'] = self.score['exact_match']
        vals['f1'] = self.score['f1']
        return vals

    def get_results(self):
        idx2word_dict = self.data.idx2word_dict
        context_words = self.data._data['*context_words']
        ques_words = self.data._data['ques_words']
        idxs = self.inputs['idxs']
        x_len = self.inputs['x_len']
        q_len = self.inputs['q_len']
        y1 = self.inputs['y1']
        y2 = self.inputs['y2']
        yp1 = self.outputs['yp1']
        yp2 = self.outputs['yp2']
        results = {}
        context_list = []
        ques_list = []
        correct_list = []
        for idx, xi_len, qi_len, y1i, y2i, yp1i, yp2i, in zip(idxs, x_len, q_len, y1, y2, yp1, yp2):
            rxi = context_words[idx]
            qi = ques_words[idx]
            xi = self.data._shared['context_words'][rxi]
            context = []
            ques = []
            for j, (xij, _) in enumerate(zip(xi, range(xi_len))):
                word = xij
                context.append([word, y1i <= j <= y2i, yp1i <= j <=yp2i])
            for qij, _ in zip(qi, range(qi_len)):
                word = qij
                ques.append(word)
            context_list.append(context)
            ques_list.append(ques)
            correct_list.append(yp1i == y1i and yp2i == y2i)
        results['context'] = context_list
        results['ques'] = ques_list
        results['correct'] = correct_list
        return results

    def print_results(self, n=10, first_n=False):
        results = self.get_results()
        idxs = range(n) if first_n else random.sample(list(range(len(results['context']))), n)
        sampled_context_list = [results['context'][idx] for idx in idxs]
        sampled_ques_list = [results['ques'][idx] for idx in idxs]
        sampled_correct_list = [results['correct'][idx] for idx in idxs]
        for context, ques, correct in zip(sampled_context_list, sampled_ques_list, sampled_correct_list):
            print()
            print("Quesiton:", " ".join(ques))
            words = []
            for each in context:
                word = each[0]
                if each[1]:
                    word = Color.ul(word)
                if each[2]:
                    word = Color.bold(word)
                words.append(word)
            print("Context:", " ".join(words))
            print("Correct?:", correct)

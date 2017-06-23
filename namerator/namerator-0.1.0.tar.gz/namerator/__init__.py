'''
namerator
=========

Name generator, by generating characters based on frequencies of letter patterns

Usage:
    $ python namerator.py -n 5 elf_names.txt
    egil-gonamilin
    taedhorilie
    lalorahinduil
    cirduiel
    amrothrie

'''
import os
from math import sqrt
from random import gauss, seed, choice
from collections import Counter

__title__ = 'namerator'
__version__ = '0.1.0'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3+'
__copyright__ = 'Copyright 2017 Johan Nestaas'


def load(path):
    with open(path) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def _chop_name(name):
    lst = [x for x in name.lower().strip().split()[0]]
    return ['', '', '', ''] + lst + ['$']


def _inc_frequencies(chop, freqs):
    freqs[0] = freqs.get(0, Counter())
    for i in range(1, 5):
        freqs[i] = freqs.get(i, {})
    for i in range(3, len(chop)):
        a, b, c, d = chop[i-4], chop[i-3], chop[i-2], chop[i-1]
        char = chop[i]
        freqs[0].update([char])
        freqs[1][d] = freqs[1].get(d, Counter())
        freqs[1][d].update([char])
        freqs[2][c + d] = freqs[2].get(c + d, Counter())
        freqs[2][c + d].update([char])
        freqs[3][b + c + d] = freqs[3].get(b + c + d, Counter())
        freqs[3][b + c + d].update([char])
        freqs[4][a + b + c + d] = freqs[4].get(a + b + c + d, Counter())
        freqs[4][a + b + c + d].update([char])
    return freqs


def _calc_frequencies(names):
    freqs = {'len': Counter()}
    for name in names:
        freqs['len'].update([len(name)])
        chop = _chop_name(name)
        _inc_frequencies(chop, freqs)
    return freqs


def _combined_freqencies(freqs, last1, last2, last3, last4):
    freq = Counter()
    freq.update(freqs[1][last1])
    for i in range(5):
        freq.update(freqs[2].get(last2, []))
    for i in range(10):
        freq.update(freqs[3].get(last3, []))
    for i in range(25):
        freq.update(freqs[4].get(last4, []))
    return freq.most_common()


def _choose(common, over=0, letter_freqs=None):
    lst = []
    for char, num in common:
        if over < 0 and char == '$':
            continue
        lst += [char] * num
    if over >= 0:
        lst += ['$'] * dict(common).get('$', 1) * (over + 1)
    if not lst:
        return _choose(letter_freqs, over=over)
    return choice(lst)


def _calc_gauss(lens):
    expanded = []
    for l, num in lens:
        expanded += [l] * num
    mean = sum(expanded) / len(expanded)
    sigma = sum((mean - x)**2 for x in expanded)
    sigma /= len(expanded) - 1
    sigma = sqrt(sigma)
    return mean, sigma


def _generate(freqs):
    name = ''
    last1 = ''
    last2 = ''
    last3 = ''
    last4 = ''
    shortest = min(x for x, y in freqs['len'].most_common())
    # longest = max(x for x, y in freqs['len'].most_common())
    mean, sigma = _calc_gauss(freqs['len'].most_common())
    namelen = int(max(gauss(mean, sigma), shortest))
    while True:
        combined = _combined_freqencies(freqs, last1, last2, last3, last4)
        next_letter = _choose(combined, over=len(name) - namelen,
                              letter_freqs=freqs[0].most_common())
        if next_letter == '$':
            break
        name += next_letter
        last4 = last3 + next_letter
        last3 = last2 + next_letter
        last2 = last1 + next_letter
        last1 = next_letter
    return name


def name_generator(names):
    if isinstance(names, str) and os.path.isfile(names):
        names = load(names)
    names = set(names)
    freqs = _calc_frequencies(names)

    def generate():
        nonlocal names, freqs
        while True:
            name = _generate(freqs)
            if name in names:
                seed()
                continue
            return name

    return generate


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--num', '-n', type=int, default=10)
    parser.add_argument('--output', '-o')
    parser.add_argument('--freq-output', '-f')
    args = parser.parse_args()
    names = load(args.path)
    freqs = _calc_frequencies(names)
    if args.freq_output:
        dump = {}
        dump['len'] = freqs['len'].most_common()
        dump['frequency'] = freqs[0].most_common()
        dump['first'] = {k: v.most_common() for k, v in freqs[1].items()}
        dump['second'] = {k: v.most_common() for k, v in freqs[2].items()}
        dump['third'] = {k: v.most_common() for k, v in freqs[3].items()}
        dump['fourth'] = {k: v.most_common() for k, v in freqs[4].items()}
        with open(args.freq_output, 'w') as f:
            json.dump(dump, f, indent=4)
        print('Dumped frequencies to {args.freq_output}'.format(args=args))
    names = set(names)
    ct = 0
    if args.output is None:
        while ct < args.num:
            name = _generate(freqs)
            if name in names:
                seed()
                continue
            names.add(name)
            print(name)
            ct += 1
        return
    with open(args.output, 'w') as f:
        while ct < args.num:
            name = _generate(freqs)
            if name in names:
                seed()
                continue
            names.add(name)
            f.write(name + '\n')
            ct += 1
            if ct % 100 == 0:
                perc = float(ct) / args.num
                print('{:.2%} done'.format(perc))


if __name__ == '__main__':
    main()

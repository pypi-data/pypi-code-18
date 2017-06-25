# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 21:32:33 2017

@author: YudongCai
"""

import numpy as np
import pandas as pd
from collections import defaultdict


def loadcnvrfile(cnvfile, chromorder=None):
    """
    parse raw cnvcaller output format
    the first 8 columns are [chr, start, end, number, gap, repeat, gc, kmer]
    the last two columns are [average, sd]
    the in-between columns are each individual
    when chromorder was state, chromsome will be sorted as the given order, contings that not states will be remove, you can use this option to exclude some contigs
    """
    df = pd.read_csv(cnvfile, sep='\t', low_memory=False)
    df['chr'] = df['chr'].astype('str')  # chr is always str type
    df['chr'] = df['chr'].astype('category', categories=chromorder, ordered=True)
    if chromorder:
        df.dropna(inplace=True)  # contig that not listed in chromorder will be removed
        df = df.sort_values('chr')
    return df


def loadtwocol(infile):
    """
    load two columns file,
    save to a dict,
    with the first as keys the second as values
    """
    kvdict = {}
    with open(infile) as f:
        for nline, line in enumerate(f):
            line = line.strip()
            if line: # to exclude blank line
                k, v = line.split('\t')
                kvdict[k] = v
    return kvdict


def loadtwocol_dlist(infile):
    """
    load two columns file,
    save to a dict, value is list, the second col as k
    """
    kvdict = defaultdict(list)
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if line:
                k, v = line.split('\t')
                kvdict[v].append(k)
    return kvdict



def loadonecol(infile):
    """
    load one columns file,
    save as a list
    """
    slist = []
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if line: # exclude blank line
                slist.append(line)
    return slist





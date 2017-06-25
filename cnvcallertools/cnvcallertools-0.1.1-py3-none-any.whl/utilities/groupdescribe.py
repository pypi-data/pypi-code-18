# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 13:02:43 2017

@author: YudongCai
"""
import pandas as pd

def groupdescribe(df, gdict):
    """
    cnvdf
    groupdict
    """
    frames = {}
    infodf = df.loc[:, 'chr':'kmer']
    for gid, glist in gdict.items():
        frames[gid] = pd.concat([infodf, df.loc[:, glist].T.describe().T], axis=1)
    newdf = pd.concat(frames, axis=0).reset_index(level=0)
    assert newdf.columns.tolist()[0] == 'level_0'
    newcol = newdf.columns.tolist()
    newcol[0] = 'group'
    newdf.columns = newcol
    newdf = newdf.sort_values(['chr', 'start', 'end', 'number', 'gap', 'repeat', 'gc', 'kmer', 'group']).loc[:, ['chr', 'start', 'end', 'number', 'gap', 'repeat', 'gc', 'kmer', 'group', 'count', 'mean', 'std','min','25%','50%','75%','max']]
    return newdf


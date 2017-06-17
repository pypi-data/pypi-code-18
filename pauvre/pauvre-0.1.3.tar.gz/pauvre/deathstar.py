#!/usr/bin/env python
# pauvre - just a pore PhD student's plotting package
# Copyright (c) 2016-2017 Darrin T. Schultz. All rights reserved.
#
# This file is part of pauvre.
#
# pauvre is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pauvre is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pauvre.  If not, see <http://www.gnu.org/licenses/>.

#things to do
# - make the program determine if the sam file has a header or not.
# - figure out how to update rcParams every time we run a program
# - figure out if the poretools logger is actually doing anything
# - Write a better docstring for how plotArc works.
# - Write a docstring for seqOrder method. I don't remember what it does
# - write a better function to get the alignment length of the sam/bam file
#    right now it opens the file twice and only gets the length the first time
# - drop columns by name, not by column number (samFile.drop...)
#   - Here's another that needs to be fixed: samFile.drop(samFile.columns[3], axis=1, inplace=True)
# - args
#   - get the filename from args
#   - set up a double-mapped mode to wrap reads around the 0th coordinate for
#      circular assemblies
#   - Make the r-dist something that the user can change.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
import itertools
import pandas as pd
import numpy as np
import scipy as sp
import os, sys

# import the pauvre rcParams
from pauvre import rcparams

#logging
import logging
logger = logging.getLogger('pauvre')

def cigar_parse(myString):
    """
    arguments:
     <myString> a CIGAR string format in a python string type.

    purpose:
     This function splits the string at every integer and returns a
     list of tuples, [(20, 'M'), (5, "I")], et cetera. The zeroth
     element of each tuple is the number of bases for the CIGAR string
     feature. The first element of each tuple is the CIGAR string
     feature type.

    There are several feature types in SAM/BAM files. See below:
     'M' - match
     'I' - insertion relative to reference
     'D' - deletion relative to reference
     'N' - skipped region from the reference
     'S' - soft clip, not aligned but still in sam file
     'H' - hard clip, not aligned and not in sam file
     'P' - padding (silent deletion from padded reference)
     '=' - sequence match
     'X' - sequence mismatch

    """
    # I forget where this bit of code is from, probably stack overflow somewhere.
    A =  ["".join(x) for _, x in itertools.groupby(myString, key=str.isdigit)]
    return [(int(A[i]),A[i+1]) for i in range(0,len(A),2)]

def aln_len(TUPS):
    """
    arguments:
     <TUPS> a list of tuples output from the cigar_parse() function.

    purpose:
     This returns the alignment length of the read to the reference.
     Specifically, it sums the length of all of the matches and deletions.
     In effect, this number is how long the read aligns to on the reference
     sequence. This number is probably the most useful for selecting reads to
     visualize in the mapped read plot.
    """
    return sum([pair[0] for pair in TUPS if pair[1] not in ['S', 'H', 'I']])

def map_len(TUPS):
    """
    arguments:
     <TUPS> a list of tuples output from the cigar_parse() function.

    purpose:
     This function returns the map length (all matches and deletions relative to
     the reference), plus the unmapped 5' and 3' hard/soft clipped sequences.
     This number is useful if you want to visualize how much 5' and 3' sequence
     of a read did not map to the reference. For example, poor quality 5' and 3'
     tails are common in Nanopore reads.
    """
    return sum([pair[0] for pair in TUPS if pair[1] not in ['I']])

def tru_len(TUPS):
    """
    arguments:
     <TUPS> a list of tuples output from the cigar_parse() function.

    purpose:
     This function returns the total length of the read, including insertions,
     deletions, matches, soft clips, and hard clips. This is useful for
     comparing to the map length or alignment length to see what percentage of
     the read aligned to the reference.
    """
    return sum([pair[0] for pair in TUPS])

def fix_pos(start_index):
    """
    arguments:
     <TUPS> a list of tuples output from the cigar_parse() function.

    purpose:
     When using a doubled SAMfile, any reads that start after the first copy
     of the reference risk running over the plotting window, causing the program
     to crash. This function corrects for this issue by changing the start site
     of the read.

    Note: this will probably break the program if not using a double alignment
    since no reads would map past half the length of the single reference
    """
    if start_index > int(seqLen/2):
        return start_index - int(seqLen/2) - 1
    else:
        return start_index

def seqOrder(numSeqs):
    """ Write docstring for this. I don't remember what it does."""
    if numSeqs % 2 == 0:
        l1 = np.arange(0, numSeqs, 2)
        l2 = np.arange(numSeqs-1, 0, -2)
    else:
        l1 = np.arange(0, numSeqs, 2)
        l2 = np.arange(numSeqs-2, 0, -2)
    return [val for pair in zip(l1, l2) for val in pair]

def plotArc(start_angle, stop_angle, radius, width, **kwargs):
    """ write a docstring for this function"""
    numsegments = 100
    theta = np.radians(np.linspace(start_angle+90, stop_angle+90, numsegments))
    centerx = 0
    centery = 0
    x1 = -np.cos(theta) * (radius)
    y1 = np.sin(theta) * (radius)
    stack1 = np.column_stack([x1, y1])
    x2 = -np.cos(theta) * (radius + width)
    y2 = np.sin(theta) *  (radius + width)
    stack2 = np.column_stack([np.flip(x2, axis=0), np.flip(y2,axis=0)])
    #add the first values from the first set to close the polygon
    np.append(stack2, [[x1[0],y1[0]]], axis=0)
    arcArray = np.concatenate((stack1,stack2), axis=0)
    return patches.Polygon(arcArray, True, **kwargs)

def fix_query_reflength(seqLen, queries):
    """
    arguments:
     <seqLen> This is the reference fasta length. It should be 2x the actual
               length of the reference since this program takes a sam file from
               a concatenated reference.
     <queries> This is a list of SQL-type query strings. This is generated
                from argparse.

    purpose:
     This function takes in a list of queries to use for read filtering
     for the deathstar plot. It is often not advisable to plot all mapped reads
     since many of them are too small relative to the reference length. Also,
     the point of a death star plot is to show continuity of a circular
     reference, so short reads aren't very helpful there either.

     Currently, this function only recognizes the keyword argument 'reflength'.
    """
    print("hey I'm in here")
    for i in range(len(queries)):
        if 'reflength' in queries[i].split():
            queries[i] = queries[i].replace('reflength', str(int(seqLen/2)))

def deathstar(args):
    print(args)
    filename = args.sam
    global seqLen
    seqLen = 0
    #this function just exists to find the length of the alignment.
    # In the future, write a more efficient way to get the length
    with open(filename, 'r') as f:
        count = 0
        for line in f:
            if line.strip() and count < 3:
                search = line.strip().split()
                for element in search:
                    if "LN:" in element:
                        seqLen = int(element.replace('LN:',''))
                        print("found seqLen: {}".format(seqLen))
                count += 1
    if seqLen == 0:
        print(
    """You have used a SAM file with no header. Please add a header to
                 the sam file.
       Use `samtools faidx ref.fa; samtools view -ht ref.fa.fai myfile.sam`,
        where ref.fa is the fasta file to which your reads are mapped""")

    # This stops numpy from printing numbers in scientific notation.
    np.set_printoptions(suppress=True)

    # this also needs to be changed depending on if it was a concatenated SAM
    # if circular = true, then use linspace between 0,720
    # if circular = false, then use linspace between 0, 360
    # on second thought, it might not be necessary to change this value even
    #  for doubled sequences
    angleMap = np.linspace(0,720,seqLen)

    #these are the line width for the different cigar string flags.
    # usually, only M, I, D, S, and H appear in bwa mem output
    widthDict = {'M':0.45, # match
                 'I':0.9,  # insertion relative to reference
                 'D':0.05, # deletion relative to reference
                 'N':0.1,  # skipped region from the reference
                 'S':0.1,  # soft clip, not aligned but still in sam file
                 'H':0.1,  # hard clip, not aligned and not in sam file
                 'P':0.1,  # padding (silent deletion from padded reference)
                 '=':0.1,  # sequence match
                 'X':0.1}  # sequence mismatch

    #these are the known column names for what appears in the sam file
    myCols = ['QNAME',  'FLAG', 'RNAME',  'POS', 'MAPQ',
              'CIGAR', 'RNEXT', 'PNEXT', 'TLEN',  'SEQ',
              'QUAL',   'TAG1',  'TAG2', 'TAG3', 'TAG4',
              'TAG5',   'TAG6',  'TAG7', 'TAG8', 'TAG9']
    #read in the samfile and skip the header, we know it has a header because
    # the program would have already crashed if not.
    samFile = pd.read_table(filename, sep='\t', names=myCols, header=None, skiprows=[0,1,2])
    #drop the unneeded columns
    samFile.drop(samFile.columns[np.array([2, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,19,20])-1], axis=1, inplace=True)
    #calculate the various lengths of the read based on how they map.
    samFile['TUPS'] = samFile['CIGAR'].apply(cigar_parse)
    samFile['ALNLEN'] = samFile['TUPS'].apply(aln_len)
    samFile['TRULEN'] = samFile['TUPS'].apply(tru_len)
    samFile['MAPLEN'] = samFile['TUPS'].apply(map_len)
    samFile['POS'] = samFile['POS'].apply(fix_pos)
    #also fix this
    samFile.drop(samFile.columns[3], axis=1, inplace=True)

    #turn the query string into something usable,
    #  get rid of variables from argparse
    fix_query_reflength(seqLen, args.query)
    # string all the queries together
    queryString = " and ".join(args.query)
    print("You are using this query string to filter reads:\n'{}'".format(queryString))
    samFile = samFile.query(queryString)

    # now determine how to sort the reads in the order they will be plotted
    if args.small_start == 'inside':
        ascend = True
    elif args.small_start == 'outside':
        ascend = False
    samFile.sort_values(by=args.sort, ascending=ascend, inplace=True)
    samFile = samFile.reset_index()

    ##################
    # PLOT SOME PLOTS
    ##################

    figWidth = 5
    figHeight = 3

    fig_1 = plt.figure(figsize=(figWidth, figHeight))

    circleDiameter = 2.0

    leftMargin = 0.5
    bottomMargin = 0.5

    panelCircle =  plt.axes([leftMargin/figWidth, #left
                             bottomMargin/figHeight,  #bottom
                             circleDiameter/figWidth, #width
                             circleDiameter/figHeight     #height
                             ],frameon=False)
    panelCircle.tick_params(axis='both',which='both',\
                       bottom='off', labelbottom='off',\
                       left='off', labelleft='off', \
                       right='off', labelright='off',\
                       top='off', labeltop='off')

    numseqs = len(samFile.index) + 2
    panelCircle.set_xlim([-15 - numseqs, 15 + numseqs])
    panelCircle.set_ylim([-15 - numseqs, 15 + numseqs])

    myPatches = []
    rows = np.arange(0, len(samFile.index))

    #change this?
    r_dist = 10
    for i in rows:
        stringTuples = samFile.loc[i, 'TUPS']
        #I've completely forgotten why I subtract one from here.
        start_index = samFile.loc[i, 'POS'] - 1
        start_angle= angleMap[start_index]
        stop_index = 0
        stop_angle = angleMap[stop_index]
        for tup in stringTuples:
            if tup[1] == 'I':
                #If there is an insertion, back up halfway and make plot the
                # insertion to visually show a "bulge" with too much sequence.
                # do not advance the start index to resume normal plotting
                # after the insertion.
                iStartIndex = start_index-int(tup[0]/2)
                iStopIndex = iStartIndex + tup[0]
                iStartAngle = angleMap[iStartIndex]
                iStopAngle = angleMap[iStopIndex]
                arc = plotArc(start_angle=iStartAngle, stop_angle=iStopAngle, radius=r_dist, 
                              width=widthDict[tup[1]], fc='black')
            else:
                stop_index = start_index + tup[0]
                stop_angle = angleMap[stop_index]
                #myPatches.append(patches.Arc((0,0), r_dist, r_dist, 90, 360-stop_angle, 360-start_angle, ec='black', ls='-', lw=widthDict[tup[1]]))
                arc = plotArc(start_angle=start_angle, stop_angle=stop_angle, radius=r_dist, 
                              width=widthDict[tup[1]], fc='black')
                start_index = stop_index
                start_angle = angleMap[start_index]

            myPatches.append(arc)
        r_dist += 1

    for patch in myPatches:
        panelCircle.add_patch(patch)

    plt.show()
    #plt.savefig('/Users/darrin/git/lab_notebook_DTS/files/20170405_Wed/gD122nano_to_2013_ALNLENgt10000aMAPLENltSeqLen_ALNLEN_desc_2400dpi.png', dpi=2400, transparent=False, frameon=True, fc='white')

def run(parser, args):
    deathstar(args)

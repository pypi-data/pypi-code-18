#!/usr/bin/env python

"""
Read protein match output produced by noninteractive-alignment-panel.py and
group it by pathogen (either virus or bacteria).

This is currently only useful when you are matching against a subject protein
database whose titles have a pathogen name in square brackets, like this:

gi|820945251|ref|YP_009137096.1| envelope glycoprotein H [Human herpesvirus 1]
gi|820945301|ref|YP_009137146.1| virion protein US10 [Human herpesvirus 1]
gi|820945229|ref|YP_009137074.1| ubiquitin E3 ligase ICP0 [Human herpesvirus 1]

In this case, those three matched subjects are from the same pathogen. This
script will gather those matches under their common "Human herpesvirus 1"
title and provides methods to print them.

Files with names in this format are provided by NCBI for their viral and
bacterial refseq protein FASTA.

The script reads *file names* from standard input, and writes to standard
output.  Alternately, you can also provide file names on the command line.

Typical usage:

  $ find . -name summary-proteins | proteins-to-pathogens.py \
        --sampleNameRegex '(Sample_\d+)/' --html > index.html

Input files must contain lines in the following format:

0.77 47.00 48.10  5  5  74 gi|101105594| ubiquitin [Brazilian marseillevirus]
0.31 42.70 48.10 47 47 630 gi|313768007| protein BpV1_008c [Bathycoccus virus]
0.21 42.00 48.10 42 42 687 gi|313768010| protein BpV1_011c [Bathycoccus virus]
0.77 46.60 48.10  5  5  74 gi|327409793| ubiquitin [Lausannevirus]
0.33 42.70 48.10 48 48 624 gi|472342805| protein 70 [Micromonas pusilla virus]

Fields must be whitespace separated. The seven fields are:

    Coverage
    Median bit score
    Best bit score
    Read count
    HSP count
    Protein length
    Title (in the format "protein name [pathogen name]")
"""

from __future__ import print_function
import argparse
import sys
from itertools import chain

# It's not clear that the PDF backend is the right choice here, but it
# works (i.e., the generation of PNG images works fine).
import matplotlib
matplotlib.use('PDF')

# These imports are here because dark.proteins imports matplotlib.pyplot
# and we need to set the matplotlib backend before the import. So please
# don't move this import higher in this file.

from dark.proteins import ProteinGrouper


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Group proteins by the pathogen they're from.")

    parser.add_argument(
        'filenames', nargs='*', help='Sample file names to read input from.')

    parser.add_argument(
        '--sampleNameRegex', default=None,
        help=('An (optional) regular expression that can be used to extract a '
              'short sample name from full sample file name.  The regular '
              'expression must have a matching group (delimited by '
              'parentheses) that captures the part of the file name that '
              'should be used as the sample name.'))

    parser.add_argument(
        '--pathogenPanelFilename', default=None,
        help=('An (optional) filename to write a pathogen-sample panel PNG '
              'image to.'))

    parser.add_argument(
        '--html', default=False, action='store_true',
        help='If specified, output HTML instead of plain text.')

    parser.add_argument(
        '--format', default='fasta', choices=('fasta', 'fastq'),
        help=('Give the format of the sequence files written by '
              'noninteractive-alignment-panel.py when it created the '
              'summary-proteins files given on output.'))

    parser.add_argument(
        '--proteinFastaFilename', '--pff', nargs='+', action='append',
        help=('Optional filename(s) giving the name of the FASTA file(s) '
              'with the protein AA sequences with their associated pathogens '
              'in square brackets. This is the format used by NCBI for '
              'bacterial and viral reference sequence protein files. If '
              'given, the contents of this file will be used to determine how '
              'many proteins each matched pathogen has. This makes it much '
              'easier to spot significant matches (as opposed to those where, '
              'say, just one protein from a pathogen is matched).'))

    parser.add_argument(
        '--minProteinFraction', type=float, default=0.0,
        help=('The minimum fraction of proteins in a pathogen that must be '
              'matched by at least one sample in order for that pathogen to '
              'be displayed.'))

    parser.add_argument(
        '--pathogenType', default='viral', choices=('bacterial', 'viral'),
        help=('Specify the pathogen type. This option only affects the '
              'language used in HTML output.'))

    args = parser.parse_args()

    if args.proteinFastaFilename:
        # Flatten lists of lists that we get from using both nargs='+' and
        # action='append'. We use both because it allows people to use
        # (e.g.)  --pff on the command line either via "--pff file1 --pff
        # file2" or "--pff file1 file2", or a combination of these. That
        # way it's not necessary to remember which way you're supposed to
        # use it and you also can't be hit by the subtle problem
        # encountered in https://github.com/acorg/dark-matter/issues/453
        proteinFastaFilenames = list(chain.from_iterable(
            args.proteinFastaFilename))
    else:
        proteinFastaFilenames = None

    grouper = ProteinGrouper(sampleNameRegex=args.sampleNameRegex,
                             format_=args.format,
                             proteinFastaFilenames=proteinFastaFilenames)

    if args.filenames:
        filenames = args.filenames
    else:
        filenames = (line[:-1] for line in sys.stdin)

    for filename in filenames:
        with open(filename) as fp:
            grouper.addFile(filename, fp)

    if args.html:
        print(grouper.toHTML(args.pathogenPanelFilename,
                             minProteinFraction=args.minProteinFraction,
                             pathogenType=args.pathogenType))
    else:
        print(grouper.toStr())

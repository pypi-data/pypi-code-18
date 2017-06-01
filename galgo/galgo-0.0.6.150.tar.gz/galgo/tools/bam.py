from __future__ import print_function
from argtools import command, argument
import pysam
from pysam import Samfile
import re
import logging
from collections import namedtuple
from builtins import filter, zip, map
from itertools import groupby
from ..utils import fill_text, Counter, cached_property
from ..bioseq import color_term_dna, get_aln_pos_text, dna_revcomp, Fasta
from ..samutil import LocalInfo, sam_intervals, Read
from ..samutil import aln2cigar, Cigar
from operator import attrgetter


@command.add_sub
@argument('bamfile')
@argument('-l', '--is-list', action='store_true')
@argument('-t', '--tags', help='comma separated tags (e.g. RG)')
def bam_header2tab(args):
    """
    USAGE: bam_haeder2tab {bam_list} -l -t RG
    """
    tag1_set = set(args.tags.split(','))
    #tags = args.tags.split(',')
    fnames = []
    fn_recs = []
    if args.is_list:
        bamfiles = [line.rstrip() for line in open(args.bamfile)]
    else:
        bamfiles = [args.bamfile]
    for bam in bamfiles:
        sam = pysam.Samfile(bam)
        fnames.append(sam.filename)
        fn_recs.append((sam.filename, sam.header))
        sam.close()

    # header
    # {tag1: [{tag2: cont}]}
    def gather_tags(fn_recs):
        """
        Returns: set(['PG', 'RG.ID', 'RG.SM', ...]), {'PG': ..., 'RG.ID': ..., ...})
        """
        tag_set = set()
        out_recs = []
        for fn, recs in fn_recs:
            for tag1, rec1s in recs.items():
                if tag1_set and tag1 not in tag1_set:
                    continue
                for rec1 in rec1s:
                    out_rec = {'fname': fn}
                    if isinstance(rec1, dict):
                        for tag2, rec2 in rec1.items():
                            tag = tag1 + '.' + tag2
                            tag_set.add(tag)
                            out_rec[tag] = rec2
                    else:
                        tag = tag1
                        tag_set.add(tag)
                        out_rec[tag] = rec2
                    out_recs.append(out_rec)
        return tag_set, out_recs

    tag_set, out_recs = gather_tags(fn_recs)
    keys = list(sorted(tag_set)) + ['fname']

    print (*keys, sep='\t')
    for rec in out_recs:
        out = [rec.get(key, '.') for key in keys]
        print (*out, sep='\t')


@command.add_sub
@argument('bamfile')
@argument('bamout')
@argument('-u', '--unpaired')
@argument('-f', '--uncount-flag', type=lambda x: int(x, 16), default=0x900, help='uncount-flag for existing reads; default is secondary or supplementary reads')
def bam_discard_unpaired(args):
    sam = pysam.Samfile(args.bamfile)
    read1s = set()
    read2s = set()
    uncount_flag = args.uncount_flag
    for rec in sam:
        if rec.flag & uncount_flag:
            continue
        if rec.is_read1:
            read1s.add(rec.qname)
        else:
            read2s.add(rec.qname)

    paired = read1s & read2s
    unpaired = (read1s - paired) | (read2s - paired)
    logging.info('Paired reads: %s', len(paired))
    logging.info('Unpaired reads: %s', len(unpaired))

    sam.reset()
    out = pysam.Samfile(args.bamout, mode='wb', template=sam)
    out2 = pysam.Samfile(args.unpaired, mode='wb', template=sam) if args.unpaired else None
    for rec in sam:
        if rec.qname in paired:
            # workaround for avoiding duplicated emission of the same record
            if rec.is_read1:
                if rec.qname in read1s:
                    out.write(rec)
                    read1s.remove(rec.qname)
            else:
                if rec.qname in read2s:
                    out.write(rec)
                    read2s.remove(rec.qname)
        elif out2:
            out2.write(rec)



class SamReadInfo(object):
    """ TODO write test
    """

    def __init__(self, rec, _saminfo):
        self._info = _saminfo
        self.rec = rec

    @cached_property
    def edit(self):
        tag = dict(self.rec.get_tags())
        edit = tag.get('NM', 0)
        return edit

    @cached_property
    def _cigar(self):
        return Cigar(self.rec.cigartuples)

    @property
    def lclip(self):
        return self._cigar.lclip

    @property
    def rclip(self):
        return self._cigar.rclip

    @cached_property
    def overhang(self):   # TODO how to consider region filled with N bases ?
        return max(self.left_overhang, self.right_overhang)

    @cached_property
    def left_overhang(self):
        if self.rec.is_unmapped:
            return 0
        if self._cigar.lclip > 0:
            return min(self.rec.pos, self._cigar.lclip)
        else:
            return 0

    @cached_property
    def right_overhang(self):
        if self.rec.is_unmapped:
            return 0
        rclip = self._cigar.rclip
        if rclip:
            rdist = self._info._lengths[self.rec.tid] - self.rec.aend
            return min(rclip, rdist)
        else:
            return 0


class SamInfo(object):
    def __init__(self, sam):
        """
        sam: pysam.Samfile object
        """
        self._sam = sam
        self._filters = []
        self._lengths = {sam.get_tid(name): length for name, length in zip(sam.references, sam.lengths)}

    def get_length(self, refname):
        return self._lengths[self._sam.get_tid(refname)]

    def get_read_info(self, rec):
        return SamReadInfo(rec, _saminfo=self)


@command.add_sub
@argument('bamfile')
@argument('-l', '--list')
@argument('--max-edit', type=int, help='use NM tag')
@argument('--max-overhang', type=int, help='set limit to overhang length between read and reference')
@argument('-o', '--output', default='/dev/stdout')
def bam_filter(args):
    sam = pysam.Samfile(args.bamfile)
    if args.output.endswith('.bam'):
        mode = 'wb'
    else:
        mode = 'wh'
    out = pysam.Samfile(args.output, mode=mode, template=sam)
    max_edit = args.max_edit
    max_overhang = args.max_overhang

    saminfo = SamInfo(sam)
    it = map(saminfo.get_read_info, sam)
    if args.list:
        white_list = set([name.rstrip() for name in open(args.list)])
        cond = lambda read: read.rec.qname in white_list
        it = filter(cond, it)

    if args.max_edit is not None:
        cond = lambda read: read.edit <= max_edit
        it = filter(cond, it)

    if args.max_overhang is not None:
        cond = lambda read: read.overhang <= max_overhang
        it = filter(cond, it)

    for read in it:  # fetch only primary and non-supplementary reads
        out.write(read.rec)


@command.add_sub
@argument('bamfile')
@argument('-r', '--region')
def bam_profile(args):
    """
    """
    sam = pysam.Samfile(args.bamfile)
    attrs = ['name', 'read1', 'unmapped', 'suppl', 'num_frags', 'qlen', 'rname', 'start', 'end', 'alen', 'mapq', 'reverse', 'lclip', 'rclip', 'edit', 'nins', 'ndel']
    getter = attrgetter(*attrs)
    with sam:
        print (*(attrs + ['tags_md']), sep='\t')
        for rec in sam.fetch(args.region):
            r = Read(rec)
            print (*(getter(r) + (dict((k, v) for k, v in rec.tags if k != 'MD'),)), sep='\t')


# TODO sort by read_name, read_length, ref_identity, ref_diversity <= weighted identity (using base probability as weight is ok)
# show read properties (mismatch on reads
@command.add_sub
@argument('bam')
@argument('region', nargs='+')  # TODO currently, need this option
@argument('-r', '--reference')
@argument('-c', '--color-base', action='store_true')
@argument('-m', '--mask-ref-base', action='store_true')
@argument('--order', help='sort orders: select from qname, edit, nins, ndel, alen, <ref_pos>'.format())
@argument('-R', '--reverse', action='store_true')
def bam_aln_view(args):
    """
    """
    sam = Samfile(args.bam)
    skip_flag = 0x004
    sep = ' ' * 10
    sep = '\t'
    def decorate(aln, ref_aln=None, indicator=None):
        if ref_aln and args.mask_ref_base:
            #aln = ''.join(('.' if a == r and a != ('-' or ' ') else a) for a, r in zip(aln, ref_aln))
            aln = ''.join(('.' if a == r else a) for a, r in zip(aln, ref_aln))  # '-' is also shown as '.'
        if indicator:
            # if aln is blank, fill with indicator instead
            aln = ''.join(i if a == ' ' else a for a, i in zip(aln, indicator))
        if args.color_base:
            aln = color_term_dna(aln)
        return aln

    def get_sorted(read_alns):
        if args.order is None:
            return read_alns
        # if args.order.isdigit():  # TODO getting corresponding reference position is required
        #     pos = int(args.order)
        #     read_alns = sorted(read_alns, key=lambda x: x[1], reversed=args.reverse)
        order = args.order
        assert order in 'qname edit edit_ratio nins ndel alen'.split(' ')
        return sorted(read_alns, key=lambda x: getattr(x[0], order), reverse=args.reverse)

    logging.info('Target region: %s', args.region)
    with sam:
        for iv in sam_intervals(sam, regions=(args.region or None)):
            loc = LocalInfo(sam, iv, fasta=args.reference, skip_flags=skip_flag)
            print ('start', loc.start)
            print ('end', loc.end)
            print ('align length', loc.align_length)
            ref_aln = ''.join(loc.get_ref_align())
            ref_dec = decorate(ref_aln)
            pos_txt = get_aln_pos_text(ref_aln, offset=loc.start)
            indicator = pos_txt['indicator']
            print (pos_txt['number'])
            print (indicator)
            print (ref_dec, iv.contig, 'mapq', 'clip', 'edit', 'nins', 'ndel', 'alen', 'edit_ratio', sep=sep)
            indicator = indicator.replace('|', ':')  # for visibility
            print (indicator)
            it = loc.iter_read_aligns()
            it = get_sorted(it)
            for read, aln in it:
                read_aln = decorate(''.join(aln), ref_aln, indicator=indicator)
                clip_status = ('1' if read.has_lclip else '0') + ('1' if read.has_rclip else '0')
                print (read_aln, read.rec.qname, read.mapq, clip_status, read.edit, read.nins, read.ndel, read.alen,
                        '{0:.2f}'.format(read.edit_ratio), sep=sep)



class SamConcat(object):
    # TODO concat other headers

    def __init__(self, bams):
        self._bams = bams
        self._refs = []
        self._lengths = []
        self._refset = set()

        for fn in self._bams:
            with Samfile(fn) as sam:
                for ref, length in zip(sam.references, sam.lengths):
                    if ref not in self._refset:
                        self._refs.append(ref)
                        self._lengths.append(length)
                        self._refset.add(ref)

        logging.info('Ref lengths: %s', len(self._refs))

    def write(self, output):
        if output.endswith('.bam'):
            mode = 'wb'
        else:
            mode = 'wh'
        out = pysam.Samfile(output, mode=mode, reference_names=self._refs, reference_lengths=self._lengths)

        for fn in self._bams:
            with Samfile(fn) as sam:
                tid_map = {sam.gettid(ref): out.gettid(ref) for ref in sam.references}  # {org_tid: out_tid}
                for rec in sam:
                    rec.reference_id = tid_map.get(rec.reference_id, -1)
                    rec.next_reference_id = tid_map.get(rec.reference_id, -1)
                    out.write(rec)



# TODO rescue other header contents (e.g. @RG)
# TODO fai file for set reference order
@command.add_sub
@argument('bams', nargs='+')
@argument('-o', '--output', default='/dev/stdout')
def bam_cat(args):
    """ Concatenate bamfiles in order with different references
    """
    concat = SamConcat(args.bams)
    concat.write(args.output)


@command.add_sub
@argument('bam')
@argument('-r', '--region', help='region of target bam file')
@argument('-s', '--source-bam')  # TODO pair of fastq
@argument('-o', '--output', default='/dev/stdout')
def bam_fill_seq(args):
    """ Fill empty sequence with known seqs
    """
    if not args.source_bam:
        source_bam = args.bam
    else:
        source_bam = args.source_bam
    logging.info('Loading samfile: %s', source_bam)
    src_seqs = {1: {}, 2: {}}

    src = pysam.Samfile(source_bam)
    with src:
        for rec in src:
            if rec.is_supplementary:  # skip supplementary alignment
                continue
            if rec.is_secondary:  # skip supplementary alignment
                continue
            if rec.seq is None:  # empty
                continue
            if rec.is_read1:
                src_seqs[1][rec.qname] = (rec.seq, rec.is_reverse)
            else:
                src_seqs[2][rec.qname] = (rec.seq, rec.is_reverse)

    logging.info('Loaded read1 : %s', len(src_seqs[1]))
    logging.info('Loaded read2 : %s', len(src_seqs[2]))

    sam = Samfile(args.bam)
    if args.output.endswith('.bam'):
        mode = 'wb'
    else:
        mode = 'wh'
    out = pysam.Samfile(args.output, mode=mode, template=sam)

    if args.region:
        it = sam.fetch(region=args.region)
    else:
        it = sam

    for rec in it:
        qname = rec.qname
        if rec.seq is None:  # only fill when empty
            ret = src_seqs[1 if rec.is_read1 else 2].get(rec.qname)
            if ret is not None:
                seq, is_rev = ret
                if is_rev != rec.is_reverse:
                    seq = dna_revcomp(seq)
                seq = Cigar(rec.cigar).hard_clip_seq(seq)
                rec.seq = seq  # refill

        out.write(rec)


@command.add_sub
@argument('bam')
@argument('-r', '--region', help='region of target bam file')
@argument('--max-nm', default=4, type=int)
@argument('--max-depth', default=8000, type=int)
@argument.exclusive(
    argument('--summary', action='store_true'),
    argument('--read-count', action='store_true'),
)
def bam_depth_with_nm(args):
    """
    * unmapped is discarded
    * both clipped is discarded
    * end clipped is included
    * multimap is included
    * stratified with NM

    default mode:
        pos is 1-based

    summary mode:
        covered
    """
    sam = Samfile(args.bam)
    if args.region:
        c, s, e = parse_region(args.region)
        it = sam.pileup(reference=r, start=s, end=e, max_depth=args.max_depth)
    else:
        it = sam.pileup(max_depth=args.max_depth)
    sam_info = SamInfo(sam)

    def cond(prec):
        rec = prec.alignment
        if rec.is_unmapped:
            return False
        read = sam_info.get_read_info(rec)
        if read.overhang > 0:
            return False
        return True

    max_key = 'NM_more'
    nm_keys = ['NM' + str(nm) for nm in range(args.max_nm+1)] + [max_key]
    def get_key(prec):
        rec = prec.alignment
        nm = rec.get_tag('NM')
        if nm < args.max_nm:
            return 'NM' + str(nm)
        else:
            return max_key

    header = ['contig', 'pos'] + nm_keys
    def iter_table(it):
        Record = namedtuple('Record', header)
        for pcol in it:
            ps = filter(cond, pcol.pileups)
            counts = Counter(map(get_key, ps))
            yield Record(pcol.reference_name, pcol.pos+1, *(counts[k] for k in nm_keys))

    summary_header = ['contig', 'length', 'covered'] + nm_keys
    def iter_summary(it):
        """ NMx is the number of covered position with at least a read whose edit distance to the refernece is under x.
        """
        Record = namedtuple('Record', summary_header)
        def get_min_nm(row):
            for k in nm_keys:
                if getattr(row, k) > 0:
                    return k

        it1 = iter_table(it)
        for contig, rows in groupby(it1, lambda row: row.contig):
            length = sam_info.get_length(contig)
            counts = Counter([get_min_nm(row) for row in rows])
            nm_counts = [counts[k] for k in nm_keys]
            covered = sum(nm_counts)
            yield Record(contig, length, covered, *nm_counts)

    read_count_header = ['contig', 'length', 'total'] + nm_keys
    def iter_read_counts(it):
        """ NMx is the number of reads whose edit distance to the refernece is under x.
        """
        Record = namedtuple('Record', read_count_header)

        it1 = iter_table(it)
        for contig, rows in groupby(it1, lambda row: row.contig):
            length = sam_info.get_length(contig)
            rows = list(rows)
            counts = {}
            for k in nm_keys:
                counts[k] = sum(getattr(row, k) for row in rows)

            nm_counts = [counts[k] for k in nm_keys]
            total = sum(nm_counts)
            yield Record(contig, length, total, *nm_counts)

    if args.summary:
        logging.info('Emit coverage summary')
        print (*summary_header, sep='\t')
        for row in iter_summary(it):
            print (*row, sep='\t')
    elif args.read_count:
        logging.info('Emit read counts')
        print (*read_count_header, sep='\t')
        for row in iter_read_counts(it):
            print (*row, sep='\t')
    else:
        print (*header, sep='\t')  # header
        for row in iter_table(it):
            print (*row, sep='\t')


_MappingBlock = namedtuple('MappingBlock', 'start end is_del local_start local_end')
class MappingConverter(object):
    '''
    Illustration with examples

    pos: 0-based coordinate

                         1         2         3         4         5         6         7
    pos        0123456789012345678901234567890123456789012345678901234567890123456789012345
                                                          1
    local_pos            0123 456                     7 8901         234
                                                           1
    last_end             01234456                     677890111111111123

    >>> aln = '----------AGGG-GTT---------------------C-CCTA---------TTA-------------------'

                         AGGG GTT  # (0, '7M') => (10, '4M1D3M')
                         AGGG GTT  # (0, '4H7M') => (10, '4H4M1D3M')
                     AAAAAGGG GTT  # (0, '4S7M') => (10, '4S4M1D3M')
                     AAAAAGG- GTT  # (0, '4S3M1D3M') => (10, '4S3M2D3M')
                         AGGG GTT  # (0, '3M4I4M') => (10, '3M4I1M1D3M')
                           +  # insertion at next
                         AGGG GTT  # (0, '4M4I3M') => (10, '4M4I1D3M')
                            +
                          GGG GTT  # (1, '3M4I1M2I2M') => (11, '3M4I1D1M2I2M')
                            + +
                          GGG GTT                     C -CTA         TC    # (1, 5M4I2M1D5M) => (11, '3M1D2M4I1M21D1M2D3M9D2M4H')
                               +
                          GGG GTT                     C -CTA         TC    # (1, 30H5M4I2M3I1D5M4H) => (11, '30H3M1D2M4I1M21D1M3I2D3M9D2M4H')
                               +                      +
                          GGG GTT                     C -CTA         TCATTTT    # (1, 30H5M4I2M3I1D6M4S) => (11, '30H3M1D2M4I1M21D1M3I2D3M9D3M4S')
                               +                      +

    >>> mc = MappingConverter(aln)

    >>> lposs = [0, 3, 4, 7, 11, 15]
    >>> [mc.get_pos(lpos) for lpos in lposs]
    [10, 13, 15, 39, 44, -1]

    >>> mc.get_ref_cigar(3, 6).to_str()
    '3D'
    >>> mc.get_ref_cigar(3, 17).to_str()
    '7D4M1D2M'

    >>> x, y = (mc.convert(0, Cigar.parse('7M'))); x, y.to_str()
    (10, '4M1D3M')
    >>> x, y = (mc.convert(0, Cigar.parse('4H7M'))); x, y.to_str()
    (10, '4H4M1D3M')
    >>> x, y = (mc.convert(0, Cigar.parse('4S7M'))); x, y.to_str()
    (10, '4S4M1D3M')
    >>> x, y = (mc.convert(0, Cigar.parse('4S3M1D3M'))); x, y.to_str()
    (10, '4S3M2D3M')
    >>> x, y = (mc.convert(0, Cigar.parse('3M4I4M'))); x, y.to_str()
    (10, '3M4I1M1D3M')
    >>> x, y = (mc.convert(0, Cigar.parse('4M4I3M'))); x, y.to_str()
    (10, '4M4I1D3M')
    >>> x, y = (mc.convert(1, Cigar.parse('3M4I1M2I2M'))); x, y.to_str()
    (11, '3M4I1D1M2I2M')
    >>> x, y = (mc.convert(1, Cigar.parse('5M4I2M1D5M4H'))); x, y.to_str()
    (11, '3M1D2M4I1M21D1M2D3M9D2M4H')
    >>> x, y = (mc.convert(1, Cigar.parse('30H5M4I2M3I1D5M4H'))); x, y.to_str()
    (11, '30H3M1D2M4I1M21D1M3I2D3M9D2M4H')
    >>> x, y = (mc.convert(1, Cigar.parse('30H5M4I2M3I1D6M4S'))); x, y.to_str()
    (11, '30H3M1D2M4I1M21D1M3I2D3M9D3M4S')

                         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15
               0....5....0....5....0....5.7..0....5...90....5....0....5.7..0...45....01...5....0....5....0....5....0....5....0....5....0....5....0....5....0....5....0
    >>> aln = 'TTTATTTATTTATTTATTTAT-----TTTTTTAAGATGGA-----------------GTCTCGCTTTGTTGC---------------CCAGGCTGGAGTGCAG--------------------------------------TGGCGTGATC'

               ....................-     -.............                 ...............               ................                                      ..    # 6H20M2D21M1I25M
                                                                               +1
                        20M         7D        13M           17D          8M    1I  7M       15D             16M                        38D                   2M

    >>> mc = MappingConverter(aln)
    >>> x, y = mc.convert(0, Cigar.parse('6H20M2D21M1I25M')); x, ' '.join(y.to_str_tuple())
    (0, '6H 20M 7D 13M 17D 8M 1I 7M 15D 16M 38D 2M')

    '''
    def __init__(self, ref_aln):
        """ alignment of reference sequence to objective coordinate
        """
        self._blocks = []
        s = 0
        local_s = 0
        for op, l in aln2cigar(ref_aln):
            local_l = l if op == Cigar.M else 0
            b = _MappingBlock(s, s + l, op == Cigar.D, local_start=local_s, local_end=local_s + local_l)
            self._blocks.append(b)
            s += l
            local_s += local_l

    def get_pos(self, lpos):  # TODO binary search?
        for b in self._blocks:
            if b.is_del:
                continue
            if b.local_end <= lpos:
                continue
            offset = (lpos - b.local_start)
            return b.start + offset
        return -1

    def get_ref_cigar(self, start, end):
        """
        start: aln coordinate
        end: aln coodrinate
        """
        cigar = Cigar()
        for b in self._blocks:
            if b.end < start:
                continue
            s = max(start, b.start)
            e = min(end, b.end)
            op = Cigar.D if b.is_del else Cigar.M
            cigar.add((op, e - s))
            if end < b.end:
                break
        return cigar

    def convert(self, lpos, cigar):
        poss = []
        out_cigar = Cigar()
        cur_lpos = lpos   # reference local position (not a position on sequence!)
        ib = iter(self._blocks)
        block = next(ib)
        while block.local_end <= cur_lpos:  # skip blocks
            block = next(ib, None)

        for op, l in cigar:
            if op != Cigar.I:  # emit past blocks if operation is not an I (which should be emited just after previous cigar operation)
                while block and block.local_end < cur_lpos:
                    if block.is_del:
                        out_cigar.add((Cigar.D, block.end - block.start))
                    else:
                        out_cigar.add((Cigar.M, block.end - block.start))
                    block = next(ib, None)
            if op in (Cigar.S, Cigar.H):
                out_cigar.add((op, l))
                continue
            if op in (Cigar.M, Cigar.D):
                if block:
                    poss.append((block.start + (cur_lpos - block.local_start)))  # offset at cur_lpos
                    cur_lend = cur_lpos + l
                while block and block.local_start < cur_lend:
                    if block.is_del:
                        out_cigar.add((Cigar.D, block.end - block.start))
                    else:
                        length = min(block.local_end, cur_lend) - max(block.local_start, cur_lpos)
                        if length:
                            #out_cigar.add((Cigar.M, length))
                            out_cigar.add((op, length))
                    if block.local_end <= cur_lend:  # when this block is end, read next
                        block = next(ib, None)
                    else:
                        break
                cur_lpos += l
                continue
            if op == Cigar.I:
                out_cigar.add((Cigar.I, l))
                continue
            raise NotImplementedError

        return (poss[0], out_cigar)

#TODO
# - take multiple fasta and names
# - set mate information for given msas
@command.add_sub
@argument('bam')
@argument('-f', '--msa-fasta', required=True)
@argument('-n', '--refname', default='consensus')
@argument('-o', '--output', default='/dev/stdout')
@argument('--skip-flag', type=lambda x: int(x, 16), default=0x000)
def bam_surject_msa(args):
    """
    Caveats:
    - flags are remained as original statuses
    - remaining original values for MD, NM, and AS tags
    - mate are given as unmapped
    - same records are emited
    """
    skip_flag = args.skip_flag
    sam = Samfile(args.bam)
    fasta = Fasta(open(args.msa_fasta))
    mapped_ref_set = set(sam.references)

    # setup output
    refname = args.refname
    ref_length = len(fasta.contigs[0])

    if args.output.endswith('.bam'):
        mode = 'wb'
    else:
        mode = 'wh'
    out = pysam.Samfile(args.output, mode=mode, reference_names=[refname], reference_lengths=[ref_length])

    # iteration
    query_refs = fasta.names
    out_tid = out.gettid(refname)
    for qref in query_refs:
        if qref not in mapped_ref_set:
            logging.warning('%s is not found in original BAM file', qref)
            continue
        q_aln = fasta.get(qref)
        mc = MappingConverter(q_aln.seq)
        for rec in sam.fetch(reference=qref):
            if rec.flag & skip_flag:
                continue
            #a = pysam.AlignedSegment()
            a = rec.__copy__()
            #print (rec)
            if not rec.is_unmapped:
                org_cigar = Cigar(rec.cigartuples)
                pos, cigar = mc.convert(rec.pos, org_cigar)
                if org_cigar.query_length != cigar.query_length:
                    logging.error('Invalid cigar conversion')
                    logging.error('org %s %s %s', rec.pos, org_cigar, org_cigar.query_length)
                    logging.error('new %s %s %s', pos, cigar, cigar.query_length)
                    s1 = pos
                    e1 = mc.get_pos(rec.pos + cigar.ref_length)
                    logging.error('ref %s-%s %s', s1, e1, mc.get_ref_cigar(s1, e1))
                    logging.error('read %s', rec.seq)
                    logging.error('qref %s', q_aln.seq[s1:e1])
                    raise Exception('Incompatible Cigar')
                a.cigar = cigar.values
                a.reference_start = pos
            a.reference_id = out_tid
            a.next_reference_id = -1     # this is required
            a.next_reference_start = -1  # this is required
            #a.flag = rec.flag
            #orec.seq = '*'
            #print (orec)
            out.write(a)


@command.add_sub
@argument('bam')
@argument('-o', '--output', default='/dev/stdout')
def bam_uniq(args):
    """
    * BAM file should be sorted
    * (qname, pos, is_unmapped, is_read_1, cigar) are checked
    * if multiple records exist, primary alignment is selected
    * scores are not changed
    """
    sam = Samfile(args.bam)

    # setup output
    if args.output.endswith('.bam'):
        mode = 'wb'
    else:
        mode = 'wh'
    out = pysam.Samfile(args.output, mode=mode, template=sam)
    it = sam  # TODO region

    def get_key(rec):
        return (rec.qname, rec.pos, rec.is_unmapped, rec.is_read1, rec.cigar)

    def get_best_rec(recs):
        for rec in recs:
            if not rec.is_secondary:
                return rec
        return rec  # No primary alignments were found

    for key, recs in groupby(it, get_key):
        rec = get_best_rec(recs)
        out.write(rec)

from __future__ import print_function
from argtools import command, argument
from pysam import Samfile
import numpy as np
import logging
from operator import attrgetter
from itertools import islice, groupby
from collections import defaultdict
from builtins import range, filter, map
from ..utils import unzip, Counter
from ..utils import format as fmt
from .. import sh
from .sam_loader import SamDepthAnalyzer, SamPosInfo, SamModelBuilder
from .model import InferModel
from tqdm import tqdm


import networkx as nx
class VariantGraph(object):
    def __init__(self, refname):
        self.refname = refname
        self._graph = nx.MultiGraph()
        self._aln_vars = defaultdict(list)   # {aln_rec: [variant]}

    @classmethod
    def from_depth_analyzer(cls, depth_analyzer):
        refs = depth_analyzer.iter_ref_records()
        for refname, it in refs:
            self = cls(refname)
            logging.info('Storing variants')
            it = tqdm(it)
            #it = islice(it, 20000)
            for pos_info in it:
                if pos_info.nubases > 1 and list(sorted(pos_info.unsegs, reverse=True))[1] > 1:   #  at least two second major alleles were needed
                    self.add_variant(pos_info)
            logging.info('Storing variants is done')
            yield self

    def add_variant(self, pos_info):
        self._graph.add_node(pos_info.pos, **{'pos_info': pos_info})
        for info in pos_info.get_read_info():
            pcol = info.pop('pcol')
            data = dict(info, pos_id=pos_info.pos)
            aln = pcol.alignment
            self._aln_vars[aln].append(data)

            # edge
            if len(self._aln_vars[aln]) > 1:
                p1, p2 = self._aln_vars[aln][-2:]
                p1_id = p1['pos_id']
                p2_id = p2['pos_id']
                data = {
                    'qname': aln.qname,
                    'bases': [p1['bases'], p2['bases']],
                    'quals': [p1['quals'], p2['quals']],
                }
                self._graph.add_edge(p1_id, p2_id, **data)

    def get_graph(self):
        return self._graph

    def get_subgraphs(self):
        return list(nx.connected_component_subgraphs(self._graph))


@command.add_sub
@argument('bam')
def mc_pos_info(args):
    cols = 'contig pos nsegs nubases ubases unsegs uquals_mean'.split(' ')
    cols = 'contig pos nsegs nubases ubases unsegs wsegs uwsegs uquals_mean'.split(' ')

    getvals = {col: attrgetter(col) for col in cols}
    getvals['nsegs'] = lambda rec: rec.nsegs
    getvals['ubases'] = lambda rec: ','.join(rec.ubases)
    getvals['unsegs'] = lambda rec: ','.join(map(str, rec.unsegs))
    getvals['uwsegs'] = lambda rec: ','.join(map('{:.02f}'.format, rec.uwsegs))
    getvals['uquals_mean'] = lambda rec: ','.join(map('{:.02f}'.format, rec.uquals_mean))
    getvals['contig'] = lambda rec: tid_refnames[rec.tid]

    print (*cols, sep='\t')  # header
    with Samfile(args.bam) as sam:
        tid_refnames = {sam.get_tid(name): name for name in sam.references}
        da = SamDepthAnalyzer(sam)
        for rec in da.iter_records():
            vals = [getvals[col](rec) for col in cols]
            print (*vals, sep='\t')


import gzip
from dill import dill
import cPickle as pickle
@command.add_sub
@argument('bam')
@argument('-o', '--outdir', default='mc_vg_output')
def mc_variant_graph(args):
    sh.call(['mkdir', '-p', args.outdir])
    with Samfile(args.bam) as sam:
        da = SamDepthAnalyzer(sam)
        for vg in VariantGraph.from_depth_analyzer(da):
            outname = fmt('{args.outdir}/{vg.refname}.vg')
            logging.info('Saving graph to %s', outname)
            with open(outname, 'w+') as fo:
                dill.dump(vg, fo)
            subs = vg.get_subgraphs()
            graph = vg.get_graph()
            nnodes = len(graph.nodes())
            logging.info('Number of nodes for %s : %s', vg.refname, nnodes)
            logging.info('Number of subgraphs for %s : %s', vg.refname, len(subs))


def show_model(model):
    for ref in model.refs:
        logging.info('Reference: %s', ref.name)
        logging.info('Number of variants: %s', len(ref.variants))
        logging.info('Number of candidates: %s', len(ref.candidates))
        logging.info('Number of paired candidates: %s', len([c for c in ref.candidates if c.is_paired]))

    ref_counts = Counter()
    for frag in tqdm(model.fragments):
        key = frozenset([c.ref.name for c in frag.candidates])
        ref_counts[key] += 1

    # for frag in tqdm(model.fragments):
    #     key = [(c.ref.name, tuple(sorted(c.bases.items()))) for c in frag.candidates]
    #     diff = len(key) - len(set(key))
    #     if len(set(key)) > 1:
    #         logging.info('Number of redundant candidates is %s of %s (%s)', diff, len(key), set(key))

    for key in sorted(ref_counts, key=lambda key: (len(key), tuple(sorted(key)))):
        key1 = tuple(sorted(key))
        count = ref_counts[key]
        logging.info('Number of fragments for %s is %s', ','.join(key1), count)


def show_initial_genotype_info(infer_model):
    v_poss = {}  # {(rname, vpos): phase_start_pos}
    for ref in infer_model.refs:
        rname = ref.name
        blocks = infer_model.get_het_blocks(ref.name)
        for bl in blocks:
            for v in bl['variants']:
                v_poss[rname, v.pos] = bl['pos']

    for v in infer_model.variants:
        rname = v.ref.name
        pos = v.pos
        #depths = infer_model.get_full_depths(v)
        tot_depth = infer_model.get_total_depth(v)
        sinfo = infer_model.get_site_info(v)
        gen_scores = infer_model.get_init_gen_scores(v) # [((b1, b2, ..), prob, score)]

        v_pos = v_poss.get((rname, v.pos))

        print (rname, pos,
               v_pos,
               sinfo['ncands'],
               sinfo['site_score'],
               sinfo['base_counts'],
               sinfo['mean_depths'],
               gen_scores,
               sep='\t')


def show_variant_info(infer_model):
    for v in infer_model.variants:
        ref = v.ref.name
        pos = v.pos
        sinfo = infer_model.get_site_info(v)
        gen_probs = infer_model.get_variant_probs(v)   # [((b1, b2, ..), prob)]

        gens = []
        hap_probs = []
        for gp in gen_probs:
            probs = gp['prob']
            b = ','.join(gp['bases'])
            gens.append(b)
            #hap_probs.append(','.join(map('{0:.3f}'.format, probs)))
            hap_probs.append(','.join(map('{0:.3f}'.format, probs)))

        #print (gens, probs)
        print (ref, pos, sinfo,
               '|'.join(gens),
               '|'.join(hap_probs),
                sep='\t')

@command.add_sub
@argument('bam')
@argument('-o', '--outname', default='mc_vg_output.vg')
@argument('-r', '--regions', nargs='*')
@argument('--hap-depth', type=float, default=20.)
def mc_vg_create(args):
    import sys
    sys.setrecursionlimit(10000)
    with Samfile(args.bam) as sam:
        smb = SamModelBuilder(sam, regions=args.regions)
        show_model(smb.model)
    im = InferModel(smb.model, args.hap_depth)
    show_initial_genotype_info(im)
    #im.fix_
    show_variant_info(im)   # show variant, alts, depth, probs.

        # with gzip.open(args.outname, 'wb+') as fo:
        #     pickle.dump(smb.model, fo)


@command.add_sub
@argument('graph')
def mc_vg_phasing(args):
    import sys
    sys.setrecursionlimit(10000)
    with gzip.open(args.graph, 'rb') as fi:
        model = pickle.load(fi)
        print (len(model.fragments))
        print (len(model.refs))

#TODO dill.load is segfault
import glob
@command.add_sub
@argument('input_dir')
def mc_vg_read(args):
    fnames = sorted(glob.glob(fmt('{args.input_dir}/*.vg')))
    for fname in fnames:
        logging.info('Loading %s', fname)
        #sh.call('sleep 1')
        with open(fname) as fi:
            vg = dill.load(fi)
            subs = vg.get_subgraphs()
            graph = vg.get_graph()
            nnodes = len(graph.nodes())
            logging.info('Number of nodes for %s : %s', vg.refname, nnodes)
            logging.info('Number of subgraphs for %s : %s', vg.refname, len(subs))


@command.add_sub
@argument('pos_info')
@argument('graph')
def mc_infer(args):
    """
    Emit VCF ?
    """
    pos_infos = PosInfo.parse(args.pos_info)
    vg = VariantGraph.parse(args.graph)
    infer = Inferer(vg, pos_infos)
    while not infer.is_converged:
        infer.update()
        infer.save_info()
    infer.emit_vcf()

import os
import json

from Bio.Seq import Seq
from django.test import TestCase

from edge.pcr import pcr_from_genome
from edge.models import Genome, Fragment, Genome_Fragment
from edge.blastdb import build_all_genome_dbs, fragment_fasta_fn


class GenomePcrTest(TestCase):

    def build_genome(self, circular, *templates):
        g = Genome(name='Foo')
        g.save()
        for seq in templates:
            f = Fragment.create_with_sequence('Bar', seq, circular=circular)
            Genome_Fragment(genome=g, fragment=f, inherited=False).save()
            try:
                os.unlink(fragment_fasta_fn(f))
            except:
                pass
        build_all_genome_dbs(refresh=True)
        return Genome.objects.get(pk=g.id)

    def test_pcr_produces_expected_product(self):
        upstream = "gagattgtccgcgtttt"
        p1_bs = "catagcgcacaggacgcggag"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g = self.build_genome(False, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(len(r[1]), 1)  # one binding site for each primer
        self.assertEquals(len(r[2]), 1)  # one binding site for each primer
        self.assertEquals(r[3]['fragment_name'], g.fragments.all()[0].name)
        self.assertEquals(r[3]['fragment_id'], g.fragments.all()[0].id)
        self.assertEquals(
            r[3]['region'],
            (len(upstream) + 1, len(upstream + p1_bs + middle + p2_bs)))

    def test_finds_pcr_product_across_circular_boundary(self):
        upstream = "gagattgtccgcgtttt"
        p1_bs = "catagcgcacaggacgcggag"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        template = ''.join([middle[10:], p2_bs, downstream, upstream, p1_bs, middle[0:10]])
        g = self.build_genome(True, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(r[3]['fragment_name'], g.fragments.all()[0].name)
        self.assertEquals(r[3]['fragment_id'], g.fragments.all()[0].id)
        self.assertEquals(r[3]['region'],
                          (len(template) - 10 - len(p1_bs) + 1, len(middle) - 10 + len(p2_bs)))

    def test_finds_pcr_product_when_fwd_primer_is_across_circular_boundary(self):
        upstream = "gagattgtccgcgtttt"
        p1_bs = "catagcgcacaggacgcggag"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        template = ''.join([p1_bs[5:], middle, p2_bs, downstream, upstream, p1_bs[0:5]])
        g = self.build_genome(True, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(r[3]['fragment_name'], g.fragments.all()[0].name)
        self.assertEquals(r[3]['fragment_id'], g.fragments.all()[0].id)
        self.assertEquals(
            r[3]['region'],
            (len(template) - 5 + 1, len(p1_bs) - 5 + len(middle + p2_bs)))

    def test_finds_pcr_product_when_rev_primer_is_across_circular_boundary(self):
        upstream = "gagattgtccgcgtttt"
        p1_bs = "catagcgcacaggacgcggag"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        template = ''.join([p2_bs[5:], downstream, upstream, p1_bs, middle, p2_bs[0:5]])
        g = self.build_genome(True, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(r[3]['fragment_name'], g.fragments.all()[0].name)
        self.assertEquals(r[3]['fragment_id'], g.fragments.all()[0].id)
        self.assertEquals(
            r[3]['region'],
            (len(p2_bs) - 5 + len(downstream + upstream) + 1, len(p2_bs) - 5))

    def test_pcr_produces_product_with_multiple_binding_sites_but_one_overlapping_region(self):
        p1_bs = "catagcgcacaggacgcggag"
        upstream = "gagattgtccgcgtttt" + str(Seq(p1_bs).reverse_complement())
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g = self.build_genome(False, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(len(r[1]), 2)  # two binding sites for each primer
        self.assertEquals(len(r[2]), 1)  # one binding site for this primer
        self.assertEquals(r[3]['fragment_name'], g.fragments.all()[0].name)
        self.assertEquals(r[3]['fragment_id'], g.fragments.all()[0].id)
        self.assertEquals(
            r[3]['region'],
            (len(upstream) + 1, len(upstream + p1_bs + middle + p2_bs)))

    def test_pcr_does_not_produce_product_with_multiple_overlapping_regions(self):
        p1_bs = "catagcgcacaggacgcggag"
        upstream = "gagattgtccgcgtttt" + str(Seq(p1_bs).reverse_complement())
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggc" + p2_bs + "gcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g = self.build_genome(False, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], None)
        self.assertEquals(len(r[1]), 2)  # two binding sites for each primer
        self.assertEquals(len(r[2]), 2)  # two binding sites for each primer

    def test_pcr_does_not_produce_product_when_primer_binding_site_is_too_small(self):
        p1_bs = "catagcgcacaggacgcggag"
        upstream = "gagattgtccgcgtttt"
        middle = "cggcacctgtgagccg"
        p2_bs = "gctagcatca"
        downstream = "gttaaggcgcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g = self.build_genome(False, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], None)
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(len(r[2]), 0)

    def test_pcr_does_not_produce_product_when_primer_binding_site_has_too_many_mutations(self):
        def mutate(s, n):
            c = s[n]
            if c == 'a':
                c = 'g'
            if c == 'g':
                c = 't'
            if c == 't':
                c = 'c'
            if c == 'c':
                c = 'a'
            return s[0:n] + c + s[n + 1:]

        p1_bs = "catagcgcacaggacgcggag"
        upstream = "gagattgtccgcgtttt"
        middle = "cggcacctgtgagccg"
        p2_bs = "gctagcatcagtacgta"
        downstream = "gttaaggcgcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + mutate(mutate(mutate(p1_bs, 5), 9), 11)
        p1_good = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g = self.build_genome(False, template)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], None)
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(len(r[2]), 1)

        g = self.build_genome(False, template)
        r = pcr_from_genome(g, p1_good, p2)
        self.assertEquals(r[0], ''.join([p1_good, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(len(r[2]), 1)

    def test_pcr_does_not_produce_product_when_primer_binds_to_different_fragments(self):
        p1_bs = "catagcgcacaggacgcggag"
        upstream = "gagattgtccgcgtttt"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        template1 = ''.join([upstream, p1_bs, middle])
        template2 = ''.join([middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g = self.build_genome(False, template1, template2)
        r = pcr_from_genome(g, p1, p2)
        self.assertEquals(r[0], None)
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(len(r[2]), 1)

    def test_pcr_does_produce_product_when_duplicate_regions_on_different_genome(self):
        p1_bs = "catagcgcacaggacgcggag"
        upstream = "gagattgtccgcgtttt"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())

        g1 = self.build_genome(False, template, template)
        g2 = self.build_genome(False, template)

        r = pcr_from_genome(g1, p1, p2)
        self.assertEquals(r[0], None)
        self.assertEquals(len(r[1]), 2)  # two binding sites for each primer
        self.assertEquals(len(r[2]), 2)  # two binding sites for each primer

        r = pcr_from_genome(g2, p1, p2)
        self.assertEquals(r[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(len(r[2]), 1)

    def test_pcr_api(self):
        upstream = "gagattgtccgcgtttt"
        p1_bs = "catagcgcacaggacgcggag"
        middle = "cggcacctgtgagccg"
        p2_bs = "taatgaccccgaagcagg"
        downstream = "gttaaggcgcgaacat"
        template = ''.join([upstream, p1_bs, middle, p2_bs, downstream])
        p1 = 'aaaaaaaaaa' + p1_bs
        p2 = 'tttttttttt' + str(Seq(p2_bs).reverse_complement())
        g = self.build_genome(False, template)

        res = self.client.post('/edge/genomes/%s/pcr/' % g.id,
                               data=json.dumps(dict(primers=[p1, p2])),
                               content_type='application/json')
        self.assertEquals(res.status_code, 200)
        d = json.loads(res.content)

        self.assertEquals(len(d), 4)
        self.assertEquals(d[0], ''.join([p1, middle, str(Seq(p2).reverse_complement())]))
        self.assertEquals(len(d[1]), 1)
        self.assertEquals(d[1][0]['subject_start'], len(upstream) + 1)
        self.assertEquals(d[1][0]['subject_end'], len(upstream) + len(p1_bs))
        self.assertEquals(d[1][0]['query_start'], len(p1) - len(p1_bs) + 1)
        self.assertEquals(d[1][0]['query_end'], len(p1))
        self.assertEquals(len(d[2]), 1)
        self.assertEquals(d[2][0]['subject_start'], len(template) - len(downstream))
        self.assertEquals(d[2][0]['subject_end'], len(template) - len(downstream) - len(p2_bs) + 1)
        self.assertEquals(d[2][0]['query_start'], len(p2) - len(p2_bs) + 1)
        self.assertEquals(d[2][0]['query_end'], len(p2))

# -*- coding: utf-8 -*-
# The starting number of sequence index by NCBI alignment is 1

from __future__ import print_function
import os
import yaml
import regex
import pickle
import numpy as np
import pandas as pd
from Bio import Entrez
from Bio.Seq import Seq
from pyfaidx import Fasta
from itertools import islice

all_function = {'a':'annot_update(manifest_data)','m':'File_annot_mod(manifest_data)','b':'bowtie_build(manifest_data)',\
't':'Target_statistics(manifest_data,target)','d':'targetbases_genomewide_distribute(manifest_data,slide_size,target)'}

def annot_update(manifest_data):
    """
    Use chromosome accession to crawl chromosome annotation and genome sequence by Entrez module from Bio package.
    """
    if not os.path.exists('1.Material_prep'):
        os.mkdir('1.Material_prep')
    Entrez.email = "biojxz@163.com"  # using my email if you doesnt mind
    print("Downloading genome and chromosome annotation file ...")
    for chro in manifest_data['chr_accession']:
        f = open('1.Material_prep/%s_annot.txt'%chro,'w')
        # get genome.fa
        handle = Entrez.efetch(db="nucleotide",id=manifest_data['chr_accession'][chro],rettype="ft",retmode="text")
        f.write(handle.read())
        f.close()

class File_annot_mod():
    def __init__(self,manifest_data):
        """
        Format modification of annotation file.
        """
        self.manifest_data = manifest_data
        self.call_modify(manifest_data)

    def call_modify(self,manifest_data):
        for chro in manifest_data['chr_accession']:
            self.modify('%s_annot.txt'%chro)
        os.system("""cat 1.Material_prep/chr*_annot_gene.xls | awk -F"\t" '{if(NR==1 || $1!~/gene_id/) print}'\
        > 1.Material_prep/annot_gene.xls""")

    def modify(self,annot_file):
        f1 = open('1.Material_prep/' + annot_file)
        f2 = open('1.Material_prep/%s_gene.xls'%annot_file.split(".")[0],'w')
        f3 = open('1.Material_prep/%s_geneplus.xls'%annot_file.split(".")[0],'w')
        f4 = open('1.Material_prep/%s_intron.xls'%annot_file.split(".")[0],'w')
        gene_site,strand,mRNA,gene_id,gene_annot = {},{},{},{},{}
        n = 0
        for line in islice(f1,1,None):
            line = line.rstrip()
            line_list = line.split('\t')
            try: 
                if line_list[2] == 'gene':
                    n += 1
                    gene_site[n] = int(line_list[0].strip('<|>')),int(line_list[1].strip('<|>'))
                    strand[n] = '+' if gene_site[n][0] < gene_site[n][1] else '-'
                elif line_list[2] == 'mRNA':
                    mRNA[n] = [int(line_list[0].strip('<|>')),int(line_list[1].strip('<|>'))]
                    mRNA_mutil = True
                elif line_list[2] == 'CDS':
                    mRNA_mutil = False
                elif line_list[2] == '':
                    if line_list[3] == 'locus_tag':
                        gene_id[n] = line_list[4]
                    elif line_list[3] == 'product':
                        gene_annot[n] = line_list[4]
            except:
                if mRNA_mutil:
                    mRNA[n] = mRNA[n] + [int(line_list[0].strip('<|>')),int(line_list[1].strip('<|>'))]
                else:
                    pass
        print('gene_id','strand','gene_start','gene_end','gene_length','gene_annotation',sep='\t',file=f2)
        print('gene_id','strand','upstream_start','upstream_end','gene_start','gene_end',\
        'downstream start','downstream end','gene_length','gene_annotation',sep='\t',file=f3)
        print('gene_id','strand','gene_start','gene_end','intron start','intron end',sep='\t',file=f4)
        for i in range(1,n+1):
            gene_length = abs(gene_site[i][0]-gene_site[i][1]) + 1
            upstream_start = gene_site[i][0]-1000 if strand[i]=='+' else gene_site[i][0]+1000
            upstream_end = gene_site[i][0]-1 if strand[i]=='+' else gene_site[i][0]+1
            downstream_start = gene_site[i][1]+1 if strand[i]=='+' else gene_site[i][1]-1
            downstream_end = gene_site[i][1]+1000 if strand[i]=='+' else gene_site[i][1]-1000
            # if you want to make sure upstream_start or downstream_end is greater than 0,you can do this:
            # if upstream_start < 1: upstream_start = 1
            # downstream_end < 1: upstream_start = 1
            print(gene_id[i],strand[i],gene_site[i][0],gene_site[i][1],gene_length,gene_annot[i],sep='\t',file=f2)
            print(gene_id[i],strand[i],upstream_start,upstream_end,gene_site[i][0],gene_site[i][1],\
            downstream_start,downstream_end,gene_length,gene_annot[i],sep='\t',file=f3)
            if len(mRNA[i]) > 2:
                mRNAtointron = map(lambda x:x+1 if mRNA[i].index(x)%2 else x-1,mRNA[i]) \
                if strand[i]=='+' else map(lambda x:x-1 if mRNA[i].index(x)%2 else x+1,mRNA[i])
                intron_list = mRNAtointron[1:-1]
                intron_list = map(lambda x:str(x),intron_list)
                print(gene_id[i],strand[i],gene_site[i][0],gene_site[i][1],'\t'.join(intron_list),sep='\t',file=f4)
        f1.close();f2.close();f3.close()


def bowtie_build(manifest_data):
    bowtie_build = manifest_data['bowtie_build']
    genome_path = manifest_data['genome_path']
    os.system("%s -f %s 1.Material_prep/genome"%(bowtie_build,genome_path))


class Target_statistics():
    def __init__(self,manifest_data,target):
        self.manifest_data = manifest_data
        self.target = target
        self.genome_seq = Fasta(manifest_data["genome_path"])
        # Running functions:
        self.genome_target_statistics()
        self.gene_target_statistics()
        self.gene_target_score()

    def genome_target_statistics(self):
        """
        This function will produce bed, txt and pdf file
        """

        f1 = open('1.Material_prep/%s_sites.bed'%self.target,'w')
        f2 = open('1.Material_prep/%s_targetextseq.txt'%self.target,'w')
        f3 = open('1.Material_prep/%s_targetsite_extseq.txt'%self.target,'w')
        print('chro\ttarget_site\ttarget_extseq',file=f3)
        for chro,accession in self.manifest_data["chr_accession"].items(): #accession is NC accession of chromosome
            seq = str(self.genome_seq[accession][:]).upper()
            site_tmp = 0
            chrsize = len(self.genome_seq[accession])
            # Use regex instead of re module because of overlapped is necessary to be considered
            for index,items in enumerate(regex.finditer(self.target,seq,overlapped=True)):
                site = items.span()[0] + 1 # items.span()[0] of regex.finditer is starting from 0
                print(chro,site,site+len(self.target)-1,site-site_tmp-1,items.group(),'+',sep='\t',file=f1)
                site_tmp = site + 1
                # Prepare for Weblogo:
                site_center = site + len(self.target)/2 - 1
                if site_center>9 and site_center < chrsize - 9:
                    targetextseq = self.genome_seq[accession][site_center-9:site_center+9]
                    targetextseq = str(targetextseq)
                    print('>%s_%d\n%s'%(chro,index+1,targetextseq),file=f2)
                    targetextseq_rc = str(Seq(targetextseq).reverse_complement())
                    print('>%s_rc%d\n%s'%(chro,index+1,targetextseq_rc),file=f2)
                    print(chro,site_center,targetextseq,sep='\t',file=f3)
        f1.close()
        f2.close()
        f3.close()
        # os.system("weblogo -c classic --format pdf < 1.Material_prep/%s_targetextseq.txt > 1.Material_prep/%s_weblogos.pdf"%(target,target))

    def gene_target_statistics(self):
        f = open('1.Material_prep/gene_%s_site.xls'%self.target,'w')
        print('chro\tgene_id\ttarget_site',file=f)
        
        def chro_target_statistics(chro,accession):
            f1 = open('1.Material_prep/%s_annot_gene.xls'%chro)
            f2 = open('1.Material_prep/%s_annot_gene2.xls'%chro,'w')
            for index,line in enumerate(f1):
                line = line.rstrip().split('\t')
                if index:
                    gene_minsite = int(line[2]) if line[1] == '+' else int(line[3])
                    gene_maxsite = int(line[3]) if line[1] == '+' else int(line[2])
                    seq = str(self.genome_seq[accession][gene_minsite:gene_maxsite]).upper()
                    for index,items in enumerate(regex.finditer(self.target,seq,overlapped=True)):
                        target_site = items.span()[0] + gene_minsite + 1
                        print(chro,line[0],target_site,sep='\t',file=f)

                    gene_length = int(line[4])
                    # Count target nucleotides from the 5′-most 90% of eah gene
                    gene_nearts = gene_minsite + int(0.9*gene_length)
                    gene_target_counts = (str(self.genome_seq[accession][gene_minsite:gene_nearts+1]).upper()).count(self.target)
                    print(line[0],line[1],line[2],line[3],line[4],gene_target_counts,line[5],sep='\t',file=f2)
                else:
                    print(line[0],line[1],line[2],line[3],line[4],self.target+'counts',line[5],sep='\t',file=f2)
            f1.close();f2.close()
        for chro,accession in self.manifest_data['chr_accession'].items():
            chro_target_statistics(chro,accession)
        os.system("""cat 1.Material_prep/chr*_annot_gene2.xls | awk -F"\t" '{if(NR==1 || $1!~/gene_id/) print}'\
        > 1.Material_prep/annot_gene2.xls""")
        f.close()

    def gene_target_score(self):
        """self.manifest_data example:
        Target_score:
            3:
                A: 0.46
                T: 0.35
                G: 0.11
                C: 0.08
        """
        df1 = pd.read_table('1.Material_prep/%s_targetsite_extseq.txt'%self.target)
        df2 = pd.read_table('1.Material_prep/gene_%s_site.xls'%self.target)
        targetcounts = df2.groupby('gene_id').size()
        df_merge = pd.merge(df1,df2,on=['chro','target_site'],how='right')
        Dict_score = self.manifest_data['Target_score']
        def gene_score_sum(extseq):
            score_sum = 0.00
            for site, nucleotide in Dict_score.items():
                target_nucl = extseq[site-1]
                try:
                    nucleotide_score = nucleotide[target_nucl]
                except:
                    # Default score of 'N' nucleotide is 0.25
                    nucleotide_score = 0.25
                score_sum += nucleotide_score
            correction_factor = 4.0 / len(Dict_score)
            score_sum_corr = score_sum * correction_factor
            return score_sum_corr 

        df_merge['target_score'] = df_merge['target_extseq'].apply(gene_score_sum)

        # sum gene target_score
        gd = df_merge.iloc[:,[3,4]].groupby('gene_id').sum()
        df_targetcounts = pd.DataFrame({'target_counts':targetcounts})
        # add gene target counts data
        df_merge2 = pd.merge(gd,df_targetcounts,left_index=True,right_index=True)
        df_merge2['target_score_ave'] = df_merge2['target_score'] / df_merge2['target_counts']
        df_merge2.to_csv('1.Material_prep/%s_gene_score.xls'%self.target,sep='\t')


def targetbases_genomewide_distribute(manifest_data,slide_size,target):
    df = pd.read_table('1.Material_prep/%s_sites.bed'%target,usecols=[0,1],names=['chro','site'])
    def chro_proc(chro,chrsize):
        df_chro = df[df['chro']==chro]
        df_chro['count'] = 1
        df_coordinate = pd.DataFrame(np.arange(1,chrsize+1))
        df_map = pd.merge(df_coordinate,df_chro,left_on=0,right_on='site',how='left')
        df_map = df_map.fillna(0)
        df_map['slide_num'] = (df_map[0]-1)//slide_size + 1
        df_map_comb = df_map.iloc[:,[3,4]].groupby(['slide_num']).sum()
        df_map_comb.to_csv('1.Material_prep/%s_%s_sliding-window_%d.txt'%(target,chro,slide_size),sep='\t')
    for chro,chrsize in manifest_data['chr_size'].items():
        chro_proc(chro,chrsize)


class gene_target_score():
    def __init__(self,manifest_data):
        pass

    def chro_ts(self,chro,accession):
        f1 = open('1.Material_prep/%s_annot_gene.xls'%chro)
        Dict_score = manifest_data[target_score]


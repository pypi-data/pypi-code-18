"""
visualization is a module visualizing tnseq data. 
main function:
a) Insertion_distribution function is used to analyze the distribution of transposon insertion overlaid across Chromosomes.
b) Gene_igs_analysis function is for analysis of the insertion density of gene and IGS.
c) weblogo function will call weblogo program to test the target bias of transposon.
d) readcounts_analysis function is applied to analyze the number of same reads from the high-through sequencing.
"""

from __future__ import print_function
import matplotlib.pyplot as plt
from itertools import islice
from pyfaidx import Fasta
import pandas as pd
import numpy as np
from Bio.Seq import Seq
import os

all_function = {'i':'Insertion_distribution(tag, slide_size, target, manifest_data)', 'g':'Gene_igs_analysis(tag)',
                'w':'weblogo(tag, target, units, manifest_data)', 'r':'readcounts_analysis(tag)'}


class Insertion_distribution():
    def __init__(self, tag, slide_size, target, manifest_data):
        self.tag = tag
        self.slide_size = slide_size
        self.target = target
        self.manifest_data = manifest_data
        self.genome_seq = Fasta(manifest_data["genome_path"])
        self.plot_plt()

    def plot_plt(self):
        datalist = self.data_processing()
        fig, ax_list = plt.subplots(nrows=len(datalist))
        ax_list[0].set_title('insert counts distribution')
        font = {'family': 'serif', 
            'color':  'darkred', 
            'weight': 'normal', 
            'size': 16, 
            }
        for index, data in enumerate(datalist): #datalist.reverse() [::-1]
            chro = data.split("_")[-3] #extract chromosome
            df = pd.read_table(data)
            df_genome = pd.read_table('1.Material_prep/%s_%s_sliding-window_%d.txt'%(self.target, chro, self.slide_size))
            ax_list[index].set_xlim(xmax=len(df['chromosome']))
            ax_list[index].set_xticks(map(lambda x:x*1000 / self.slide_size, [0, 1000, 2000, 3000])) #len(df['chromosome'])
            #ax_list[index].set_aspect(4)
            ax_list[index].set_ylim((0, 120))
            #ax_list[index].set_adjustable("datalim")
            ax_list[index].vlines(df_genome['slide_num'], [0], df_genome['count'], colors='#C6E2FF')
            ax_list[index].vlines(df['slide_num'], [0], df['chromosome'], colors='#66CDAA')
            # set ticks
            ax_list[index].set_yticks([20, 60, 100])
            # Hide the top and the right spines
            ax_list[index].spines['top'].set_visible(False)
            ax_list[index].spines['right'].set_visible(False)
            # Only show ticks on the bottom spines
            ax_list[index].xaxis.set_ticks_position('bottom')
            ax_list[index].yaxis.set_ticks_position('left')
            ax_list[index].set_ylabel(chro,  fontdict=font)
        plt.savefig('%s/%s_insertcounts_distribution_%d.pdf'%(self.tag, self.tag, self.slide_size))

    def data_processing(self):
        list = []
        df = pd.read_table('%s/%s_all_insertions.xls'%(self.tag, self.tag), usecols=[0, 1, 2])

        def chro_proc(chro,accession):
            df_chro = df[df['chromosome']==chro]
            df_chro = df_chro.groupby(['insertions', 'insert_direct'], as_index=False).count()
            df_chro['F'] = np.where(df_chro['insert_direct']=='+', df_chro['chromosome'], 0)
            df_chro['R'] = np.where(df_chro['insert_direct']=='-', -1 * df_chro['chromosome'], 0)
            chrsize = len(self.genome_seq[accession])
            arr_coordinate = np.arange(1, chrsize + 1)
            df_coordinate = pd.DataFrame({'chro_coordinate':arr_coordinate})
            df_map = pd.merge(df_coordinate, df_chro, left_on='chro_coordinate', right_on='insertions', how='left')
            df_map = df_map.fillna(0)
            #df_map_mod = df_map[df_map['insertions']!=0]
            df_map['slide_num'] = (df_map['chro_coordinate']-1) // self.slide_size + 1
            df_map_comb = df_map.iloc[:, [3, 4, 5, 6]].groupby(['slide_num']).sum()
            #df_map.to_csv('%s/%s_%s_plus.txt'%(tag, tag, chro), sep='\t', index=False, columns=['F'], header=False)
            #df_map.to_csv('%s/%s_%s_minus.txt'%(tag, tag, chro), sep='\t', index=False, columns=['R'], header=False)
            #df_map_mod.to_csv('%s/%s_%s_artemis.txt'%(tag, tag, chro), sep='\t', index=False, columns=['insertions', 'F', 'R'])
            df_map_comb.to_csv('%s/%s_%s_sliding-window_%d.txt'%(self.tag, self.tag, chro, self.slide_size), sep='\t')
            return '%s/%s_%s_sliding-window_%d.txt'%(self.tag, self.tag, chro, self.slide_size)
        for chro,accession in self.manifest_data['chr_accession'].items():
            filename = chro_proc(chro,accession)
            list.append(filename)
        return list

class Gene_igs_analysis():
    def __init__(self, tag):
        """Insertion site distribution at yeast transcription start sites (TSS),  intergenic regions
        and transcription termination sites (TTS)"""
        self.drawISDwithR(tag)

    def drawISDwithR(self, tag):

        #call R
        def call_R1(tag):  # colour = Chromosome
            f=open('%s/%s_idd.R'%(tag, tag), 'w')
            Rscript="""library("ggplot2")
            fgene <- read.table("%s/%s_all_gene.xls", sep='\t', header=T)
            fIGS <- read.table("%s/%s_all_IGS.xls", sep='\t', header=T)
            fgene$rate <- (abs(fgene$insert_site - fgene$gene_start)+1)/fgene$gene_length
            fIGS$rate[fIGS$rate>=0] <- fIGS$rate[fIGS$rate>=0] + 1
            gene_rate <- fgene[, c("gene_id", "rate")]
            IGS_rate <- fIGS[, c("gene_id", "rate")]
            data_rate <- rbind(gene_rate, IGS_rate)
            write.table(data_rate, 'ts.r')
            pdf("%s/%s_idd.pdf")
            ggplot(data_rate, aes(rate)) + geom_histogram(binwidth=0.04, colour="#00FFFF") + xlim(-2, 3)\
            + ggtitle("Hits in ORF or IGS distrubution of %s")
            dev.off()
            """%(tag, tag, tag, tag, tag, tag, tag)
            print(Rscript, file=f)
            f.close()
            os.system('R2 CMD BATCH %s/%s_idd.R'%(tag, tag))
        def call_R2(tag):  # colour = Chromosome
            
            f=open('%s/%s%s_isd.R'%(tag, tag, est), 'w')
            Rscript="""library("ggplot2")
            fa<-read.table("%s/%s%s_isd.xls")
            colnames(fa) <-c("Chromosome", "Insertion.site")
            pdf("%s/%s%s_isd.pdf")
            ggplot(fa, aes(Insertion.site)) + geom_density(adjust=1/5, colour="#0000FF") + xlim(-0.05, 0.01)  #binwidth=0.02
            dev.off()
            """%(tag, tag, est, tag, tag, est)
            print(Rscript, file=f)
            f.close()
            os.system('R2 CMD BATCH %s/%s%s_isd.R'%(tag, tag, est))
        call_R1(tag)

#def Pichia_TA_weblogo():
def weblogo(tag, target, units, manifest_data):
    if not os.path.exists('visualization'):os.mkdir('visualization')
    f1 = open(tag+'/'+tag+'_all_insertions.xls')
    f2 = open('%s/%s_targetextseq.txt'%(tag, tag), 'w')
    f3 = open('%s/%s_targetextprob.xls'%(tag, tag), 'w')
    #f3=open('%s/%s_basecount.txt'%(tag, tag), "w")
    genome_path = '1.Material_prep/genome.fa'
    genome_seq = Fasta(genome_path)
    Prob = {}
    Prob[0] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[1] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[2] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[3] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[4] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[5] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[6] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[7] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[8] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[9] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[10] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[11] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[12] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[13] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[14] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[15] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[16] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}
    Prob[17] = {'A':0, 'T':0, 'G':0, 'C':0, 'N':0}

    for index1, line in enumerate(islice(f1, 1, None)):
        line = line.split()
        chromosome = manifest_data['chr_accession'][line[0]]
        site = int(line[1])
        site_center = site # + len(target)/2 - 1
        if site_center>9 and site_center<len(genome_seq[chromosome])-9: #ignore head and tail insertion
            if line[2] == '+':
                targetextseq = genome_seq[chromosome][site_center-9:site_center+9]
            else:
                targetextseq = genome_seq[chromosome][site_center-10:site_center+8]
            targetextseq = str(targetextseq).upper()
            if line[2] == '-': #reverse complement target
                targetextseq = str(Seq(targetextseq).reverse_complement())

            for index2,  base in enumerate(targetextseq):
                Prob[index2][base] += 1
            print('>%s_%d\n%s'%(chromosome, index1+1, targetextseq), file=f2)
    all_base = float(index1)

    for i in range(18):
        #A_prob = Prob[i]['A'] / all_base
        #T_prob = Prob[i]['T'] / all_base
        #G_prob = Prob[i]['C'] / all_base
        #C_prob = Prob[i]['G'] / all_base
        for base in ['A', 'T', 'G', 'C']:
            base_prob = Prob[i][base] / all_base
            print(i+1, base, '%.2f'%base_prob, sep='\t', file=f3)

    f1.close()
    f2.close()
    f3.close()
    os.system("weblogo -c classic -U %s --format pdf < %s/%s_targetextseq.txt > %s/%s_weblogos.pdf"%(units, tag, tag, tag, tag))

def readcounts_analysis(tag):
    f=open('%s/%s_readcounts.r'%(tag, tag), 'w')
    Rscript="""library("ggplot2")
    dt <- read.csv("%s/%s_all_insertions.xls", sep='\t')
    dt2 <- dt[, c(1, 6)]
    pdf("%s/%s_readcounts.pdf")
    colnames(dt2) <-c("Chromosome", "reads")
    ggplot(dt2,  aes(x=reads)) + geom_bar(colour="#3EA055") \
    + scale_x_log10(breaks = scales::trans_breaks("log10",  function(x) 10^x), \
    labels = scales::trans_format("log10",  scales::math_format(10^.x))) \
    + scale_y_continuous(breaks=seq(0, max(dt2$reads)*1.2, 1000))\
    + annotation_logticks(sides="b")\
    + ggtitle("Reads distribution of %s")
    dev.off()"""%(tag, tag, tag, tag, tag)
    print(Rscript, file=f)
    f.close()
    os.system('R2 CMD BATCH %s/%s_readcounts.r'%(tag, tag))

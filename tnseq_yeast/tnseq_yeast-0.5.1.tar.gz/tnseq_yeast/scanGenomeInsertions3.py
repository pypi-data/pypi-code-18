"""
visualization is a module visualizing tnseq data. 
main function:
a) Insertion_distribution function is used to analyze the distribution of transposon insertion overlaid across Chromosomes. Also used to produce artemis and DNAplot data.
b) Gene_igs_analysis function is for analysis of the insertion density of gene and IGS.
c) weblogo function will call weblogo program to test the target bias of transposon.
d) readcounts_analysis function is applied to analyze the number of same reads from the high-through sequencing.
"""

from __future__ import print_function
import os, sys
import numpy as np
import pandas as pd
from Bio.Seq import Seq
from pyfaidx import Fasta
from itertools import islice
import matplotlib.pyplot as plt
import prepareMaterial


all_function = {'w':'wigfile_creation(tag, manifest_data)', 
                'g':'gene_gaps(tag)',
                'i':'Insertion_distribution(tag, target, manifest_data).plot_plt(window, yplot, read_count)',
                'l':'weblogo(tag, target, units, manifest_data)',
                'r':'Reads_normalization(tag, target, manifest_data).normalization(local_size)',
                't':'Test2(tag).t1(3)',
                }

def wigfile_creation(tag, manifest_data):
    df_target = pd.read_table('1.Material_prep/TA_sites.bed', usecols=[0, 1], names=['chromosome', 'insertions'])
    df_target['init'] = 0
    df_alldp = pd.read_table('%s/%s_all_insertions.xls'%(tag, tag), usecols=[0, 1, 2])
    df_alldp['insertions'] = np.where(df_alldp['insert_direct']=='-', df_alldp['insertions']-1, df_alldp['insertions'])
    dgb_alldp = pd.DataFrame(df_alldp.groupby(['chromosome', 'insertions']).size())
    df_merge = pd.merge(df_target, dgb_alldp, left_on=['chromosome', 'insertions'], right_index=True, how='outer')
    df_merge = df_merge.fillna(0)
    df_merge['hitcounts'] = df_merge['init'] + df_merge[0]
    for chro in manifest_data['chr_accession']:
        df_merge[df_merge['chromosome'] == chro].iloc[:, [1, 4]].to_csv('%s/%s_%s.wig'%(tag, tag, chro), sep='\t', index=False, header=None)

def gene_gaps(tag):
    df = pd.read_table('%s/%s_all_gene.xls'%(tag, tag),usecols=['gene_id', 'gene_start', 'gene_end', 'insert_site'])

    def calculate_gaps(df):
        df_rowf = pd.DataFrame(df[:1].values,columns=['gene_id', 'gene_start', 'gene_end', 'insert_site'])
        df_rowl = pd.DataFrame(df[-1:].values,columns=['gene_id', 'gene_start', 'gene_end', 'insert_site'])
        
        df_rowf['insert_site'] = min(df_rowf.values[0][1:3])
        df_rowl['insert_site'] = max(df_rowl.values[0][1:3])
        df1 = df_rowf.append(df, ignore_index=True)
        df2 = df.append(df_rowl, ignore_index=True)
        #df['gaps'] = df2['insert_site'] - df1['insert_site']
        #print(df2[:10])
        #sys.exit(df2)
        return df2['insert_site'] - df1['insert_site']
    df_gaps = df.groupby('gene_id').apply(calculate_gaps)
    df_gaps.to_csv('%s/%s_gaps.xls'%(tag, tag), sep='\t')

def insertion_gaps(tag,manifest_data,size):
    df = pd.read_table('%s/%s_alldp.xls'%(tag,tag),usecols=[0,1],names=['chro','target_site'])
    for index,chro in enumerate(manifest_data['chr_accession']):
        df_chro = df[df['chro'] == chro]
        df_chro['start'] = np.append(0,np.array(df_chro['target_site'][:-1]))
        df_chro['diff'] = df_chro['target_site'] - df_chro['start']
        df_chro_select = df_chro[df_chro['diff'] >= size]
        df_total1 = df_chro if not index else df_total1.append(df_chro)
        df_total2 = df_chro_select if not index else df_total2.append(df_chro_select)
        print(chro,len(df_chro_select))
    df_total1.iloc[:,[0,2,1,3]].to_csv('%s/%s_insertion_gaps.xls'%(tag,tag),sep='\t',index=False,header=['chr','start','end','diff'])
    df_total2.iloc[:,[0,2,1,3]].to_csv('%s/%s_insertion_gaps_size%d.xls'%(tag,tag,size),sep='\t',index=False,header=['chr','start','end','diff'])


class Insertion_distribution():
    """
    Produce distribution data of transposon insertion overlaid across Chromosomes 
    and data used for artemis and DNAplot.
    """
    def __init__(self, tag, target, manifest_data):
        self.tag = tag
        self.target = target
        self.manifest_data = manifest_data
        self.genome_seq = Fasta(manifest_data["genome_path"])

    def plot_plt(self, window, yplot, read_count):
        df = pd.read_table('%s/%s_all_insertions.xls'%(self.tag, self.tag),
             usecols=['chromosome', 'insertions', 'insert_direct', 'count2'])
        datalist = []

        for chro,accession in self.manifest_data['chr_accession'].items():
            filename = self.data_processing(df, chro, accession, window, read_count)
            datalist.append(filename)

        fig, ax_list = plt.subplots(nrows=len(datalist))
        ax_list[0].set_title('%s/%s_insertcounts_distribution'%(self.tag, self.tag), color='blue')
        font = {'family': 'serif', 
                'color':  'darkred', 
                'weight': 'normal', 
                'size': 16, 
                }
        for index, data in enumerate(datalist): #datalist.reverse() [::-1]
            chro = data.split("_")[-3] #extract chromosome
            df = pd.read_table(data)
            sliding_window_path = '1.Material_prep/%s_%s_sliding-window_%d.txt'%(self.target, chro, window)
            if not os.path.exists(sliding_window_path):
                prepareMaterial.targetbases_genomewide_distribute(self.manifest_data, window, self.target)
            df_genome = pd.read_table(sliding_window_path)
            ax_list[index].set_xlim(xmax=len(df['counts']))
            ax_list[index].set_xticks(map(lambda x: x*1000 / window, [0, 1000, 2000, 3000])) #len(df['chromosome'])
            #ax_list[index].set_aspect(4)
            if yplot:
                ax_list[index].set_ylim((0, yplot))
            #ax_list[index].set_adjustable("datalim")
            ax_list[index].vlines(df_genome['win_seqNo'], [0], df_genome['count'], colors='#C6E2FF')
            ax_list[index].vlines(df['win_seqNo'], [0], df['counts']/df['hits_num'], colors='#66CDAA')
            # set ticks
            ax_list[index].tick_params(axis='y', labelsize=8)
            ##ax_list[index].set_yticks([20, 60, 100])
            # Hide the top and the right spines
            ax_list[index].spines['top'].set_visible(False)
            ax_list[index].spines['right'].set_visible(False)
            # Only show ticks on the bottom spines
            ax_list[index].xaxis.set_ticks_position('bottom')
            ax_list[index].yaxis.set_ticks_position('left')
            ax_list[index].set_ylabel(chro,  fontdict=font)
        plt.savefig('%s/%s_insertcounts_distribution_%d.pdf'%(self.tag, self.tag, window))

    def chro_coordinate(self, chro, accession):
        chrsize = len(self.genome_seq[accession])
        arr_coordinate = np.arange(1, chrsize + 1)
        df_coordinate = pd.DataFrame({'chro_coordinate':arr_coordinate})
        return df_coordinate

    def data_processing(self, df, chro, accession, window, read_count):
        df_chro = df[df['chromosome']==chro]

        if read_count:
            df_chro = df_chro.rename(columns={'count2': 'counts'})
            del df_chro['chromosome']
        else: 
            del df_chro['count2']
            df_chro = df_chro.rename(columns={'chromosome': 'counts'})
            df_chro = df_chro.groupby(['insertions', 'insert_direct'], as_index=False).count()

        df_chro['F'] = np.where(df_chro['insert_direct']=='+', df_chro['counts'], 0)
        df_chro['R'] = np.where(df_chro['insert_direct']=='-', -1 * df_chro['counts'], 0)        
        df_coordinate = self.chro_coordinate(chro, accession)
        df_map = pd.merge(df_coordinate, df_chro, left_on='chro_coordinate', right_on='insertions', how='left')
        df_map = df_map.fillna(0)

        df_map['win_seqNo'] = (df_map['chro_coordinate']-1) // window + 1 
        slide_file = '%s/slide_%s'%(self.tag, window)
        if not os.path.exists(slide_file):
            os.mkdir(slide_file)

        global count
        count = 0
        def count_nonzero(col):
            global count
            count += 1
            # Export read counts of hits in one sliding-window
            #col[col.values != 0].to_csv(slide_file + '/%s_%d.xls'%(chro, count), sep='\t')
            return np.count_nonzero(col)
            
        def median(col):
            col2 = col[col.values != 0]
            return np.median(col2)

        df_map_comb = df_map.iloc[:, [3, 4, 5, 6]].groupby(['win_seqNo']).agg({'counts':[sum, median, np.std, count_nonzero],
                                                                               'F':[sum, np.std],'R':[sum, np.std]})
        df_map_comb.columns = ['counts', 'counts_median', 'counts_std', 'hits_num', 'F', 'F_std', 'R', 'R_std']
        df_map_comb.reindex(columns=sorted(df_map_comb.columns)) #; sys.exit(df_map_comb)
        df_map_comb.to_csv('%s/%s_%s_sliding-window_%d.xls'%(self.tag, self.tag, chro, window), sep='\t')

        """
        Generate data used for artemis and DNAplot
        """
        DNAplot_p = '%s/%s_%s_plus.txt'%(self.tag, self.tag, chro)
        DNAplot_m = '%s/%s_%s_minus.txt'%(self.tag, self.tag, chro)
        artemis = '%s/%s_%s_artemis.txt'%(self.tag, self.tag, chro)
        if not os.path.exists(DNAplot_p):
            df_map.to_csv(DNAplot_p, sep='\t', index=False, columns=['F'], header=False)
        if not os.path.exists(DNAplot_p):
            df_map.to_csv(DNAplot_m, sep='\t', index=False, columns=['R'], header=False)
        if not os.path.exists(DNAplot_p):
            df_map_mod = df_map[df_map['insertions']!=0]
            df_map_mod.to_csv(artemis, sep='\t', index=False, columns=['insertions', 'F', 'R'])
        return '%s/%s_%s_sliding-window_%d.xls'%(self.tag, self.tag, chro, window)


class Reads_normalization(Insertion_distribution):

    def normalization(self, local_size):
        for chro, accession in self.manifest_data['chr_accession'].items():
            self.chro_normalization(local_size, chro, accession)

    def chro_normalization(self, local_size, chro, accession):
        df = pd.read_table('%s/%s_all_insertions.xls'%(self.tag, self.tag),
             usecols=['chromosome', 'insertions', 'insert_direct', 'count2']
             )
        df_chro = df[df['chromosome']==chro]
        df_coordinate = self.chro_coordinate(chro, accession)
        df_map = pd.merge(df_coordinate, df_chro, left_on='chro_coordinate',
                 right_on='insertions', how='left')
        df_map = df_map.fillna(0)
        #df_map2 = df_map[df_map['count2']!=0]
        local_size2 = 0.5 * local_size 
        dt_norm = []
        df_sr = df.iloc[:,[1,3]].values
        #np_reads = df['count2'].values
        site_end = df_map['chro_coordinate'].values[-1]

        for site, read_counts in df_sr:
            
            if site < local_size2:
                site_up = 0
                site_down = local_size #;print(1,site_up)
            elif site + local_size2 > site_end:
                site_up = int(site_end - local_size + 1)
                site_down = int(site_end + 1) #;print(2)
            else:
                site_up = int(site - local_size2)
                site_down = int(site + local_size2) #;print(site_up)
            df_local = df_map[site_up:site_down]
            df_local = df_local[df_local['count2']!=0]
            print(df_map[df_map['chro_coordinate']==1312883]);sys.exit()
            np_local_reads = df_local['count2'].values 
            np_local_reads = np.sort(np_local_reads)#;print(np_local_reads,read_counts);
            reads_index_list = np.where(np_local_reads==read_counts)#;print(len(reads_index_list[0]))
            if not len(reads_index_list[0]):
                print(site,site_up,site_down)
            reads_index_mean = np.mean(reads_index_list) + 1
            reads_median = np.median(np_local_reads)
            reads_num = len(np_local_reads)
            median_index = 0.5 * (reads_num + 1)
            index_delta = reads_index_mean - median_index
                
            def sigmoid_deri(x, a, b):
                return 2*a / (1+np.exp(-5*x/b))

            x = index_delta
            a = reads_median
            b = reads_num
            reads_norm = sigmoid_deri(x, a, b)
            dt_norm.append(reads_norm)
        print(dt_norm);sys.exit()


class Gene_igs_analysis():
    def __init__(self, tag):
        """Insertion site distribution at yeast transcription start sites (TSS), intergenic regions
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

class Test1():
    count = 1
    def __init__(self,b):
        self.a = 1
        self.__t1(b)
    
    def __t1(self,b):
        print(self.a, b)

class Test2(Test1):
    def t1(self,c):
        print(self.a,c+1)
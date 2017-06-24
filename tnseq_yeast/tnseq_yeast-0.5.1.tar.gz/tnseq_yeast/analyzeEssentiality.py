# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------#
# USAGE: ./jx                                                                        #
# AUTHOR: ZJX (Jim Chu), biojxz@gmail.com                                            #
# ORGANIZATION: ECUST                                                                #
# VERSION: 1.0                                                                       #
# CREATED: 2016年08月23日 15时20分01秒                                               #
#------------------------------------------------------------------------------------#

from __future__ import print_function
import os
import sys
import yaml
import numpy as np
import pandas as pd
from pyfaidx import Fasta
import visualization as vis
from itertools import islice
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

all_function = {'w':'wigfile_creation(tag,manifest_data)','s':'targetcounts_vs_length(tag,manifest_data,bin)',\
'g':'gene_integration_densities(dirfile,all_insert,estype,reads_limit,TAcounts)','e':'es_map(tag,estypefile)',\
'p':'es_promoter(tag)','f':'insert_freq_compare(dirfile)','p':'essentiality_prob(dirfile)','c':'compare(dirfile)'}

def wigfile_creation(tag,manifest_data):
    df_target = pd.read_table('material_prep/TA_sites.bed',usecols=[0,1],names=['chro','target_site'])
    df_target['init'] = 0
    df_alldp = pd.read_table('%s/%s_alldp.xls'%(tag,tag),usecols=[0,1,2],names=['chro','insert_site','direction'])
    df_alldp['insert_site'] = np.where(df_alldp['direction']=='-',df_alldp['insert_site']-1,df_alldp['insert_site'])
    dgb_alldp = pd.DataFrame(df_alldp.groupby(['chro','insert_site']).size())
    ##how to make sure int instead of float,maybe use groupby after df_target plus dgb_alldp
    df_merge = pd.merge(df_target,dgb_alldp,left_on=['chro','target_site'],right_index=True,how='outer')
    df_merge = df_merge.fillna(0)
    df_merge['hitcounts'] = df_merge['init'] + df_merge[0]
    for chro in manifest_data['chr_accession']:
        df_merge[df_merge['chro']==chro].iloc[:,[1,4]].to_csv('%s/%s_%s.wig'%(tag,tag,chro),sep='\t',index=False,header=None)

class targetcounts_vs_length():
    def __init__(self,tag,manifest_data,bin):
        self.tag = tag
        self.manifest_data = manifest_data
        self.sliding_window_method(bin)

    #分析指定文件夹内'*_CDS.xls'类文件的基因内部插入个数及位置
    #参考Henry L. Levin的方法，必须基因非必须基因的分界线：20 inserts/kb/million
    def sliding_window_method(self,bin):
        f = open('%s/%s_sliding_window_length_%d.xls'%(self.tag,self.tag,bin),'w')
        f2 = open('%s/%s_sliding_window_targetcounts_%d.xls'%(self.tag,self.tag,bin),'w')
        genome = Fasta(self.manifest_data['genome_path'])
        df_target = pd.read_table('1.material_prep/TA_sites.bed',usecols=[0,1],names=['chromosome','target_site'])
        df_alldp = pd.read_table('%s/%s_all_insertions.xls'%(self.tag,self.tag),usecols=[0,1])
        
        # genome lenght sliding window
        for index,(chro,accession) in enumerate(self.manifest_data['chr_accession'].items()):
            arr = np.arange(len(genome[accession]))
            df = pd.DataFrame(arr,columns=['site'])
            df['chromosome'] = chro
            df_total = df if not index else df_total.append(df)
        
        df_genomewide = pd.merge(df_total,df_target,left_on=['chromosome','site'],right_on=['chromosome','target_site'],how='outer')
        df_genomewide['target_site'] = np.where(df_genomewide['target_site'].isnull(),0,1)
        df_genomewide = pd.merge(df_genomewide,df_alldp,left_on=['chromosome','site'],right_on=['chromosome','insertions'],how='outer')
        df_genomewide['insertions'] = np.where(df_genomewide['insertions'].isnull(),0,1)
        shifting = bin / 100
        for chro,accession in self.manifest_data['chr_accession'].items():
            chro_len = len(genome[accession])
            bin_num = (chro_len - bin)/shifting + 1
            for index,i in enumerate(range(bin_num)):
                bin_start = i*shifting
                bin_end = bin_start + bin
                TA_count = df_genomewide[df_genomewide['chromosome']==chro]['target_site'].iloc[bin_start:bin_end].sum()
                insert_count = df_genomewide[df_genomewide['chromosome']==chro]['insertions'].iloc[bin_start:bin_end].sum()
                print(chro,index,bin_end,TA_count,insert_count,sep='\t',file=f)
        
        # genome target sliding window
        df_genomewide2 = pd.merge(df_total,df_target,left_on=['chromosome','site'],right_on=['chromosome','target_site'],how='right')
        multiple = 1.0 * chro_len / len(df_genomewide2[df_genomewide2['chromosome']==chro])
        bin2 = int(bin / multiple)
        shifting2 = bin2 / 100
        for index,(chro,accession) in enumerate(self.manifest_data['chr_accession'].items()):
            df_genomewide2_chro = df_genomewide2[df_genomewide2['chromosome']==chro]
            chro_targetcounts = len(df_genomewide2_chro)
            df_genomewide2_chro['target_accumu'] = np.arange(chro_targetcounts)
            bin_num2 = (chro_targetcounts - bin2)/shifting2 + 1
            for index,i in enumerate(range(bin_num2)):
                bin_start2 = i*shifting2
                bin_end2 = bin_start2 + bin2
                bin_start2_corr = df_genomewide2_chro[df_genomewide2_chro['target_accumu']==bin_start2].iloc[0,2]
                bin_end2_corr = df_genomewide2_chro[df_genomewide2_chro['target_accumu']==bin_end2].iloc[0,2]
                genome_lenght = bin_end2_corr - bin_start2_corr + 1
                insert_count = df_genomewide[df_genomewide['chromosome']==chro]['insertions'].iloc[bin_start2_corr:bin_end2_corr].sum()
                print(chro,index,bin_end2,genome_lenght,insert_count,sep='\t',file=f2)

        f.close()
        f2.close()
        self.figwithR(bin)

    def figwithR(self,bin):
        file_Rscript = '%s/%s_figwithR.R'%(self.tag,self.tag)
        f = open(file_Rscript,'w')
        Rscript = """library('ggplot2')
        a <- read.table('%s/%s_sliding_window_length_%d.xls')
        b <- read.table('%s/%s_sliding_window_targetcounts_%d.xls')
        colnames(a) <- c('chromosome','index','bin_end','TA_count','insert_count')
        colnames(b) <- c('chromosome','index','bin_end','genome_length','insert_count')
        pdf("%s/%s_sliding_window_length.pdf")
        qplot(TA_count,insert_count,data = a,colour = chromosome)+geom_smooth(aes(x=TA_count,y=insert_count),method='lm')
        dev.off()
        pdf("%s/%s_sliding_window_targetcounts.pdf")
        qplot(genome_length,insert_count,data = b,colour = chromosome)+geom_smooth(aes(x=genome_length,y=insert_count),method='lm')
        dev.off()
        """%(self.tag,self.tag,bin,self.tag,self.tag,bin,self.tag,self.tag,self.tag,self.tag)
        print(Rscript,file=f)
        f.close()
        os.system('R2 CMD BATCH %s'%file_Rscript)


class gene_integration_densities():
    def __init__(self,dirfile,all_insert,estype,reads_limit,TAcounts):
        self.dirfile = dirfile[0]
        self.tag = dirfile[0].split('/')[0].split('.')[0]
        self.all_insert = all_insert
        self.estype = estype
        self.reads_limit = reads_limit
        self.TAcounts = TAcounts
        self.data_process()
        self.esidd_draw_with_R()

    # 2016.11.21 modify
    def data_process(self):
        # orf integration densities
        df = pd.read_table(self.dirfile,usecols=[0,2,4,5,7]) # names=['gene_id','gene_start','gene_length','insert_site'
        df_annot = pd.read_table('1.material_prep/annot_gene2.xls',usecols=[0,2,4,5,6]) 
        # limit sequencing reads of gene insertions
        df = df[df['reads'] > self.reads_limit]
        df['ratio_length'] = abs(df['insert_site']-df['gene_start'])/df['gene_length']
        # remove 10% seq near 3' terminator
        df_remove = df[df['ratio_length']<0.9]
        del df_remove["gene_length"]
        #dgb = pd.merge(df,dgb_size,left_on=["gene_id"],right_index=True,how='left')
        # 计算某基因所有插入位点率的总和
        # dgb = df.groupby(['chr','gene_id','gene_length','annot']).count()['insert_site']
        grouped = df_remove.loc[:,['gene_id','ratio_length']].groupby('gene_id',as_index=False)
        df_hits = df_remove.merge(grouped.count(),on='gene_id',how='left')
        df_hits_ave = df_hits.merge(grouped.mean(),on='gene_id',how='left')
        df_final = df_hits_ave.merge(df_annot,on=['gene_id','gene_start'],how='outer')
        if self.all_insert:
            all_insert_actually = self.all_insert
            print("# All insertion counts refer to all independent insertions.")
        else:
            all_insert_actually = grouped1.count()['ratio_length'].sum()
            print("# All insertion counts refer to all insertions in genes.")
        if self.TAcounts:  #TAcounts of 90% 3'near gene is 71.882
            df_final['insert_freq'] = 1000000*72*df_final['ratio_length_y']/(all_insert_actually*df_final['TAcounts'])
        else:
            df_final['insert_freq'] = 1000000*1442.7*df_final['ratio_length_y']/(all_insert_actually*df_final['gene_length'])

        df_final = df_final.fillna(0)
        """df_insertcounts = pd.DataFrame(df_edition1[df_edition1['ratio_length'] < 0.9].groupby(['gene_id'],as_index=False).size())
        df_insert_TA_counts = pd.merge(df_TAcounts,df_insertcounts,left_on=['chr','gene_id'],right_index=['chr','gene_id'],how='left')
        df_insert_TA_counts = df_insert_TA_counts.fillna(0)
        df_insert_TA_counts.to_csv('7.Essential_analysis/%s_insertvsTAcounts.xls'%tag,sep='\t',index=False,header=['chr','gene_id','TAcounts','insertcounts'])"""
        # output gene insertion density distribution information
        df_final.to_csv('%s/%s_geneidd_detail.xls'%(self.tag,self.tag),sep='\t',index=False,\
        header=['gene_id','gene_start','insert_site','reads','ratio_length','hits_num','ratio_length_ave','gene_length','TAcounts','gene_annotion','insert_freq'])

        # map Sc or Sp essential gene tag to geneidd data
        df_estag = pd.read_table("1.material_prep/%s_estype.txt"%self.estype)
        df_new = df_final.loc[:,['gene_id','insert_freq','reads','TAcounts','gene_annotation']]
        df_new = df_new.groupby(['gene_id','insert_freq','TAcounts','gene_annotation'],as_index=False).sum()
        df_new["ratio_reads"] = df_new["reads"] / df_new["TAcounts"]
        df_estag_map = df_new.merge(df_estag,on='gene_id',how='left')
        # df_estag_map = df_estag_map.drop_duplicates()
        df_estag_map = df_estag_map.fillna('NE')
        df_estag_map['tag'] = np.where(df_estag_map['mapES'].str.contains('ES'),'Essential','Non-essential')
        df_estag_map.to_csv('%s/%s_geneidd_%s_fig.xls'%(self.tag,self.tag,self.estype),sep='\t',index=False)

    def esidd_draw_with_R(self):
        f = open('%s/%s_esidd.R'%(self.tag,self.tag),'w')
        Rscript="""library("ggplot2")
        dt <- read.csv("%s/%s_geneidd_%s_fig.xls",sep='\t',header=T)
        pdf("%s/%s_geneidd_%s.pdf")
        ggplot(dt,aes(insert_freq,..count..)) + geom_density(aes(colour=tag),adjust = 1/5) + scale_x_continuous(breaks=seq(0,300,50))\
        + ggtitle("%s integration densities of ORFs homology to %s essential ORFs ")+theme(plot.title=element_text(size=rel(0.8),colour="#CD7F32"))\
        + xlim(0,400) 
        dev.off()"""%(self.tag,self.tag,self.estype,self.tag,self.tag,self.estype,self.tag,self.estype)
        print(Rscript,file=f)
        f.close()
        os.system('R CMD BATCH %s/%s_esidd.R'%(self.tag,self.tag))

def insert_freq_compare(dirfile):
    if not os.path.exists('12.Insert_freq_compare'): os.mkdir('12.Insert_freq_compare')
    for index,dn in enumerate(dirfile):
        tag = dn.split('/')[0]
        df = pd.read_table(dn)
        df_sort = df.sort_values(by='insert_freq').reset_index(drop=True)

        if index:
            df_es[tag] = df_sort.iloc[:1500,0]
            tag_all = tag_all + '-'+tag
        else:
            df_es = pd.DataFrame({tag:df_sort.iloc[:1500,0]})
            tag_all = tag
    df_es.to_csv('12.Insert_freq_compare/%s_insert_freq_compare.xls'%tag_all,sep='\t',index=False)
    f = open('12.Insert_freq_compare/insert_freq_compare.R','w')
    Rscript="""
    library("VennDiagram")
    dt <- read.csv("12.Insert_freq_compare/%s_insert_freq_compare.xls",sep='\t',header=T)
    venn.diagram(dt,"12.Insert_freq_compare/%s_vn.png",col = "transparent",fill = c("cornflowerblue", "green")\
    ,alpha = 0.50)
    """%(tag_all,tag_all)
    print(Rscript,file=f)
    f.close()
    os.system('Rscript 12.Insert_freq_compare/insert_freq_compare.R')


class es_promoter():
    def __init__(self,tag):
        self.es_prom(tag)

    def es_prom(self,tag):
        df = pd.read_table('%s/%s_geneidd_detail.xls'%(tag,tag),usecols=['gene_id','gene_start','gene_length','insert_site','TAcounts','insert_freq'])
        df_IGS = pd.read_table('%s/%s_all_IGS.xls'%(tag,tag))
        #df_es = df[df['insert_site']>0]
        df_es = df[(df['insert_freq']<25) & (df['TAcounts']>50)]
        #df_es = df_es[df_es['TAcounts']>50]
        df_nes = df[df['insert_freq']>380]
        df_es.loc[:,['gene_id','gene_start','gene_length','insert_site']].to_csv('%s/%s_es.xls'%(tag,tag),index=False,sep='\t')
        df_nes.loc[:,['gene_id','gene_start','gene_length','insert_site']].to_csv('%s/%s_nes.xls'%(tag,tag),index=False,sep='\t')
        self.drawwithR(tag,'es')
        self.drawwithR(tag,'nes')

    def drawwithR(self,tag,est):
        f=open('%s/%s_idd_est.R'%(tag,tag),'w')
        Rscript="""library("ggplot2")
        fgene <- read.table("%s/%s_%s.xls",sep='\t',header=T)
        fIGS0 <- read.table("%s/%s_all_IGS.xls",sep='\t',header=T)
        fgene$rate <- (abs(fgene$insert_site - fgene$gene_start)+1)/fgene$gene_length
        fgene_uniq <- unique(fgene[,c('gene_id','gene_start')])
        fIGS <- merge(fIGS0,fgene_uniq,by='gene_id')
        fIGS$rate[fIGS$rate>=0] <- fIGS$rate[fIGS$rate>=0] + 1
        gene_rate <- fgene[,c("gene_id","rate")]
        IGS_rate <- fIGS[,c("gene_id","rate")]
        data_rate <- rbind(gene_rate,IGS_rate)
        pdf("%s/%s_idd_%s.pdf")
        ggplot(data_rate,aes(rate)) + geom_histogram(binwidth=0.005,colour="#00FFFF") + xlim(-0.1,0)\
        + ggtitle("Hits in ORF or IGS distrubution of %s")
        dev.off()
        """%(tag,tag,est,tag,tag,tag,tag,est,tag)
        print(Rscript,file=f)
        f.close()
        os.system('Rscript %s/%s_idd_est.R'%(tag,tag))


def insertvsTAcounts_fig(tag):
    file_Rscript = '7.Essential_analysis/%s_insertvsTAcounts.R'%tag
    f = open(file_Rscript,'w')
    Rscript = """library('ggplot2')
    a <- read.table('7.Essential_analysis/%s_insertvsTAcounts.xls',header = TRUE)
    pdf("7.Essential_analysis/%s_insertvsTAcounts.pdf")
    qplot(insertcounts/TAcounts,data = a,geom = "density",colour=chr,adjust = 1/5)
    dev.off()
    """%(tag,tag)
    print(Rscript,file=f)
    f.close()
    os.system('R2 CMD BATCH %s'%file_Rscript)


class condiff:
    """
    1. Build model of gene essentiality assessment by Machine-learning
    2. Calculate the probability of gene essentiality in different culture condition
    3. Compare gene essentiality in different culture condition
    """
    def __init__(self,tag,tag2):
        self.tag = tag
        self.essentiality_prob() 
        
    def build_model(self):

        return 5.825,7.789,1.849
    
def essentiality_prob(dirfile):
    tag = dirfile[0].split('/')[0].split('.')[0]
    def probability(x1,x2,w0,w1,w2):
        return 1 / (1 + np.exp(-(w0 + w1 * value_std[:,0] + w2 * value_std[:,1])))
    df = pd.read_table(dirfile[0],usecols=[0,1,2,3,4]) # names=['gene_id','insert_freq','reads']
    stdsc = StandardScaler()
    value = df.iloc[:,[1,4]].values
    value_std = stdsc.fit_transform(value)
    w0,w1,w2 = 5.825,7.789,1.849 #build_model()
    df["probability"] = probability(value_std[:,0],value_std[:,1],w0,w1,w2)
    df.to_csv("%s/%s_probability.xls"%(tag,tag),sep="\t",index=False)

def compare(dirfile):
    tag = dirfile[0].split('/')[0].split('.')[0]
    tag2 = dirfile[1].split('/')[0].split('.')[0]
    df1 = pd.read_table("%s/%s_probability.xls"%(tag,tag))
    df2 = pd.read_table("%s/%s_probability.xls"%(tag2,tag2))
    df_merge = pd.merge(df1,df2,on=['gene_id','TAcounts','gene_annotation'],how='outer')
    df_merge['condiff'] = df_merge['probability_x'] - df_merge['probability_y']
    df_merge_adj = df_merge.iloc[:,[0,1,4,5,6,7,8,9,2,3]]
    df_merge_adj.to_csv("%s/%s-%s_condiff.xls"%(tag2,tag,tag2),sep="\t",index=False)


if __name__ == '__main__':
    manifest_data = yaml.load(open('manifest.yaml'))
    tag = sys.argv[1]
    bin = int(sys.argv[2])
    shifting = int(sys.argv[3])
    sliding_window_method(tag,manifest_data,bin,shifting)
    TA_insertcounts_fig(tag,bin,shifting) #gene_insert_distribute(tag,0)
    insertvsTAcounts_fig(tag)
    #TA_insertcounts2(tag)



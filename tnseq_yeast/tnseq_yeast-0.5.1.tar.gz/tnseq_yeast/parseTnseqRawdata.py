# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import shutil
import numpy as np
import pandas as pd
from Bio.Seq import Seq
from itertools import islice
import multiprocessing as mp

"""
Finds and removes adapter sequences and primers of unwanted sequence such as 
transposon sequences and index primer from high-throughput sequencing reads.
Take TcBuster mutant libraries as examples, reads containing TcBuster sequence AAAGGTTGAAGAACACTG from the 5¡¯ end 
were trimmed to remove transposon, and those reads without transposon sequence were discarded completely 
(command line options cutadapt -g AAAGGTTGAAGAACACTG -O 17 -e 0.2  --match-read-wildcards --discard-untrimmed -f fastq)
Remaining reads were further trimmed to find and remove partial adapter sequence ATACCACGAC from the 3¡¯ end 
(cutadapt -a ATACCACGAC -O 5 -e 0.1 -m 10 -f fastq -o 3.Cutadapt_trimmed/tss4_t_l 3.Cutadapt_trimmed/tss4_t)
"""




def cutadapt(Tndata,transposon,manifest_data,tag,core_num,select,Lmax,ut):

    ADAPTER_HEAD = manifest_data['transposon'][transposon]
    #ADAPTER_REV = str(Seq(ADAPTER_HEAD).reverse_complement())
    ADAPTER_TAIL = manifest_data['tail_adapter']
    #ADAPTER_TAIL = 'GTCGTGGTAT'
    if 1:#tag + '-trimmed.fastq' not in os.listdir('3.Cutadapt_trimmed'):
        os.system("skewer -r 0.03 -m head -x %s -t %s -L %s %s 2.Tndata_raw/%s -o 3.Cutadapt_trimmed/%s"\
        %(ADAPTER_HEAD,core_num,Lmax,ut,Tndata,tag))

    if select: #tag_cutadapt not in os.listdir('3.Cutadapt_trimmed'):
        os.system("skewer -Q 40 -m tail -t %s -x %s -l 16 -L 50 -e 3.Cutadapt_trimmed/%s-trimmed.fastq \
        -o 3.Cutadapt_trimmed/%s-trimmed"%(core_num,ADAPTER_TAIL,tag,tag))
    print("\n========== Skewer finished for: %s ==========\n\n"%Tndata) 

#align to pichia pastoris genome
def bowtie(tag,core_num):
    tag_cutadapt = tag + '-trimmed-trimmed.fastq'
    tag_bowtie = tag + '_bowtie.txt'
    if 1:#tag_bowtie not in os.listdir('4.Bowtie_data_dir'):
        os.system("bowtie -p %s -v 3 -a --best --strata -y -m 1 -q pichia/genome \
        3.Cutadapt_trimmed/%s 4.Bowtie_data_dir/%s"%(core_num,tag_cutadapt,tag_bowtie))
    print("\n========== Bowtie finished for: %s ==========\n\n"%tag_cutadapt)

#remove reads duplicates
def unique(file_impt,tag,transposon,manifest_data):
    if not os.path.exists(tag):os.mkdir(tag)
    ## debug:
    print(file_impt,tag,transposon)
    df = pd.read_table("%s"%file_impt,header=None,usecols=[1,2,3,4],names=['insert_direct','chro','site','seq'])
    #drop the length of site base is less 20bp
    df=df[df['seq'].map(lambda x:len(x)>20)]#.iloc[:,[2,3,1,4]] ##limit the length of reads if necessary
    #site amendment
    if 'TcB' in transposon:
        df['site_amdt'] = np.where(df['insert_direct']=='+',df['site']+4,df['site']+df['seq'].str.len()-3)  #whether forword site is the same as inverse site
    elif 'SB' in transposon:
        df['site_amdt'] = np.where(df['insert_direct']=='+',df['site']+1,df['site']+df['seq'].str.len())
    elif 'PB' in transposon:
        df['site_amdt'] = np.where(df['insert_direct']=='+',df['site']+2,df['site']+df['seq'].str.len()-1)
    if 'L' in transposon: #transfer to 'TIRR' format
        df['site_amdt'] = np.where(df['insert_direct']=='+',df['site_amdt']+1,df['site_amdt']-1)
        df['seq'] = [str(Seq(x).reverse_complement()) for x in df['seq']]
        df['insert_direct'] = df['insert_direct'].apply(lambda x: '-' if x=='+' else '+')  ##pandas combining lambda is useful
    #count every same read num
    dg1 = df.groupby(['chro','site_amdt','insert_direct','seq'],as_index=False).count()  #count the total insertion reads of every site
    dg2 = df.iloc[:,[1,2,0,4]].groupby(['chro','site_amdt','insert_direct']).count()
    #count the length of reads
    dg1['seq_length']=df['seq'].str.len()
    def dereplicate1(df,n=1,columns1='site',columns2='seq_length'):
        #this sort will miss long length of site base
        return df.sort_values(by=[columns1,columns2])[-n:]
    #df_dere1 is the first dereplicated DataFrame
    df_dere1 = dg1.groupby(['chro','site_amdt','insert_direct'],group_keys=False).apply(dereplicate1)
    df_dere1 = pd.merge(df_dere1,dg2,left_on=['chro','site_amdt','insert_direct'],right_index=True,how='left').drop('seq_length',axis=1)

    def dereplicate2(chro_ac,chro,transposon):  #mark similar reads
        df_chro = df_dere1[df_dere1['chro']==chro_ac]
        chro_row_df = df_chro.values #converting DataFrame to array
        a0,e0,b0,Ta0,D1 = 0,0,"str","str",{}
        for i in chro_row_df:
            [a,c,b,d,e] = i[1:]  #a:site,c:insert_direct,b:seq,e:counts
            if 'SB' in transposon:
                Ta = b[:2] if c == '+' else b[-2:]
            elif 'TcB' in transposon:
                Ta = b[3:5] if c == '+' else b[-5:-3]
            elif 'PB' in transposon:
                Ta = b[1:3] if c == '+' else b[-3:-1]
            if a > a0+2:
                D1[str(a)+c]='Unique_read'
            else:  
                if c==c0:
                    if Ta=='TA' and Ta0=='TA':
                        if e>e0:
                            if a==a0+1:
                                D1[str(a)+c],D1[str(a0)+c0]='Remain1','Similar1'
                            else:
                                D1[str(a)+c],D1[str(a0)+c0]='SimTRemain1','SimTRemain1'
                        elif e<e0:
                            if a==a0+1:
                                D1[str(a)+c],D1[str(a0)+c0]='Similar1','Remain1'
                            else:                            
                                D1[str(a)+c],D1[str(a0)+c0]='SimTRemain1','SimTRemain1'
                        else:
                            if a==a0+1:
                                if len(b) > len(b0):
                                    D1[str(a)+c],D1[str(a0)+c0]='Remain2','Similar2'
                                else:
                                    D1[str(a)+c],D1[str(a0)+c0]='Similar2','Remain2'
                            else:                            
                                D1[str(a)+c],D1[str(a0)+c0]='SimTRemain2','SimTRemain2'
                    elif Ta=='TA' and Ta0!='TA':
                        D1[str(a)+c],D1[str(a0)+c0]='Remain3','Similar3'
                    elif Ta!='TA' and Ta0=='TA':
                        D1[str(a0)+c0],D1[str(a)+c]='Remain3','Similar3'
                    else:
                        if a==a0+1:
                            if e>e0:
                                D1[str(a)+c],D1[str(a0)+c0]='Remian4','Similar4'
                            elif e<e0:
                                D1[str(a0)+c0],D1[str(a)+c]='Remain4','Similar4'
                            else:
                                if len(b) > len(b0):
                                    D1[str(a)+c],D1[str(a0)+c0]='Remain5','Similar5'
                                else:
                                    D1[str(a)+c],D1[str(a0)+c0]='Similar5','Remain5'
                        else:
                            if e>e0:
                                D1[str(a)+c],D1[str(a0)+c0]='possibility1','possibility2'
                            else:
                                D1[str(a0)+c0],D1[str(a)+c]='possibility1','possibility2'
                else:
                    if a != a0:
                        D1[str(a)+c] = 'Unique_read'
                    else:
                        if Ta=='TA' and Ta0!='TA':
                            D1[str(a)+c],D1[str(a0)+c0]='Remain6','Similar6'
                        elif Ta!='TA' and Ta0=='TA':
                            D1[str(a0)+c0],D1[str(a)+c]='Remain6','Similar6'
                        elif Ta=='TA' and Ta0=='TA':
                            if e>e0:
                                D1[str(a)+c],D1[str(a0)+c0]='Remain6','Similar7'
                            elif e<e0:
                                D1[str(a)+c],D1[str(a0)+c0]='Similar7','Remain7'
                            else:
                                if len(b) > len(b0):
                                    D1[str(a)+c],D1[str(a0)+c0]='Remain8','Similar8'
                                else:
                                    D1[str(a0)+c0],D1[str(a)+c]='Remain8','Similar8'
            a0,c0,e0,Ta0 = a,c,e,Ta
        df_mark = pd.DataFrame(pd.Series(D1,index=D1.keys())) ##converting dict to DataFrame
        df_mark['site_amdt'] = df_mark.index.str[:-1].astype(np.int64)  ##converting str to int
        df_mark['insert_direct'] = df_mark.index.str[-1]
        df_chro = df_chro.merge(df_mark,on=['site_amdt','insert_direct'],how='outer')
        df_chro['chro'] = chro
        #remove the duplication caused by sequencing error
        df_chro_dere2 = df_chro[df_chro[0].str[:-1]!='Similar']
        df_chro_dere3 = df_chro_dere2.copy()
        #remove the insertion direction duplication
        #df_chro_dere3.ix[df_chro_dere3.insert_direct=='-','site_amdt'] = df_chro_dere3['site_amdt'] -1
        df_chro_dere3.site_amdt[df_chro_dere3.insert_direct=='-'] -= 1
        df_chro_dere3 = df_chro_dere3.drop_duplicates(subset=['chro','site_amdt'])
        df_chro_dere2.to_csv("%s/%s_%s_insertions.xls"%(tag,tag,chro),sep='\t',index=False,\
        header=['chromosome','insertions','insert_direct','read','count1','count2','mark'])
        df_chro_dere3.to_csv("%s/%s_%s_insertions2.xls"%(tag,tag,chro),sep='\t',index=False,\
        header=['chromosome','insertions','insert_direct','read','count1','count2','mark']) 
        return df_chro,df_chro_dere2,df_chro_dere3
    all_insertions0,all_insertions1,all_insertions2 = 0,0,0
    for index,(chro,chro_ac) in enumerate(manifest_data['chr_accession'].items()):
        dereplicate = dereplicate2(chro_ac,chro,transposon)
        all_insertions0 += len(dereplicate[0])
        all_insertions1 += len(dereplicate[1])
        all_insertions2 += len(dereplicate[2])
        print('%s_dereplicate1: %d\t\t%s_dereplicate2: %d'%(chro,len(dereplicate[0]),chro,len(dereplicate[1])))
        #combine all chromosome data
        if not index:
            df_all0 = dereplicate[0]
            df_all1 = dereplicate[1]
            df_all2 = dereplicate[2]
        else:
            df_all0 = df_all0.append(dereplicate[0])
            df_all1 = df_all1.append(dereplicate[1])
            df_all2 = df_all2.append(dereplicate[2])
    print('# Independent insertions in genome is %d considering insert direction before the second dereplication.'%all_insertions0)
    print('# Independent insertions in genome is %d considering insert direction after the second dereplication.'%all_insertions1)
    print('# Independent insertions in genome is %d if ignoring insert direction.'%all_insertions2)
    df_all0.to_csv("%s/%s_all_insertions0.xls"%(tag,tag),sep='\t',index=False,\
    header=['chromosome','insertions','insert_direct','read','count1','count2','mark'])
    df_all1.to_csv("%s/%s_all_insertions.xls"%(tag,tag),sep='\t',index=False,\
    header=['chromosome','insertions','insert_direct','read','count1','count2','mark'])
    df_all2.to_csv("%s/%s_all_insertions2.xls"%(tag,tag),sep='\t',index=False,\
    header=['chromosome','insertions','insert_direct','read','count1','count2','mark'])

#locating the insertion sites to chromosomes of Pp 
def site_annot(tag,chro):
    f_ins = open('%s/%s_%s_insertions.xls'%(tag,tag,chro))
    #f_IGS = open('%s/%s_%s_IGS.xls'%(tag,tag,chro),'w')
    f_gene = open('%s/%s_%s_gene.xls'%(tag,tag,chro),'w')
    f_intron = open('%s/%s_%s_intron.xls'%(tag,tag,chro),'w')
    df_gene = pd.read_table('1.material_prep/%s_annot_gene.xls'%chro)
    fin_intron = open('1.material_prep/%s_annot_intron.xls'%chro)
    arr_gene = df_gene.values
    arr_gene_str = df_gene.astype('string').values  #coverting int to str
    gene_lastsite = max(arr_gene[-1][2:3])
    #f_IGS.write('\t'.join(df_gene.columns[:5])+'\tinsert_site\trate\n')
    f_gene.write('\t'.join(df_gene.columns[:5])+'\tinsert_site\tinsert_direct\treads\tgene_annotation\n')
    List_IGS = [];List_gene = []
    for i in islice(f_ins,1,None):
        i = i.split()
        insert_site = int(i[1])
        if insert_site <= gene_lastsite:
            for index,j in enumerate(arr_gene):
                if j[1] == '+':
                    if j[2] > insert_site:
                        List_IGS.append(insert_site)
                        break
                    elif j[3] >= insert_site:
                        List_gene.append(insert_site)
                        f_gene.write('\t'.join(arr_gene_str[index][:5])+'\t%s\t%s\t%s\t%s\n'%(i[1],i[2],i[5],j[5]))
                        break
                else:
                    if j[3] > insert_site:
                        List_IGS.append(insert_site)
                        break
                    elif j[2] >= insert_site:
                        List_gene.append(insert_site)
                        f_gene.write('\t'.join(arr_gene_str[index][:5])+'\t%s\t%s\t%s\t%s\n'%(i[1],i[2],i[5],j[5]))
                        break
        else:
            List_IGS.append(insert_site)
    List_IGS_rate = []
    for j in arr_gene:  #IGS insertion distribution
        for insert_site in List_IGS:
            ## this method will miss few igs site
            if j[1] == '+':
                prom_rate = (insert_site-j[2])/1000.0
                term_rate = (insert_site-j[3])/1000.0
                if prom_rate < -10: continue
                if term_rate > 10: break
            else:
                prom_rate = (insert_site-j[2])/-1000.0
                term_rate = (insert_site-j[3])/-1000.0
                if term_rate > 10: continue
                if prom_rate < -10: break
            rate = prom_rate if prom_rate<=0 else term_rate
            List_IGS_rate.append([j[0],j[1],j[2],j[3],j[4],insert_site,rate])
    df_igs = pd.DataFrame(List_IGS_rate,columns=list(df_gene.columns[:5])+['insert_site','rate'])
    df_igs['rate_abs'] = df_igs['rate'].abs() #np.where(df_igs['rate']>0,df_igs['rate'],-df_igs['rate'])
    gb_igs = df_igs.groupby('insert_site',group_keys=False).apply(lambda x: x.sort_values(by=['rate_abs'])[:1]) ##if [0] repalce [:1],it will doesnt work
    del gb_igs['rate_abs']
    gb_igs.to_csv('%s/%s_%s_IGS.xls'%(tag,tag,chro),sep='\t',index=False)
    #debug code: List_gene.append(634910);List_gene.sort()
    f_intron.write('gene_id\tstrand\tgene_start\tgene_end\tinsert_site\twhichintron\tintron\n')
    intron_count = 0
    for k in islice(fin_intron,1,None):  #intron insertion distribution
        k = k.rstrip().split('\t')  #rstrip is 
        k2 = map(int,k[4:])
        if len(k2) == 2:
            (ismin,ismax) = (k2[0],k2[1]) if k[1] == '+' else (k2[1],k2[0])
            for insert_site in List_gene:
                if insert_site <= ismin: continue
                if insert_site <= ismax:
                    intron_count += 1
                    print(k[0],k[1],k[2],k[3],insert_site,1,k[4],k[5],sep='\t',file=f_intron)
                else: break
        else:
            LT_intron = zip(*([iter(k2)]*2))
            (ismin,ismax) = (k2[0],k2[-1]) if k[1] == '+' else (k2[-1],k2[0])
            for insert_site in List_gene:
                if insert_site <= ismin: continue
                if insert_site <= ismax:
                    if k[1] == '+':
                        Li = map(lambda x:x[0]<insert_site and x[1]>=insert_site,LT_intron)
                    else:
                        Li = map(lambda x:x[1]<insert_site and x[0]>=insert_site,LT_intron)
                    try:
                        intron_count += 1
                        print('\t'.join(k[:4]),insert_site,Li.index(True)+1,'\t'.join(k[4:]),sep='\t',file=f_intron)
                    except: pass
                else: break
    f_ins.close();f_gene.close();f_intron.close()
    return len(List_gene),len(List_IGS),intron_count




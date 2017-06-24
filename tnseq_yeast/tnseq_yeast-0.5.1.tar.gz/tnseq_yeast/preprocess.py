#!usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import re
import parseTnseqRawdata as ptr

# all function list:
all_function = {'c':'cutadapt(filename,transposon,manifest_data,tag,core_num,select,Lmax,ut)'\
,'b':'bowtie(tag,core_num)','u':'unique(transposon,tag,manifest_data)','s':'site_annot(tag,manifest_data)',\
'w':'weblogo(filename)','i':'gene_insert(filename)','m':'mapES(filename)'}

filename_cr = ''

def cutadapt(filename,transposon,manifest_data,tag,core_num,select,Lmax,ut):
    if not os.path.exists('3.Cutadapt_trimmed'): os.system('mkdir 3.Cutadapt_trimmed')
    # cutadapt program will not run if tag+'_t_l' file already exists
    if filename[-3:] == '.gz':
        os.system('pigz -p %s -d 2.Tndata_raw/%s'%(core_num,filename))
        filename = filename[:-3]
    ptr.cutadapt(filename,transposon,manifest_data,tag,core_num,select,Lmax,ut)

def bowtie(tag,core_num):
    if not os.path.exists('4.Bowtie_data_dir'):os.system('mkdir 4.Bowtie_data_dir')
    ptr.bowtie(tag,core_num)

def unique(transposon,tag,manifest_data):
    ptr.unique('4.Bowtie_data_dir/%s_bowtie.txt'%tag,tag,transposon,manifest_data)

def site_annot(tag,manifest_data):
    num_gene,num_IGS,num_intron = 0,0,0
    for chro in manifest_data['chr_accession']:
        a,b,c = ptr.site_annot(tag,chro)
        num_gene += a
        num_IGS += b
        num_intron += c
    print("# The number of insertions in genes is %s"%num_gene)
    print("# The number of insertions in IGSs is %s"%num_IGS)
    print("# The number of insertions in introns is %s"%num_intron)
    os.system("""cat %s/%s_chr*_gene.xls | awk -F"\t" '{if(NR==1 || $1!~/gene_id/) print}' > %s/%s_all_gene.xls"""%(tag,tag,tag,tag))
    os.system("""cat %s/%s_chr*_IGS.xls | awk -F"\t" '{if(NR==1 || $1!~/gene_id/) print}' > %s/%s_all_IGS.xls"""%(tag,tag,tag,tag))
    os.system("""cat %s/%s_chr*_intron.xls | awk -F"\t" '{if(NR==1 || $1!~/gene_id/) print}' > %s/%s_all_intron.xls"""%(tag,tag,tag,tag))


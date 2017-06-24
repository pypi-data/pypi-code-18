# -*- coding: utf-8 -*-
#libreadcounts1_vs_libreadcounts2
#warning:输入的库文件名filename的开头必须是转座子名称的第一个字母且大写！！

"""
模块功能说明：
1. Readcounts_diff = (Readcounts1 – Readcounts2)/Max(Readcounts1,Readcounts2)
2. 我们定义，两个library的测序reads数差异程度用参数Readcounts_diff表示；
3. 本脚本的作用是比较两个library的测序reads数差异。如某位点仅在lib1中有reads，则Readcounts_diff = 1;
反之,如某位点仅在lib2中有reads,则Readcounts_diff = -1;两个lib都测出reads时-1< Readcounts_diff <1
4. 将两个lib测出的所有sites按染色体位点从小到大进行排序，以排序的序号为横坐标，Readcounts_diff为纵坐标，
绘制散点图(位点插入reads数测序差异图)
5. 位点插入reads数测序差异图可反映两个库的重叠性，进而可在一定程度上判断库的饱和性，转座子随机性和互补性
"""

from __future__ import print_function
import re
import os,sys
import commands
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import parseTnseqRawdata as ptr

##列出所有函数
all_function={'l':'libreadcounts1_vs_libreadcounts2(filename1,filename2)','p':'libs_plus(tag,dirnamelist,comb_type)','v':'vslibreads(dirnamelist,manifest_data)'}

def libs_plus(tag,dirnamelist,comb_type):
    if not os.path.exists(tag): os.mkdir(tag)
    allnames = ''
    TYPE_D = {'all':'insertions','gene':'gene','cds':'gene','igs':'IGS','IGS':'IGS'}
    print("\n# Starting merging following files:")
    for dirname in dirnamelist:
        dirname = dirname.strip('/')
        filename = dirname + '/' + dirname + '_all_%s.xls'%TYPE_D[comb_type]
        length =int(commands.getstatusoutput('cat %s | wc -l'%filename)[1]) - 1
        allnames = allnames + ' ' + filename
        print(">> %s\t\tUnique reads: %d"%(filename,length))
    file_combine = '%s/%s_%s_append.xls'%(tag,tag,TYPE_D[comb_type])
    os.system("""cat %s | awk -F"\t" '{if(NR==1 || ($1!~/chromosome/ && $1!~/gene_id/)) print}' > %s"""\
    %(allnames,file_combine))
    df1 = pd.read_table(file_combine)
    tag_uniq = ['chromosome','insertions'] if TYPE_D[comb_type]=='insertions' else ['gene_id','insert_site']
    df1.sort_values(by=tag_uniq)
    #df1['Total'] = df1.groupby(tag_uniq)['count2'].transform('sum')
    sys.exit(df1.head(100))
    df2 = df1.drop_duplicates(subset=tag_uniq)
    print("# Unique reads of merged file: %d\n"%len(df2))
    df2.to_csv('%s/%s_all_%s.xls'%(tag,tag,TYPE_D[comb_type]),sep='\t',index=False)


def libreadcounts1_vs_libreadcounts2(filename1,filename2):
    #判断lib-filename是否合法
    if (filename1[0] not in 'TS') and (filename2[0] not in 'TS'):
        print("Usage:filename's first letter must be 'S' or 'T'!")   
    pwd=os.getcwd() 

    #以符号'_'或'.'为分隔符，注意点号需要转义
    tag1=re.split("_|\.",filename1)[0]
    tag2=re.split("_|\.",filename2)[0]
    
    #使用pandas.read_table打开两个要vs(pk)的两个文件
    df1=pd.read_table('%s/%s'%(pwd,filename1),names=['chr','insertions','orientation','read','count1','count2','rep'])
    df2=pd.read_table('%s/%s'%(pwd,filename2),names=['chr','insertions','orientation','read','count1','count2','rep'])

    #合并两个数据框，同时具有去重复的作用，'outer'表示为并集
    df_merge=pd.merge(df1,df2,on=['chr','insertions'],how='outer')
    df_merge=df_merge.sort_values(by=['chr','insertions'])                
    
    #指定在一些列中将缺失值填充０,生成四条染色体文件
    df_merge=df_merge.fillna({'count1_x':0,'count2_x':0,'count1_y':0,'count2_y':0})
    df_merge=df_merge.fillna('NULL')
    
    #计算readcounts差异，生成汇总文件
    df_merge['readcounts_diff']=np.where(df_merge['count2_x']-df_merge['count2_y']>=0,(df_merge['count2_x']-df_merge['count2_y'])/df_merge['count2_x'],\
    (df_merge['count2_x']-df_merge['count2_y'])/df_merge['count2_y'])
    df_merge=df_merge.iloc[:,[0,1,4,5,9,10,12,3,8,6,11,2,7]]
    df_merge.to_csv('%s/%s_%s_all_insertions.xls'%(pwd,tag1,tag2),sep='\t',header=True,index=False)
    
    #统计，筛选，报告文件生成
    #统计行数,也可以用df1.shape[0]和df1.shape[1]
    df1_rownum=len(df1.index) 
    df2_rownum=df2.shape[0]
    df_merge_rownum=df_merge.shape[0]
    #统计unique_reads
    tag1_muniq=df_merge[df_merge['seq_y']=='NULL']['seq_y'].value_counts()
    tag2_muniq=df_merge[df_merge[u'seq_x']=='NULL']['seq_x'].value_counts()
    
    #报告文件生成
    f=open("%s/%s_%s_report.xls"%(pwd,tag1,tag2),'w')
    print("%s_reads\t%d"%(tag1,df1_rownum),"%s_reads\t%d"%(tag2,df2_rownum),\
    "merge_reads\t%d"%df_merge_rownum,"%s_muniq\t%d"%(tag1,tag1_muniq),\
    "%s_muniq\t%d"%(tag2,tag2_muniq),sep='\n',file=f)
    f.close()
    
    #绘制散点图
    plt.plot(df_merge['readcounts_diff'],'|',fillstyle='none',markersize=5,color='#00aa00') 
    plt.ylim(-1.03,1.03)
    plt.xlabel('unique_read')
    plt.ylabel('readcounts_diff')
    plt.title('%s_reads vs %s_reads'%(tag1,tag2))
    plt.savefig('%s/%s_reads vs %s_reads.pdf'%(pwd,tag1,tag2),dpi=1080*720)


def vslibreads(dirnamelist,manifest_data):
    TD = {'T':'TcB','S':'SB','P':'PB'}
    dirname1 = dirnamelist[0]
    dirname2 = dirnamelist[1]
    if (dirname1[0] not in 'TSP') and (dirname2[0] not in 'TSP'):
        print("Usage:dirname's first letter must be 'S' or 'T' or 'P'!")
    tag1=dirname1.split("/")[0]
    tag2=dirname2.split("/")[0]
    if not os.path.exists('10.VSlibreads'):os.mkdir('10.VSlibreads')
    output1 = commands.getstatusoutput('cat 4.Bowtie_data_dir/%s_bowtie.txt | wc -l'%tag1)
    output2 = commands.getstatusoutput('cat 4.Bowtie_data_dir/%s_bowtie.txt | wc -l'%tag2)
    line1 = int(output1[1])
    line2 = int(output2[1])
    if line2 > line1:
        tag1,tag2 = tag2,tag1
        line1,line2 = line2,line1
    alldp1 = '%s_vs_%s/%s_vs_%s_all_insertions.xls'%(tag1,tag2,tag1,tag2)
    alldp2 = '%s/%s_all_insertions.xls'%(tag2,tag2)
    bowtie_newfile = '4.Bowtie_data_dir/%s_vs_%s_bowtie.txt'%(tag1,tag2)
    transposon1 = TD[tag1[0]] if tag1[1]!='L' else TD[tag1[0]]+'L'
    if not os.path.exists(alldp1):
        if not os.path.exists(bowtie_newfile):
            df = pd.read_table('4.Bowtie_data_dir/%s_bowtie.txt'%tag1,header=None)
            df_new = df.sample(n=line2)
            df_new.to_csv(bowtie_newfile,sep='\t',index=False,header=None)
        ptr.unique(bowtie_newfile,tag1+'_vs_'+tag2,transposon1,manifest_data)
    df1 = pd.read_table(alldp1,usecols=[0,1,2,3,5])
    df2 = pd.read_table(alldp2,usecols=[0,1,2,3,5])
    df_merge = pd.merge(df1,df2,on=['chromosome','insertions','insert_direct'],how='outer')
    df_merge_mod = df_merge.fillna(0)
    tag_new = re.split('/|\.',alldp1)[1]
    df_merge_mod.iloc[:,[0,1,2,3,5,4,6]].to_csv('10.VSlibreads/%s_vslibreads.xls'%tag_new,sep='\t',index=False)
    #draw fig
    ##plt.plot(df_merge_mod['reads_x'],df_merge_mod['reads_y'],'b.')
    ##plt.savefig('vslibreads/%s_vslibreads.pdf'%re.split('/|\.',alldp1)[1])

    file_Rscript = '10.VSlibreads/%s_vslibreads.r'%tag_new
    f = open(file_Rscript,'w')
    Rscript = """library('ggplot2')
dt <- read.table('10.VSlibreads/%s_vslibreads.xls',header = TRUE)
pdf('10.VSlibreads/%s_vslibreads.pdf')
p <- ggplot(dt,aes(count2_x,count2_y))
p + geom_point(aes(colour = factor(chromosome)),size=0.5) \
+scale_x_sqrt() + scale_y_sqrt() \
+ ggtitle("Reads compare of %s and %s")+theme(plot.title=element_text(size = rel(1),colour = "#CD7F32"))  + xlim(0,500)+ ylim(0,500)
dev.off() 
"""%(tag_new,tag_new,tag1,tag2) ##,colour = chro+geom_smooth(aes(x=reads_x,y=reads_y),method='lm')
    print(Rscript,file=f)
    f.close()
    os.system('R2 CMD BATCH %s'%file_Rscript)
"""pdf('10.VSlibreads/%s_vslibreads-2.pdf')
p <- ggplot(dt,aes(reads_x,reads_y))
p + geom_point(aes(colour = factor(chro)),size=0.5) + xlim(0,500) + ylim(0,500)
dev.off()"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:Please input filenames of library1 and library2")
    elif len(sys.argv) == 2:
        filename1=sys.argv[1]
        filename2=sys.argv[2]
        libreadcounts1_vs_libreadcounts2(filename1,filename2)
        
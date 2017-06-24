

from __future__ import print_function
import os
import sys
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyfaidx import Fasta

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from matplotlib.colors import ListedColormap
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from scanGenomeInsertions import Reads_normalization

all_function = {'d':'Gene_integration_densities(tag, norm).data_process(all_insert, reads_limit, TAcounts, estype)',
                'm':'Machine_learning(tag, norm).prep_data(manifest_data, learnobj)'}


class Gene_integration_densities(Reads_normalization):
    def __init__(self, tag, norm):
        self.tag = tag
        self.norm = norm
        

    # 2016.11.21 modify
    def __process(self, all_insert, reads_limit, TAcounts, estype):
        # ORF integration densities
        if self.norm: # Normalization
            fGene = '%s/%s_all_gene_norm.xls'%(self.tag,self.tag)
            reads = 'reads_norm'
            ntag = '_norm'
            if not os.path.exists(fGene):
                self.normalization(gene=True)
        else: # Without normalization
            fGene = '%s/%s_all_gene.xls'%(self.tag,self.tag)
            reads = 'reads'
            ntag = ''

        # Define filename of gene integration densities data
        geneidd_detail = '%s/%s_geneidd_detail%s.xls'%(self.tag, self.tag, ntag)
        geneidd = '%s/%s_geneidd_%s%s.xls'%(self.tag, self.tag, estype, ntag)
        df = pd.read_table(fGene,
             usecols=['gene_id', 'gene_start', 'gene_length', 'insert_site', reads])
        df_annot = pd.read_table('1.Material_prep/annot_gene2.xls',
                   usecols=['gene_id', 'gene_start', 'gene_length', 'TAcounts']) 
        # limit sequencing reads of gene insertions
        df = df[df[reads] > reads_limit]
        df['ratio_length'] = abs(df['insert_site']-df['gene_start'])/df['gene_length']
        # remove some seq near 3' terminator, default is 10%
        retain_size = 0.1
        df_remove = df[df['ratio_length']<= retain_size]
        del df_remove["gene_length"]
        grouped = df_remove.loc[:, ['gene_id', 'ratio_length']].groupby('gene_id', as_index=False)
        df_hits = df_remove.merge(grouped.count(), on='gene_id', how='left')
        df_hits_ave = df_hits.merge(grouped.mean(), on='gene_id', how='left')
        df_final = df_hits_ave.merge(df_annot, on=['gene_id', 'gene_start'], how='outer')
        # Get the number of all insertion sites
        try:
            Summary = yaml.load('%s/%s_summary.yaml'%(self.tag, self.tag))
            all_insert = Summary['all_insertions1']
        except:
            try:
                all_insert = sum(1 for line in open('%s/%s_all_insertions.xls'%(self.tag, self.tag)))
            except:
                sys.exit('Make sure that %s/%s_summary.yaml or %s/%s_all_insertions.xls exist'
                         %(self.tag, self.tag, self.tag, self.tag))

        if TAcounts:  # TAcounts of 90% 3'near gene is 71.882
            df_final['insert_freq'] = 1000000*72*df_final['ratio_length_y']/(all_insert*df_final['TAcounts'])
        else:
            df_final['insert_freq'] = 1000000*1442.7*df_final['ratio_length_y']/(all_insert*df_final['gene_length'])

        df_final = df_final.fillna(0)
        """df_insertcounts = pd.DataFrame(df_edition1[df_edition1['ratio_length'] < 0.9].groupby(['gene_id'], as_index=False).size())
        df_insert_TA_counts = pd.merge(df_TAcounts, df_insertcounts, left_on=['chr', 'gene_id'], right_index=['chr', 'gene_id'], how='left')
        df_insert_TA_counts = df_insert_TA_counts.fillna(0)
        df_insert_TA_counts.to_csv('7.Essential_analysis/%s_insertvsTAcounts.xls'%tag, sep='\t',
                                    index=False, header=['chr', 'gene_id', 'TAcounts', 'insertcounts'])
        """
        # output gene insertion density distribution information
        df_final.to_csv(geneidd_detail, sep='\t', index=False, header=['gene_id', 'gene_start', 'insert_site',
        reads, 'ratio_length', 'hits_num', 'ratio_length_ave', 'gene_length', 'TAcounts', 'gene_annotion', 'insert_freq'])

        # map Sc or Sp essential gene tag to geneidd data
        df_estag = pd.read_table("1.Material_prep/%s_estype.txt"%estype)
        df_new = df_final.loc[:, ['gene_id', 'insert_freq', reads, 'TAcounts', 'gene_annotation']]
        df_new = df_new.groupby(['gene_id', 'insert_freq', 'TAcounts', 'gene_annotation'], as_index=False).sum()
        df_new["ratio_reads"] = df_new[reads] / df_new["TAcounts"]
        df_estag_map = df_new.merge(df_estag, on='gene_id', how='left')
        # df_estag_map = df_estag_map.drop_duplicates()
        df_estag_map = df_estag_map.fillna('NE')
        df_estag_map['tag'] = np.where(df_estag_map['mapES'].str.contains('ES'), 'Essential', 'Non-essential')
        df_estag_map.to_csv(geneidd, sep='\t', index=False)
        self.esidd_draw_with_R(geneidd_detail, geneidd)

    # Draw figure of gene_idd
    def esidd_draw_with_R(self, geneidd_detail, geneidd):
        f = open('%s/%s_esidd.R'%(self.tag, self.tag), 'w')
        Rscript="""library("ggplot2")
        dt <- read.csv(%s, sep='\t', header=T)
        pdf("%s/%s_geneidd_%s.pdf")
        ggplot(dt, aes(insert_freq, ..count..)) + geom_density(aes(colour=tag), adjust = 1/5) \
        + scale_x_continuous(breaks=seq(0, 300, 50)) + ggtitle("%s integration densities of ORFs\
          homology to %s essential ORFs ")+theme(plot.title=element_text(size=rel(0.8), \
         colour="#CD7F32")) + xlim(0, 400) 
        dev.off()"""%(self.geneidd, self.tag, self.tag, estype, self.tag, estype)
        print(Rscript, file=f)
        f.close()
        os.system('R CMD BATCH %s/%s_esidd.R'%(self.tag, self.tag))


class Machine_learning(Gene_integration_densities):
    """
    Build logistic regression model by machine-learning
    """
    def prep_data(self, manifest_data, learnobj):
        self.test();sys.exit()
        def provide_gaps():
            if not os.path.exists('%s/%s_gene_gaps2.xls'%(self.tag, self.tag)):
                df_gaps = pd.read_table('%s/%s_gene_gaps.xls'%(self.tag, self.tag))
                del df_gaps['seqNo']
                df_gaps_max = df_gaps.groupby('gene_id',as_index=False).apply(lambda x: x.sort_values(by='gaps')[-1:])
                df_gaps_max.to_csv('%s/%s_gene_gaps2.xls'%(self.tag, self.tag), sep="\t", index=False)
            else:
                df_gaps_max = pd.read_table('%s/%s_gene_gaps2.xls'%(self.tag, self.tag))
            return df_gaps_max

        
        tag_lobj = learnobj.split('/')[-1].split('.')[0]
        if norm:
            geneidd_norm = '%s/%s_geneidd_detail_norm.xls'%(self.tag, self.tag)
            if not os.path.exists(geneidd_norm):
                df_norm = pd.read_table('%s/%s_all_insertions_norm.xls'%(self.tag, self.tag),
                          usecols = ['chromosome', 'insertions', 'reads_norm'])
                # map reads_norm to gene file
                for index, chro in enumerate(manifest_data['chr_accession']):
                    df_norm_chro = df_norm[df_norm['chromosome']==chro]
                    df_gene = pd.read_table('%s/%s_%s_gene.xls'%(self.tag, self.tag, chro),
                              usecols = ['gene_id','insert_site'])
                    df_merge1 = pd.merge(df_norm_chro, df_gene, left_on=['insertions'], right_on=['insert_site'], how='right')
                    if not index:
                        df_gene_norm = df_merge1
                    else:
                        df_gene_norm = df_gene_norm.append(df_merge1)
                df_geneidd = pd.read_table(self.geneidd_detail)
                df_merge2 = pd.merge(df_geneidd, df_gene_norm, on=['gene_id','insert_site'],how='left')
                df_merge2 = df_merge2.fillna(0) #;sys.exit(df_merge2);
                df_merge2.to_csv(geneidd_norm, sep="\t", index=False)
            
            df_norm = pd.read_table(geneidd_norm)
            df_norm = df_norm.loc[:,['gene_id','insert_freq','TAcounts','gene_annotion','reads_norm']]
            df_subject =  df_norm.groupby(['gene_id','insert_freq','TAcounts','gene_annotion'], as_index=False).sum()
            df_subject[reads] = df_subject['reads_norm'] / df_subject['TAcounts']
                
        else:
            df = pd.read_table(self.geneidd_detail)
            df = df.loc[:,['gene_id','insert_freq','TAcounts','gene_annotion',reads]]
            df_subject =  df.groupby(['gene_id','insert_freq','TAcounts','gene_annotion'], as_index=False).sum()
            df_subject[reads] = df_subject[reads] / df_subject['TAcounts']

        df_gaps = provide_gaps()
        df_subject = pd.merge(df_subject, df_gaps,on='gene_id',how='left')
        df_subject = df_subject.fillna(1500) #;sys.exit(df_subject)
        df_learnobj = pd.read_table(learnobj)
        # df_merge used for machine learning
        # Choose parameter
        parameter = ['insert_freq',reads, 'gaps']
        df_merge = pd.merge(df_subject.loc[:, ['gene_id']+parameter], df_learnobj, on="gene_id", how="right")
        # df_merge.to_csv("%s/%s_%s_prob0.xls"%(tag, tag, tag_lobj), sep="\t", index=False)
        X,  y = df_merge.loc[:, parameter].values, df_merge['Class_labels'].values
        X_train,  X_test,  y_train,  y_test = train_test_split(X,  y, test_size=0.3) #,  random_state=0)
        sc = StandardScaler()
        sc.fit(X_train)
        X_train_std = sc.transform(X_train)
        X_test_std = sc.transform(X_test)
        self.svm_model(X_train_std, X_test_std, y_train, y_test, tag_lobj, parameter)

    def logistic_model(self, X_train_std, X_test_std, y_train, y_test, tag_lobj, parameter):

        def sigmoid(Z):
            return 1 / (1 + np.exp(-Z))

        lr = LogisticRegression(C=50)#(C=1000.0,  random_state=0)
        lr.fit(X_train_std, y_train)
        y_pred = lr.predict(X_test_std)
        
        print('%s ref to %s data:'%(self.tag, tag_lobj))
        print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
        print('intercept: %s\tcoef: %s'%(lr.intercept_[0], lr.coef_[0]))

    def svm_model(self, X_train_std, X_test_std, y_train, y_test, tag_lobj, parameter):
        svm = SVC(C=50,gamma=0.1,kernel='linear') #,kernel='linear'
        svm.fit(X_train_std, y_train)
        y_pred = svm.predict(X_test_std)
        
        print('%s ref to %s data:'%(self.tag, tag_lobj))
        print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
        #print('intercept: %s\tcoef: %s'%(clf.intercept_[0], clf.coef_[0]))

        
        """
        subject_val = df_subject.loc[:, ['insert_freq',reads]].values
        subject_std = sc.fit_transform(subject_val)
        Z = lr.intercept_[0] + lr.coef_[0][0] * subject_std[:, 0] + lr.coef_[0][1] * subject_std[:, 1]
        df_subject["probability"] = sigmoid(Z)
        prob_file = "%s/%s_%s_probability.xls"%(self.tag, self.tag, tag_lobj)
        df_subject.to_csv(prob_file, sep="\t", index=False)"""
        self.plot_decision_regions(X_train_std, y_train, classifier=svm)
        plt.xlabel(parameter[0]+' [standardized]')
        plt.ylabel(parameter[1]+' [standardized]')
        plt.legend(loc='upper left')
        plt.savefig('%s/%s_%s_decision_regions.pdf'%(self.tag, self.tag, tag_lobj))
        plt.close()
        

    def plot_decision_regions(self, X,  y, classifier, resolution=0.02):
            markers = ('s', 'x', 'o', '^', 'v')
            colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
            cmap = ListedColormap(colors[:len(np.unique(y))])
            # plot the decision surface
            x1_min, x1_max = X[:,  0].min() - 1,  X[:,  0].max() + 1
            x2_min, x2_max = X[:,  1].min() - 1,  X[:,  1].max() + 1
            xx1, xx2 = np.meshgrid(np.arange(x1_min,  x1_max,  resolution), 
            np.arange(x2_min, x2_max, resolution))
            Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
            Z = Z.reshape(xx1.shape)
            plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
            plt.xlim(xx1.min(), xx1.max())
            plt.ylim(xx2.min(), xx2.max())
            # plot class samples
            for idx, cl in enumerate(np.unique(y)):
                plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], 
                alpha=0.8, c=cmap(idx), 
                marker=markers[idx], label=cl)


    """def escompare(self):
        tag_subj1 = self.subject.split('/')[0]
        tag_subj2 = self.subject2.split('/')[0]
        tag_lobj1 = self.learnobj1.split('/')[-1].split('.')[0]
        tag_lobj2 = self.learnobj2.split('/')[-1].split('.')[0]
        file1 = self.logistic_model(self.subject, self.learnobj1)
        file2 = self.logistic_model(self.subject, self.learnobj2)
        df1 = pd.read_table(file1)
        df2 = pd.read_table(file2)
        df_merge = pd.merge(df1, df2, on=['gene_id', 'TAcounts', 'gene_annotation'], how='outer')
        df_merge['escompare'] = df_merge['probability_x'] - df_merge['probability_y']
        df_merge_adj = df_merge.iloc[:, [0, 1, 7, 2, 8, 6, 10, 11, 3, 4, 5]]
        df_merge_adj.to_csv("%s/%s_%s-%s_%s_escompare.xls"%(tag_subj1, tag_subj1, tag_lobj1, \
        tag_subj2, tag_lobj2), sep="\t", index=False)"""

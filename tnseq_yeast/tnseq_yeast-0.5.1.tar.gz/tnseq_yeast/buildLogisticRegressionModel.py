
"""
machine-learning
"""

from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from matplotlib.colors import ListedColormap
from sklearn.metrics import accuracy_score

all_function = {'e':'esanalysis(subject1,subject2,learnobj1,learnobj2)'}


class esanalysis:
    def __init__(self,subject1,subject2,learnobj1,learnobj2):
        self.subject1 = subject1
        self.subject2 = subject2
        self.learnobj1 = learnobj1
        self.learnobj2 = learnobj2

        if self.subject2:
            if self.learnobj2:
                self.escompare()
            else:
                print("Please input learning-object2 pathway!")
        else:
            self.logistic_model(self.subject1,self.learnobj1)

        """self.tag_lobj = learnobj.split("/")[-1].split('.')[0]
        self.tag = subject[0].split("/")[0]
        if len(subject) == 1:
            print("Calculating probability of gene essentiality through logisticregression model \
            by machine-learning %s and %s data"%(self.tag,self.tag_lobj))
            self.logistic_model(subject[0])
        else:
            if len(subject) > 2:
                print("Warning: you provide more than two research samples, redundant samples will be ignored!")
            self.tag2 = subject[1].split("/")[0]
            self.escompare()"""

    def escompare(self):
        tag_subj1 = self.subject1.split('/')[0]
        tag_subj2 = self.subject2.split('/')[0]
        tag_lobj1 = self.learnobj1.split('/')[-1].split('.')[0]
        tag_lobj2 = self.learnobj2.split('/')[-1].split('.')[0]
        file1 = self.logistic_model(self.subject1,self.learnobj1)
        file2 = self.logistic_model(self.subject2,self.learnobj2)
        df1 = pd.read_table(file1)
        df2 = pd.read_table(file2)
        df_merge = pd.merge(df1,df2,on=['gene_id','TAcounts','gene_annotation'],how='outer')
        df_merge['escompare'] = df_merge['probability_x'] - df_merge['probability_y']
        df_merge_adj = df_merge.iloc[:,[0,1,7,2,8,6,10,11,3,4,5]]
        df_merge_adj.to_csv("%s/%s_%s-%s_%s_escompare.xls"%(tag_subj1,tag_subj1,tag_lobj1,\
        tag_subj2,tag_lobj2),sep="\t",index=False)


    def logistic_model(self,subject,learnobj):
        def plot_decision_regions(X, y, classifier, resolution=0.02):
            markers = ('s', 'x', 'o', '^', 'v')
            colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
            cmap = ListedColormap(colors[:len(np.unique(y))])
            # plot the decision surface
            x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
            x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
            xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
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

        def sigmoid(Z):
            return 1 / (1 + np.exp(-Z))

        """
        subject colname: gene_id    insert_freq    TAcounts    gene_annotation    reads    ratio_reads    mapES    tag
        """
        tag_subj = subject.split('/')[0]
        tag_lobj = learnobj.split('/')[-1].split('.')[0]
        df_subject = pd.read_table(subject) 
        sc = StandardScaler()


        df_learnobj = pd.read_table(learnobj)
        df_merge = pd.merge(df_subject.iloc[:,[0,1,5]],df_learnobj,on="gene_id",how="right")
        X, y = df_merge.iloc[:, [1,2]].values, df_merge.iloc[:, 3].values
        df_merge.to_csv("%s/%s_%s_prob0.xls"%(tag_subj,tag_subj,tag_lobj),sep="\t",index=False)
        X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3) #, random_state=0)
        
        """# train all sw_data
        X_std = sc.fit_transform(X)
        lr = LogisticRegression(C=100)
        lr.fit(X_std, y)
        """
        sc.fit(X_train)
        X_train_std = sc.transform(X_train)
        X_test_std = sc.transform(X_test)
        lr = LogisticRegression(C=100)#(C=1000.0, random_state=0)
        lr.fit(X_train_std, y_train)
        y_pred = lr.predict(X_test_std)
        
        print('%s ref to %s data:'%(tag_subj,tag_lobj))
        print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
        print('intercept: %s\tcoef: %s'%(lr.intercept_[0],lr.coef_[0]))
        Z = lr.intercept_[0] + lr.coef_[0][0] * subject_std[:,0] + lr.coef_[0][1] * subject_std[:,1]
        df_subject["probability"] = sigmoid(Z)
        prob_file = "%s/%s_%s_probability.xls"%(tag_subj,tag_subj,tag_lobj)
        df_subject.iloc[:,[0,1,5,2,6,3,8]].to_csv(prob_file,sep="\t",index=False)
        plot_decision_regions(X_train_std,y_train, classifier=lr)
        plt.xlabel('insert_freq [standardized]')
        plt.ylabel('ratio_reads [standardized]')
        plt.legend(loc='upper left')
        plt.savefig('%s/%s_%s_decision_regions.pdf'%(tag_subj,tag_subj,tag_lobj))
        plt.close()
        return prob_file





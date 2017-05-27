#! -*- coding=utf-8 -*-

import numpy as np
import pandas as pd
import re
import math
import time
import itertools
from itertools import combinations
from numpy import array
from math import sqrt
from multiprocessing import Pool
from sklearn import metrics
import pylab as pl
from math import log,exp,sqrt


def get_max_ks(date_df, start, end, rate, factor_name, bad_name, good_name, total_name,total_all):
    ks = ''
    bad = date_df.loc[start:end,bad_name]
    good = date_df.loc[start:end,good_name]
    bad_good_cum = list(abs(np.cumsum(bad/sum(bad)) - np.cumsum(good/sum(good))))
    if bad_good_cum:
        max_ks = max(bad_good_cum)
        index_max = bad_good_cum.index(max_ks)
        t = start + index_max
        len1 = sum(date_df.loc[start:t,total_name])
        len2 = sum(date_df.loc[t+1:end,total_name])
        if len1 >= rate*total_all:
            if len2 >= rate*total_all:
                ks = t
    return ks


def ks_auto(date_df,piece,rate,factor_name,bad_name,good_name,total_name,total_all):
    t1 = 0
    t2 = len(date_df)-1
    num = len(date_df)
    if num > pow(2,piece-1):
        num = pow(2,piece-1)
    t_list = [t1,t2]
    tt =[]
    i = 1
    if len(date_df) > 1:
        t_list = cut_fun(t_list,date_df,'upper',rate,factor_name,bad_name,good_name,total_name,total_all)
        tt.append(t_list)
        for t_new in tt:
            if len(t_new) > 2:
                up_down = cut_while_fun(t_new,date_df,rate,factor_name,bad_name,good_name,total_name,total_all)
                t_up = up_down[0]
                if len(t_up) > 2:
                    t_list = list(set(t_list+t_up))
                    tt.append(t_up)
                t_down = up_down[1]
                if len(t_down) > 2:
                    t_list = list(set(t_list+t_down))
                    tt.append(t_down)
                i += 1
                if len(t_list)-1 > num:
                    break
                if i >= piece:
                    break
    if len(date_df) > 0:
        length1 = date_df.loc[0,total_name]
        if length1 >= rate*total_all:
            if 0 not in t_list:
                t_list.append(0)
        else:
            t_list.remove(0)
    t_list.sort()
    return t_list

def confusion_matrix(test,pred):
    cm=confusion_matrix(test,pred)
    return cm

def accuracy(test,pred_class):
    accu=metrics.accuracy_score(y_test, y_pred_class)
    return accu

def auc_score(y_true,y_score):
    auc_score=metrics.roc_auc_score(y_true, y_scores)
    return auc_score

def precison_recall_f1(confusion_matrix):
    P0 = float(confusion_matrix[0, 0]) / confusion_matrix[:, 0].sum()
    P1 = float(confusion_matrix[1, 1]) / confusion_matrix[:, 1].sum()
    R0 = float(confusion_matrix[0, 0]) / confusion_matrix[0, :].sum()
    R1 = float(confusion_matrix[1, 1]) / confusion_matrix[1, :].sum()
    print '0为正例时,准确率：%f,召回率：%f,F1:%f' % (P0, R0, 1 / (0.5 * (1 / P0 + 1 / R0)))
    print '1为正例时,准确率：%f,召回率：%f,F1:%f' % (P1, R1, 1 / (0.5 * (1 / P1 + 1 / R1)))
    

def f1_score(precision,recall):
    f1_score = 2 * precision * recall / (precision + recall)
    return f1_score

def plot_pr(auc_score, precision, recall, label=None):  
    pylab.figure(num=None, figsize=(6, 5))  
    pylab.xlim([0.0, 1.0])  
    pylab.ylim([0.0, 1.0])  
    pylab.xlabel('Recall')  
    pylab.ylabel('Precision')  
    pylab.title('P/R (AUC=%0.2f) / %s' % (auc_score, label))  
    pylab.fill_between(recall, precision, alpha=0.5)  
    pylab.grid(True, linestyle='-', color='0.75')  
    pylab.plot(recall, precision, lw=1)      
    pylab.show() 

def roc(data_path):
    db = [] #[score,nonclk,clk]
    pos, neg = 0, 0
    with open(data_path,'r') as fs:
        for line in fs:
            nonclk,clk,score = line.strip().split('\t')
            nonclk = int(nonclk)
            clk = int(clk)
            score = float(score)
            db.append([score,nonclk,clk])
            pos += clk
            neg += nonclk 
    db = sorted(db, key=lambda x:x[0], reverse=True)
    xy_arr = []
    tp, fp = 0., 0. 
    for i in range(len(db)):
        tp += db[i][2]
        fp += db[i][1]
        xy_arr.append([fp/neg,tp/pos])
    auc = 0. 
    prev_x = 0
    for x,y in xy_arr:
        if x != prev_x:
            auc += (x - prev_x) * y
            prev_x = x
    print "the auc is %s."%auc
    x = [_v[0] for _v in xy_arr]
    y = [_v[1] for _v in xy_arr]
    pl.title("ROC curve of %s (AUC = %.4f)" % ('svm',auc))
    pl.xlabel("False Positive Rate")
    pl.ylabel("True Positive Rate")
    pl.plot(x, y)
    pl.show()

#! -*- coding=utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
import math
import operator
import treePlotter

def cal_iv_012(data,dt):
    index,columns = data.shape 
    iv_name = []
    data = data.fillna(9999999)
    for i in range(int(columns)-1):
        name = data.ix[:,i:i+1].columns.values[0]
        print name
        num = data[[name,'label']][data[name] != 9999999].reset_index()
        df = num[name].value_counts().reset_index()
        if len(df) > 1:
            df['label'] = map(lambda x:1 if x/len(num) >= dt else 0,df[name])
            if df['label'].sum()<1:
                label_0 = num['label'][num['label'] == 0].count()
                label_1 = num['label'][num['label'] == 1].count()
                data_0 = num[(num[name] == 0)&(num[name] < 1) ][[name,'label']].reset_index()
                data_1 = num[(num[name] >= 1) &(num[name] < 2) ][[name,'label']].reset_index()
                data_2 = num[num[name] >=2 ][[name,'label']].reset_index()
                data_0_0,data_0_1 = count_label(data_0)
                data_1_0,data_1_1 = count_label(data_1)
                data_2_0,data_2_1 = count_label(data_2)
                print  data_0_0,data_0_1,data_1_0,data_1_1,data_2_0,data_2_1
                woe_0 =(0 if data_0_0*data_0_1 == 0 else math.log((data_0_0/label_0)/(data_0_1/label_1))*((data_0_0/label_0)-(data_0_1/label_1)))
                woe_1 =(0 if data_1_0*data_1_1 == 0 else math.log((data_1_0/label_0)/(data_1_1/label_1))*((data_1_0/label_0)-(data_1_1/label_1)))
                woe_2 =(0 if data_2_0*data_2_1 == 0 else math.log((data_2_0/label_0)/(data_2_1/label_1))*((data_2_0/label_0)-(data_2_1/label_1)))
                iv = woe_0+woe_1+woe_2
                iv_name.append([name,iv])
                print name,iv
    iv = pd.DataFrame(iv_name)
    iv.columns = ['name','iv']
    return iv


def cal_woe_012(data,col_name,dt):
    name=col_name
    woe=[]
    data = data.fillna(9999999)
    num = data[[name,'label']][data[name] != 9999999].reset_index()
    df = num[name].value_counts().reset_index()
    if len(df) > 1:
        df['label'] = map(lambda x:1 if x/len(num) >= dt else 0,df[name])
        if df['label'].sum()<1:
                label_0 = num['label'][num['label'] == 0].count()
                label_1 = num['label'][num['label'] == 1].count()
                data_0 = num[(num[name] == 0)&(num[name] < 1) ][[name,'label']].reset_index()
                data_1 = num[(num[name] >= 1) &(num[name] < 2) ][[name,'label']].reset_index()
                data_2 = num[num[name] >=2 ][[name,'label']].reset_index()
                data_0_0,data_0_1 = count_label(data_0)
                data_1_0,data_1_1 = count_label(data_1)
                data_2_0,data_2_1 = count_label(data_2)
                print  data_0_0,data_0_1,data_1_0,data_1_1,data_2_0,data_2_1
                woe_0 =(0 if data_0_0*data_0_1 == 0 else math.log((data_0_0/label_0)/(data_0_1/label_1))*((data_0_0/label_0)-(data_0_1/label_1)))
                woe_1 =(0 if data_1_0*data_1_1 == 0 else math.log((data_1_0/label_0)/(data_1_1/label_1))*((data_1_0/label_0)-(data_1_1/label_1)))
                woe_2 =(0 if data_2_0*data_2_1 == 0 else math.log((data_2_0/label_0)/(data_2_1/label_1))*((data_2_0/label_0)-(data_2_1/label_1)))
                woe.append(woe_0)
                woe.append(woe_1)
                woe.append(woe_2)
    return woe

def cal_woe_normal(data):
    #data.columns==['ID','n1','n0']
    N=data['n1']+data['n0']
    p1=data['n1']/N
    p0=data['n0']/N
    woe=math.log(p1/p0)
    result=pd.DataFrame([data['ID'],woe]).T
    return result

def cal_iv_normal(data):
    #data.columns==['ID','n1','n0']
    N=data['n1']+data['n0']
    p1=data['n1']/N
    p0=data['n0']/N
    woe=math.log(p1/p0)
    iv=woe*(p1-p0)
    sum_iv=sum(iv)
    return sum_iv

def corr(data):
    result = data.corr()
    return result

def corr(data,name):
    result=data.corr()[name]
    return result

#互信息
def mutual_info(class_df_list, term_set, term_class_df_mat):
    A = term_class_df_mat
    B = np.array([(sum(x) - x).tolist() for x in A])
    C = np.tile(class_df_list, (A.shape[0], 1)) - A
    N = sum(class_df_list)
    class_set_size = len(class_df_list)
    
    term_score_mat = np.log(((A+1.0)*N) / ((A+C) * (A+B+class_set_size)))
    term_score_max_list = [max(x) for x in term_score_mat]
    term_score_array = np.array(term_score_max_list)
    sorted_term_score_index = term_score_array.argsort()[: : -1]
    term_set_fs = [term_set[index] for index in sorted_term_score_index]
    
    return term_set_fs

#信息增益
def info_gain(class_df_list, term_set, term_class_df_mat):
    A = term_class_df_mat
    B = np.array([(sum(x) - x).tolist() for x in A])
    C = np.tile(class_df_list, (A.shape[0], 1)) - A
    N = sum(class_df_list)
    D = N - A - B - C
    term_df_array = np.sum(A, axis = 1)
    class_set_size = len(class_df_list)
    
    p_t = term_df_array / N
    p_not_t = 1 - p_t
    p_c_t_mat =  (A + 1) / (A + B + class_set_size)
    p_c_not_t_mat = (C+1) / (C + D + class_set_size)
    p_c_t = np.sum(p_c_t_mat  *  np.log(p_c_t_mat), axis =1)
    p_c_not_t = np.sum(p_c_not_t_mat *  np.log(p_c_not_t_mat), axis =1)
    
    term_score_array = p_t * p_c_t + p_not_t * p_c_not_t
    sorted_term_score_index = term_score_array.argsort()[: : -1]
    term_set_fs = [term_set[index] for index in sorted_term_score_index]    
    
    return term_set_fs

#卡方检验
def chi_square(obs,exp):
    result=stats.chisquare(obs,exp)
    return result

#Weighted Log Likelihood Ration 加权对数似然
def wllr(class_df_list, term_set, term_class_df_mat):
    A = term_class_df_mat
    B = np.array([(sum(x) - x).tolist() for x in A])
    C_Total = np.tile(class_df_list, (A.shape[0], 1))
    N = sum(class_df_list)
    C_Total_Not = N - C_Total
    term_set_size = len(term_set)
    
    p_t_c = (A + 1E-6) / (C_Total + 1E-6 * term_set_size)
    p_t_not_c = (B +  1E-6) / (C_Total_Not + 1E-6 * term_set_size)
    term_score_mat = p_t_c  * np.log(p_t_c / p_t_not_c)
    
    term_score_max_list = [max(x) for x in term_score_mat]
    term_score_array = np.array(term_score_max_list)
    sorted_term_score_index = term_score_array.argsort()[: : -1]
    term_set_fs = [term_set[index] for index in sorted_term_score_index]
    
    print term_set_fs[:10]
    return term_set_fs

#香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    bestGini = 999999.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        gini = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            subProb = len(splitDataSet(subDataSet, -1, 'N')) / float(len(subDataSet))
            gini += prob * (1.0 - pow(subProb, 2) - pow(1 - subProb, 2))
        if (gini < bestGini):
            bestGini = gini
            bestFeature = i
    return bestFeature

def count_label_01(data):
    label_0 = data['label'][data['label'] == 0].count()
    label_1 = data['label'][data['label'] == 1].count()
    return label_0,label_1









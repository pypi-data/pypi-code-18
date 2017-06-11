#coding:utf-8
'''
Created on 2017年6月10日

@author: jiang
'''
import random
from numpy import array,tile, zeros
import operator

def loadData(feature_num = 3,rows = 10):
    labels = ['A','B','C','D','E']
    groups = []
    reLabels = []
    for i in range(rows):
        line = [random.random() for j in range(feature_num)]
        groups.append(line)
        reLabels.append(random.choice(labels))
        
    return array(groups),reLabels

def norm(dataSet):
    minValues = dataSet.min(0)
    maxValues = dataSet.max(0)
    rangeValue = maxValues-minValues
    rows = dataSet.shape[0]
    normDataSet = dataSet - tile(minValues,(rows,1))
    normDataSet = normDataSet/tile(rangeValue, (rows,1))
    
    return normDataSet

def classify(inMatrix,trainData,labels,K=3):
    if not inMatrix == None and len(inMatrix[0])>0 and not isinstance(inMatrix[0][0],(int,float)):
        inMatrix = word2VectorMatrix(inMatrix)[0]
    
    rows = trainData.shape[0]
    predict = []
    for inX in inMatrix:
        diffMatrix = tile(inX, (rows,1)) - trainData
        double_diffMatrix = diffMatrix**2
        sqrtMatrix = double_diffMatrix.sum(axis = 1)
        distance = sqrtMatrix **0.5
        sorted_distance = distance.argsort()
        voteCount = {}
        for i in range(K):
            vote_label = labels[sorted_distance[i]]
            voteCount[vote_label] = voteCount.get(vote_label,0)+1
        sorted_vote = sorted(voteCount.iteritems(),key = operator.itemgetter(1),reverse = True)
        predict.append(sorted_vote[0][0])
    return predict

def word2VectorMatrix(inMatrix):
    vocabList = set([])
    for inX in inMatrix:
        vocabList = set(vocabList)|set(inX)
    vocabList = list(vocabList)
    vector = zeros((len(inMatrix),len(vocabList)))
    for inX in inMatrix:
        for word in inX:
            if word in vocabList:
                vector[inMatrix.index(inX)][vocabList.index(word)] += 1
    return vector,vocabList


if __name__=='__main__':
    dataMatrix,labels = loadData(feature_num = 4,rows = 10)
    normDataSet = norm(dataMatrix)
    print classify([[1,2,3,4],[2],[3]], dataMatrix, labels, K=3)
    print classify([['1','2','3','4'],['2'],['3']], dataMatrix, labels, K=3)
    vector,vocabList = word2VectorMatrix([['1','2','3','4'],['2'],['3']])
    print vector
    
    
    
    
    
    
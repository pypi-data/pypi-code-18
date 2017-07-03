# coding:utf-8
from keyword_zju.Function import *
import os

_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__), path))

DEFAULT_BLACK = _get_module_path("keywordBlackList.txt")

DEFAULT_IDF = _get_module_path("idf_5000.txt")


def ImporveTFIDF(text,keywordNum,weight,blackwordFile = DEFAULT_BLACK):
    
    #print text.encode("utf-8")
    segResult = SegText(text)
    TF_Value = GetWordPara(segResult).copy()
    IDF_Value = Load_IDFFromFile()
    
    stopWordList = LoadKeywordBlackList(blackwordFile)
    wordDict = {}
    for word in TF_Value.keys():
        if word in stopWordList: continue
        if word in IDF_Value.keys():
            wordDict[word] = TF_Value[word]*IDF_Value[word]
        else:
            wordDict[word] = TF_Value[word]*IDF_Value['DEFAULT']
    
    ## Get KeywordList
    resultList = ArrangeKeyword(wordDict,keywordNum,weight)
    return resultList

def Load_IDFFromFile(filename = DEFAULT_IDF):
    
    IDF_Value = {}
    openIDFfile = open(filename,"rb")
    readLines = openIDFfile.readlines()
    stopCode = chardet.detect(readLines[0])['encoding']
    
    for line in readLines:
        ustring = line.decode("utf-8")
        ustring = ustring.strip()
        sline = ustring.split(u" ")
        try:
            word,idf = sline
            IDF_Value[word] = float(idf)
        except:
            continue
    return IDF_Value
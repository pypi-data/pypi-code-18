# -*- coding: utf-8 -*-
"""
Created on Wed May 10 19:16:25 2017

这个模块的作用是对文档进行预处理，利用tfidf模型计算txt文档的相似性，
并在程序的目录下新建一个txt文档，将计算好的相似性导入txt文档中


"""

import gensim
import logging
import os
import jieba
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def create_address(path):
    '''获得txt文件夹内所有txt文件的绝对路径。
       输入是txt文件夹的绝对路径,
       返回所有txt文件的绝对路径列表'''
    address = []
    for file in os.listdir(path):
        if(os.name == 'nt'):
            abspath_txt = path + '\\' + file
        if(os.name == 'posix'):
            abspath_txt = path + '/' + file
        address.append(abspath_txt)
    return address
        
def save_documents(address):
    """"将每篇文档都转换为一个字符串并保存在列表中。
        输入是所有txt文件的绝对路径列表，
        返回文档内容列表，列表的每一项为每个文档的内容"""
    contents = []
    for each_path in address:
        with open(each_path,'r') as f:
            contents.append(f.read())
    return contents

#对文档内容进行处理（处理字符串与分词）    
def preprocess(contents):
    '''对文档进行预处理：删去无用的字符并对文档进行分词。
       参数为字符串形式的文档列表，
       输出为经过预处理的文档列表'''
    for i in range(len(contents)):
        #删去不必要的字符
        contents[i] = contents[i].replace('\t','')
        contents[i] = contents[i].replace('\r','')
        contents[i] = contents[i].replace('\n','')
        contents[i] = contents[i].replace(' ','')
        #documents[i] = documents[i].replace(',',' ')
        #documents[i] = documents[i].replace('.',' ')
        #documents[i] = re.sub('\[\d*\]', '', documents[i]) 
        #documents[i] = documents[i].lower()
    texts = []
    #创建停用词集合
    with open('stopWord.txt','r') as f:
        contents2 = f.read()
        word_list2 = contents2.split('\n')
        for i in range(len(word_list2)):
            word_list2[i] = word_list2[i].decode('gbk')
    

    for i in range(len(contents)):
        #分词
        word_list = filter(lambda x: len(x)>0,jieba.cut(contents[i],cut_all=False))
        #去除停用词
        for word in word_list:
            if word in word_list2:
                word_list.remove(word)
        texts.append(word_list)
    print len(texts)
    return texts


    


def tfidf_similarity(texts):
    '''利用文档创建tfidf模型与索引,
       计算文档间的两两相似度并生成一个txt文件，将结果导入其中。
       输入是文档列表,
       最后在程序的当前目录下生成一个txt文件'''
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    #利用这些语料，创建tfidf模型
    tfidf_model = gensim.models.TfidfModel(corpus)
    #计算每个文档的tfidf
    tfidfs = tfidf_model[corpus]
    #创建tfidf的索引
    num_features1 = len(dictionary.token2id)
    tfidf_index = gensim.similarities.SparseMatrixSimilarity(tfidfs,num_features=num_features1)
    similarities = []
    for i in range(len(texts)):
        content = texts[i]
        each_row = []
        test = dictionary.doc2bow(content)
        test_tfidf = tfidf_model[test]
        sims = tfidf_index[test_tfidf]
        similarity = list(enumerate(sims))
        for each in similarity:
            each = {each[0]:each[1]}
            each_row.append(each)
            each_row = sorted(each_row,key = lambda x:x.values(),reverse = True)
            #print each_row
        similarities.append(each_row)
    #将相似度写入txt
    with open('tfidf_similarities.txt','w') as f:
        for each_row in similarities:
            each_row = str(each_row)
            f.write(each_row + '\n')
            
def lsi_similarity(texts,topics):
    '''利用文档创建LSI模型与索引,
       计算文档间的两两相似度并生成一个txt文件，将结果导入其中。
       输入是文档列表与主题数目。
       最后在程序的当前目录下生成一个txt文件'''
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    #利用这些语料，创建tfidf模型
    tfidf_model = gensim.models.TfidfModel(corpus)
    #计算每个文档的tfidf
    tfidfs = tfidf_model[corpus]
    #build lsimodel
    lsi_model = gensim.models.LsiModel(tfidfs, id2word=dictionary, num_topics=topics)
    corpus_lsi = lsi_model[tfidfs]
    #build index of lsi
    lsi_index = gensim.similarities.MatrixSimilarity(corpus_lsi)
    similarities = []
    for i in range(len(texts)):
        content = texts[i]
        each_row = []
        test = dictionary.doc2bow(content)
        #使用tfidf模型向量化
        test_tfidf = tfidf_model[test]
        #使用lsi模型向量化
        test_lsi = lsi_model[test_tfidf]
        #计算lsi相似度
        sims = lsi_index[test_lsi]
        similarity = list(enumerate(sims))
        for each in similarity:
            each = {each[0]:each[1]}
            each_row.append(each)
            each_row = sorted(each_row,key = lambda x:x.values(),reverse = True)
            #print each_row
        similarities.append(each_row)
    #将相似度写入txt
    with open('lsi_similarities.txt','w') as f:
        for each_row in similarities:
            each_row = str(each_row)
            f.write(each_row + '\n')
    
    
    
def lda_similarity(texts,topics):
    '''利用文档创建LDA模型与索引,
       计算文档间的两两相似度并生成一个txt文件，将结果导入其中。
       输入是文档列表与主题数目，
       最后在程序的当前目录下生成一个txt文件'''
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    #利用这些语料，创建tfidf模型
    tfidf_model = gensim.models.TfidfModel(corpus)
    #计算每个文档的tfidf
    tfidfs = tfidf_model[corpus]    
    #build LDAmodel
    lda_model = gensim.models.LdaModel(tfidfs, id2word=dictionary, num_topics=topics)
    #(vectors)tfidf to LDA
    corpus_lda = lda_model[tfidfs]
    #build index of LDA
    lda_index = gensim.similarities.MatrixSimilarity(corpus_lda)
    similarities = []
    for i in range(len(texts)):
        content = texts[i]
        each_row = []
        #test是测试数据
        test = dictionary.doc2bow(content)
        #使用tfidf模型向量化
        test_tfidf = tfidf_model[test]
        #使用lda模型向量化
        test_lda = lda_model[test_tfidf]
        #计算lda相似性
        sims = lda_index[test_lda]
        similarity = list(enumerate(sims))
        for each in similarity:
            each = {each[0]:each[1]}
            each_row.append(each)
            each_row = sorted(each_row,key = lambda x:x.values(),reverse = True)
            #print each_row
        similarities.append(each_row)
    #将相似度写入txt
    with open('lda_similarities.txt','w') as f:
        for each_row in similarities:
            each_row = str(each_row)
            f.write(each_row + '\n')
            

    
def similarity_txt(path,topics):
    '''创建TFIDF、LSI、LDA模型与索引,
       计算文档间的两两相似度并生成txt文件，将结果导入其中。
       输入是保存txt文档的目录的绝对路径与主题数目，
       最后在程序的当前目录下生成三个txt文件，分别保存三种模型
       的相似性计算结果'''
    address = create_address(path)
    contents = save_documents(address)
    texts = preprocess(contents)
    tfidf_similarity(texts)
    lsi_similarity(texts,topics)
    lda_similarity(texts,topics)
    
if __name__ == '__main__':
    path = 'D:\\anaconda_prj\\jaccord\\cn_txts'
    topics = 5
    similarity_txt(path,topics)
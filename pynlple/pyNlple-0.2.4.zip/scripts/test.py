from pynlple.ml.vectorizers import GensimVectorModel

gensim = GensimVectorModel('E:\Projects\YouScan\data-science-lab\data\word2vec\gensim_word2vec_rus_fb+smi+ys+OS_\'size\'=380.tst')

vecs = gensim.transform([['я', 'пришел', 'домой']])

print(vecs)
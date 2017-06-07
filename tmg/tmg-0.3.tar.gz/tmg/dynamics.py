from __future__ import  division
import numpy as np

class Dynamics():
    def __init__(self, n_components=None, init=None, tol=1e-4, max_iter=25, components_ = 0):
        self.n_components = n_components
        self.init = init
        self.tol = tol
        self.max_iter = max_iter
        self.components_ = components_


    #create the strategy space of the games
    # alpha is the parameter of the Dirichlet - default 1

    def get_strat_sapce(self, alpha = 1):
        p = np.random.dirichlet([alpha]*self.n_topics, self.components_ )
        p = np.asmatrix(p)
        return p

    # takes as input a normalized tfidf matrix and output a similarity graph
    # lap indicates the use of the laplacian graph - default True
    # spars indicates the sparsification of the graph - default True

    def get_graph(self, tfidf, lap = 1, spars = 1):
        S = tfidf * tfidf.transpose()
        if lap == 1:
            Ssum = S.sum(axis=1)
            Ssum = np.power(Ssum, -.5)
            Ssum = Ssum.transpose().tolist()[0]
            S12 = np.diag(Ssum)
            S12[~ np.isfinite(S12)] = 0
            S = S12 * S * S12
        if spars == 1:
            knn = np.ceil(np.log(len(S)))
            for i in range(0, len(S)):
                vals = np.sort(S[i])
                val = vals.tolist()[0][-int(knn)]
                S[i, np.where(S[i] < val)[1]] = 0
                S[i, i] = 0
            S = (S + S.transpose()) / 2
        return S


    # run  the dynamics of the topic modelling games

    def games(self,tfidf):
        A = self.get_graph(tfidf)
        strat_sapce = self.get_strat_sapce(A.shape[0])
        iter = 0
        P = np.empty([1,self.maxiter], dtype=object)
        while True:
            P[0,iter] = strat_sapce
            q = A.dot(p)
            pnew = q/q.sum(axis=1)
            diff = np.linalg.norm(p-pnew)
            p = pnew
            if iter < self.maxiter or diff < self.tol:
                break
            iter += 1
        return [p,A,P]
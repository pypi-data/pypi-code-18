# -*- coding: utf-8 -*-
# for demostration of matrix operating

import types
import tkinter as tk

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import mymat


class MatrixDemo(object):
    '''MatrixDemo has 1 (principal) proptery
    printmod: printmod'''
    def __init__(self, printmod='t'):
        self.printmod = printmod
        if printmod in {'t', 'tex', 'T', 'Tex'}:
            def func(obj, x, *args, **kwargs):
                print(x.totex(), *args, **kwargs)
            self.print = types.MethodType(func, self)
        else:
            def func(obj, x, *args, **kwargs):
                print(x, *args, **kwargs)
            self.print = types.MethodType(func, self)

    
    def demo(self, A):
        raise NotImplementedError

class GaussDemo(MatrixDemo):

    @classmethod
    def makeup(cls, m=3, n=4, lb=-5, ub=5):
        A = mymat.MyMat.randint(m, n, lb, ub)
        L = A.tril()[:,:m]
        U = A.itriu()
        for k in range(m):
            if L[k,k] == 0:
                L[k,k] = np.random.randint(lb, ub)
        A = mymat.MyMat((L * U).tolist(), dtype=np.float64)
        return A
    
    def demo(self, A):
        # Elimination Process
        tol = 0.0001
        r, c = A.shape
        m = min(r, c)
        print('Consider matrix:')
        self.print(A)
        print('------------------Elimination Process-------------------')
        k = l = 1
        cols = []
        while k <= r and l < c:
            if all(A[k:r, l] == 0):
                l += 1
                continue
            #p = max(abs(A[k:r,k]))   # get the pivot
            #ind = abs(A[k:r,k]).tolist().index(p) + 1
            for index, p in enumerate(A[k:r, l].T.tolist()):
                # find the first nonzero element or the element with maximum abstract value
                if p != 0:
                    ind = index
                    break
            if abs(p) < tol:
                raise Exception('the pivot is too small!')
            else:
                if ind != 0:
                    t = ind + k
                    A[k, l:c], A[t, l:c] = A[t, l:c].copy(), A[k, l:c].copy()    # swap row r and row k
                    print('-------------GaussI: row%d <-> row%d'%(k, t)) # print rule (elementary transform)
                    self.print(A)                                                     # print matrix

                if A(k,l) != 1:
                    if l < c:
                        print('------------GaussII: row{0} * 1/A({0},{0}), A({0},{0})={1}'.format(k, A[k,k])) # rule_print
                        A[k, (l+1):c] /= A[k, l]; A[k, l] = 1
                    self.print(A)

                if k < r:                                                            # [1  beta] __\ [1  beta         ]       
                    for s in range(k+1, r+1):                                           # [alpha A] --/ [0 A-alpha*beta]
                        if A[s,k] != 0:
                            print('------------GaussIII: row{1} -A({1},{0})*row{0}, A({1},{0})={2}'.format(k, s, A[s,k]))  # print rule (elementary transform)
                    A[k+1:r, l+1:c] -= A[k+1:r, l] * A[k, l+1:c]
                    A[k+1:r, l] = 0
                    self.print(A)

                cols.append(l)
                k += 1; l += 1

        # Back Substitution Process
        print('-----------------------Back Substitution Process--------------------')
        R = len(cols)  # rank(A)
        for l in cols[-1:0:-1]:
            for k, a in enumerate(A[1:R-1, l].T.tolist(), 1):
                if a != 0:
                    print('------------GaussIII: row{1} - A({1},{2})*row{0}, A({1},{0})={3}'.format(R, k, l, a))
                    if l<c:
                        A[k, l+1:c] -= a * A[R, l+1:c]
            A[1:R-1, l] = 0
            self.print(A)
            R -= 1
        '''for i in range(r-1, 0, -1):                                            # [a beta C] __\ [a 0 C-beta*B]
            if A[i,i] != 0:                                                    # [0 E    B] --/ [0 E B       ]
                A[i,i:c] = (A[i,i:c]-A[i,i+1:r]*A[i+1:r,i:c])/A[i,i]
                print('---------------Gauss2nd/3rd: calculus row %d'%i)        # print rule (elementary transform)
                print(A)   ''' 



def gaussDemo(A, tol=0.01):
    '''Gauss Elimination
A: matrix of full rank
exmaple:
>>> import mymat
>>> A=mymat.MyMat('1,1,1,6;0,4,-1,5;2,-2,1,1')
>>> GaussDemo(A)  # get the echelon form of A
'''

    # Elimination Process
    r, c = A.shape
    m = min(r, c)
    print('Consider matrix:')
    print(A)
    print('------------------Elimination Process-------------------')
    k = l = 1
    cols = []
    while k<=r and l<c:
        if all(A[k:r, l]==0):
            l += 1
            continue
        #p = max(abs(A[k:r,k]))   # get the pivot
        #ind = abs(A[k:r,k]).tolist().index(p) + 1
        for index, p in enumerate(A[k:r, l].T.tolist()):
            # find the first nonzero element or the element with maximum abstract value
            if p != 0:
                ind = index
                break
        if abs(p) < tol:
            raise Exception('the pivot is too small!')
        else:
            if ind != 0:
                t = ind+k
                A[k, l:c], A[t, l:c] = A[t, l:c].copy(), A[k, l:c].copy()    # swap row r and row k
                print('-------------Gauss1: row%d <-> row%d'%(k, t)) # print rule (elementary transform)
                print(A)                                                     # print matrix

            if A(k,l) != 1:
                if l < c:
                    print('------------Gauss2: row{0} * 1/A({0},{0}), A({0},{0})={1}'.format(k, A[k,k])) # rule_print
                    A[k, (l+1):c] /= A[k, l]; A[k, l] = 1
                print(A)

            if k < r:                                                            # [1  beta] __\ [1  beta         ]       
                for s in range(k+1, r+1):                                           # [alpha A] --/ [0 A-alpha*beta]
                    print('------------Gauss3: row{1} -A({1},{0})*row{0}, A({1},{0})={2}'.format(k, s, A[s,k]))  # print rule (elementary transform)
                A[k+1:r, l+1:c] -= A[k+1:r, l]*A[k, l+1:c]
                A[k+1:r, l] = 0
                print(A)

            cols.append(l)
            k += 1; l += 1

    # Back Substitution Process
    print('-----------------------Back Substitution Process--------------------')
    R = len(cols)  # rank(A)
    for l in cols[-1:0:-1]:
        for k, a in enumerate(A[1:R-1, l].T.tolist(), 1):
            if a != 0:
                print('------------Gauss3: row{1} - A({1},{2})*row{0}, A({1},{0})={3}'.format(R, k, l, a))
                if l<c:
                    A[k, l+1:c] -= a*A[R, l+1:c]
        A[1:R-1, l] = 0
        print(A)
        R -= 1
    '''for i in range(r-1, 0, -1):                                            # [a beta C] __\ [a 0 C-beta*B]
        if A[i,i] != 0:                                                    # [0 E    B] --/ [0 E B       ]
            A[i,i:c] = (A[i,i:c]-A[i,i+1:r]*A[i+1:r,i:c])/A[i,i]
            print('---------------Gauss2nd/3rd: calculus row %d'%i)        # print rule (elementary transform)
            print(A)   '''                                                    # print matrix

def denoiseDemo(n=None, rate=0.15):
    # n is a row-vector
    import numpy as np
    import matplotlib.pyplot as plt
    if n is None:
        N = 200
        x = np.linspace(0,10,N)
        signal = mymat.MyMat(np.sin(x))
        noise =mymat.R(1,N, np.random.rand)/10
        n = signal + noise
    N = n.shape[1]
    Fn = n * mymat.FM(N)      # Fourier transform
    M = int(N*rate); M1=M // 2; M2 = M - M1
    P = Fn.proj(ind2=list(range(1, M1+1))+list(range(N-M2+1, N+1)))  # get the low-frequence part
    D = np.real(P*mymat.FIM(N))  # Fourier inverse transform
    p1 = plt.plot(signal.tolist(), label='Signal')
    p2 = plt.plot(n.tolist(), label='Noised')
    p3 = plt.plot(D.tolist(), label='Denoised')
    plt.legend()
    plt.show()

def show(A, ax):
    # show matrix on an axes
    offset=0.5
    m, n = A.shape
    B = A.tofrac()
    return [[ax.text(j-offset, m-i+offset, B[i,j], fontsize=25, horizontalalignment='center', verticalalignment='center',) for j in range(1, n+1)] for i in range(1, m+1)]

def clear(texts):
    for row in texts:
        for t in row:
            t._text = ''
    

def draw_grid(m,n, ax):
    for k in range(m+1):
        ax.plot([0,n], [k,k])
    for l in range(n+1):
        ax.plot([l,l], [0,m])

def main():
    global ax, texts,A,k,l,cols,r,c
    
    root = tk.Tk()

    # matplotlib
    f = Figure(figsize=(5, 4), dpi=100)
    ax = f.add_subplot(111)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def reset():
        global k, l, cols
        k = l = 1
        cols = []

    A=mymat.MyMat('2, -8, 0,4;4, -13, -2,6;−2, 7, 4, −3', dtype=np.float64).tofrac()
    r, c = A.shape
    m = min(r, c)
    reset()

    draw_grid(r, c, ax)
    texts = show(A,ax)
    canvas.show()


    def on_key_event(event):
        print('you pressed %s' % event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)


    def _random():
        global A, texts
        if erow.get():
            r = int(erow.get())
        if ecol.get():
            c = int(ecol.get())
        A = (mymat.MyMat.randint(r, r).itril() * mymat.MyMat.randint(r, c).triu()).tofrac()
        m = min(r, c)
        reset()
        clear(texts)
        draw_grid(r, c, ax)
        texts = show(A, ax)
        canvas.show()


    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _next():
        tol = 0.0001
        global cols, ax, texts, A, k, l

        if k<=r and l<c:
            if all(A[k:r, l]==0):
                l += 1
                return
            #p = max(abs(A[k:r,k]))   # get the pivot
            #ind = abs(A[k:r,k]).tolist().index(p) + 1
            for index, p in enumerate(A[k:r, l].T.tolist()):
                # find the first nonzero element or the element with maximum abstract value
                if p != 0:
                    ind = index
                    break
            if abs(p) < tol:
                raise Exception('the pivot is too small!')
            else:
                if ind != 0:
                    t = ind+k
                    A.row_transform1(k, t)   # swap row k and row k
                    ax.set_title('# 1: row%d <-> row%d'%(k, t)) # print rule (elementary transform)
                    clear(texts); texts = show(A, ax); canvas.show()

                if A(k,l) != 1:
                    if l < c:
                        ax.set_title('# 2: row{0} * 1/A({0},{0}), A({0},{0})={1}'.format(k, A[k,k])) # rule_print
                        A[k, (l+1):c] /= A[k, l]; A[k, l] = 1
                    clear(texts); texts = show(A, ax); canvas.show()

                if k < r:                                                            # [1  beta] __\ [1  beta         ]       
                    for s in range(k+1, r+1):                                           # [alpha A] --/ [0 A-alpha*beta]
                        ax.set_title('# 3: row{1} -A({1},{0})*row{0}, A({1},{0})={2}'.format(k, s, A[s,k]))  # print rule (elementary transform)
                    A[k+1:r, l+1:c] -= A[k+1:r, l]*A[k, l+1:c]
                    A[k+1:r, l] = 0
                    clear(texts); texts = show(A, ax); canvas.show()

                cols.append(l)
                k += 1; l += 1
        else:
            # Back Substitution Process
            R = len(cols)  # rank(A)
            for l in cols[-1:0:-1]:
                for k, a in enumerate(A[1:R-1, l].T.tolist(), 1):
                    if a != 0:
                        ax.set_title('# 3: row{1} - A({1},{2})*row{0}, A({1},{0})={3}'.format(R, k, l, a))
                        if l<c:
                            A[k, l+1:c] -= a*A[R, l+1:c]
                A[1:R-1, l] = 0
                clear(texts); texts = show(A, ax); canvas.show()
                R -= 1


    bquit = tk.Button(master=root, text='推出', command=_quit)
    bquit.pack(side=tk.BOTTOM)
    bselect = tk.Button(master=root, text='随机', command=_random)
    bselect.pack(side=tk.BOTTOM)
    bselect = tk.Button(master=root, text='下一步', command=_next)
    bselect.pack(side=tk.BOTTOM)

    lshape = tk.Label(root, text="性质")
    lshape.pack(side = tk.LEFT)
    erow = tk.Entry(root, bd=5)
    erow.pack(side = tk.LEFT)
    erow.insert(0, "3")
    lrow = tk.Label(root, text="行")
    lrow.pack(side = tk.LEFT)

    ecol = tk.Entry(root, bd=5)
    ecol.pack(side = tk.LEFT)
    ecol.insert(0, "4")
    lcol = tk.Label(root, text="列")
    lcol.pack(side = tk.LEFT)
    # bevolve = tk.Button(master=root, text='Evolve', command=_evolve)
    # bevolve.pack(side=tk.BOTTOM)
    # bconfirm = tk.Button(master=root, text='Confirm', command=_confirm)
    # bconfirm.pack(side=tk.BOTTOM)
    # bselect = tk.Button(master=root, text='Best', command=_best)
    # bselect.pack(side=tk.BOTTOM)

    tk.mainloop()


    

"""
Python Finite Element Analysis (PyFEA)

Galerkin Approximation Method
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------[TO BE FIXED]------------------------------------
# Should return GLOBAL deflections
# Calculate Deflections, w
def galerkinApprox(K, L, f_dofs):
    w = np.dot(np.linalg.inv(K[0:f_dofs, 0:f_dofs]),L[0:f_dofs])
    return w
# -----------------------------[TO BE FIXED]------------------------------------


# Build Global Load Matrix, L
def buildLoad_L(q, length_ele):
    L = np.zeros(shape=(n_nodes,1), dtype=np.float)
    L_ele = np.array([[1],
                      [1]], dtype=np.float)
    for i in range(n_ele):
        L[[[dofs_num_ele[i][0]],[dofs_num_ele[i][1]]],[0]] += q*length_ele[i]/2*L_ele

    return L


# Build Global Stiffness Matrix, K
def buildStiffness_K(n_ele, length_ele, dofs_num_ele, n_nodes):
    K = np.zeros(shape=(n_nodes,n_nodes), dtype=np.float)
    K_ele = np.array([[ 1,-1],
                      [-1, 1]], dtype=np.float)
    for i in range(n_ele):
        K[[[dofs_num_ele[i][0]],[dofs_num_ele[i][1]]],[dofs_num_ele[i][0],dofs_num_ele[i][1]]] += K_ele/length_ele[i]

    return K


# Initiate Variables from User Input
def initiateVar():
    # User input: number of nodes
    try:
        n_nodes = int(input("Number of Nodes (default=3): "))
    except ValueError:
        n_nodes = 3
    # User input: node freedoms
    dofs_num_inp = np.array(range(n_nodes))
    for i in range(n_nodes):
        try:
            dofs_num_inp[i] = int(input("Node[" + str(i+1) + "] Condition < 0:free / 1:fixed > (default=0): "))
        except:
            dofs_num_inp[i] = 0

    # User input: total length
    try:
        length = int(input("Length/Span (default=1): "))
    except ValueError:
        length = 1
    # User input: distributed load
    try:
        q = float(input("Distributed Load (default=1): "))
    except ValueError:
        q = 1
    # User input: element lengths
    length_ele = np.array([])
    counter = 0
    while np.sum(length_ele) != length:
        counter += 1
        try:
            length_ele = np.append(length_ele,[float(input("Length/Span of Element[" + str(counter) + "] (default=0.5): "))])
        except ValueError:
            length_ele = np.append(length_ele, 0.5)

    # ---------------------------[TO BE FIXED]----------------------------------
    # Just plain ugly
    n_dofs = n_nodes
    f_dofs = n_nodes - sum(dofs_num_inp)
    f_dofs_index = np.where(dofs_num_inp == 0)[0]
    d_dofs_index = np.where(dofs_num_inp == 1)[0]
    n_ele  = n_nodes-1
    node_num = np.array(range(n_nodes))

    n_dofs_index = f_dofs_index
    transfer_tbchanged = np.array([], dtype=int)
    while d_dofs_index[-1] > n_dofs_index[-1]:
        transfer_tbchanged = np.append(transfer_tbchanged, d_dofs_index[-1])
        d_dofs_index = np.delete(d_dofs_index, [len(d_dofs_index)-1])
    transfer_tbchanged = np.append(transfer_tbchanged[::-1], d_dofs_index)
    n_dofs_index = np.append(n_dofs_index, transfer_tbchanged)
    dofs_num = np.array([0 for i in range(n_nodes)])
    for i in range(n_nodes):
        dofs_num[n_dofs_index[i]] = i
    # ---------------------------[TO BE FIXED]----------------------------------

    dofs_num_ele = np.zeros(shape=(n_ele,2), dtype=int)
    node_num_ele = np.zeros(shape=(n_ele,2), dtype=int)
    for j in range(n_ele):
        dofs_num_ele[j] = [dofs_num[j],dofs_num[j+1]]
        node_num_ele[j] = [node_num[j],node_num[j+1]]
    # ---------------------------[TO BE FIXED]----------------------------------
    return n_ele, f_dofs, length, length_ele, dofs_num_ele, n_nodes, q


# Plot Deformation Shape of Cable
def plotDeformation(length, w):
    # Plot Original Cable
    plt.plot([0, length], [0, 0], 'b-', linewidth=2)

    # Plot Deformation
    start_x = 0
    start_y = 0
    for i in range(len(w)):
        plt.plot([start_x, start_x+length_ele[i]/length], [start_y, -w[i]], 'r--', linewidth=2)
        start_x += length_ele[i]/length
        start_y -= w[i]

    # Legend & Axes Labels
    plt.title('Galerkin Approximation 1-D Cable')
    plt.xlabel(r'$x/L$')
    plt.ylabel(r'$P/q/L^2*w$')
    plt.legend(['Original', 'Approximate Deflection'], loc=3)

    # Set Axes Limits
    axes = plt.gca()
    axes.set_xlim([-length*0.25, length*1.25])
    axes.set_ylim([-np.amax(w)*1.25, np.amax(w)*0.25])

    # Show Plot
    plt.grid()
    plt.show()

# -----------------------------[TO BE FIXED]------------------------------------
# Does not work
# Output Results to [Filename].[Filetype]
def printResults(K):
    # Open 'results.txt' file
    r = open('results.txt','w')

    # Write data onto 'results.txt'
    r.write("Global Stiffness Matrix:\n")
    r.write("K")

    # Close file
    r.close()
# -----------------------------[TO BE FIXED]------------------------------------

def printOutput(K, L, w):
    # Results Header
    print("", end='\n')
    print("--------------------[ Results ] --------------------", end='\n\n')

    # Stiffness Matrix
    print("Global Stiffness Matrix [K]: ", end='\n')
    print(K, end='\n\n')

    # Load Matrix
    print("Global Load Matrix [L]: ", end='\n')
    print(L, end='\n\n')

    # Displacement
    print("Global Displacement Matrix [w]: ", end='\n')
    print(w, end='\n\n')

if __name__ == '__main__':
    n_ele, f_dofs, length, length_ele, dofs_num_ele, n_nodes, q = initiateVar()
    K = buildStiffness_K(n_ele, length_ele, dofs_num_ele, n_nodes)
    L = buildLoad_L(q, length_ele)
    w = galerkinApprox(K, L, f_dofs)
    printOutput(K, L, w)
    plotDeformation(length, w)

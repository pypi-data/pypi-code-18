"""
Python Finite Element Analysis (PyFEA)

Free Vibration of a Cable
"""

import numpy as np
import matplotlib.pyplot as plt

# Build Global Stiffness Matrix, K
def buildStiffness_K(n_ele, length_ele, dofs_num_ele, n_nodes):
    K = np.zeros(shape=(n_nodes,n_nodes), dtype=np.float)
    K_ele = np.array([[ 1,-1],
                      [-1, 1]], dtype=np.float)
    for i in range(n_ele):
        K[[[dofs_num_ele[i][0]],[dofs_num_ele[i][1]]],[dofs_num_ele[i][0],dofs_num_ele[i][1]]] += K_ele/length_ele[i]

    return K

# Build Mass Matrix, M
def buildMass_M():
    M = np.zeros(shape=(n_nodes,n_nodes), dtype=np.float)
    M_ele = np.array([[2, 1],
                      [1, 2]], dtype = np.float) *
    return None

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:58:22 2017

@author: Matheus
"""

from utility.knnsearch import set_nbrs_knn
from utility.knnsearch import subset_nbrs


def wlseparate_ref_voting(arr, knn_lst, class_file, threshold, n_classes):
    
    ids = []
    
    d_base, idx_base = set_nbrs_knn(arr, arr, np.max(knn_lst),
                                    return_dist=True)
                                    
    for k in knn_lst:
        dx_1, idx_1 = subset_nbrs(d_base, idx_base, k)
        
        # Calculating the geometric descriptors.
        gd_1 = geodescriptors(arr, idx_1)
    
        # Normalizing geometric descriptors
        gd_1 = ((gd_1 - np.min(gd_1, axis=0)) /
                (np.max(gd_1, axis=0) - np.min(gd_1, axis=0)))
    
        # Classifying the points based on the geometric descriptors.
        classes_1, cm_1 = classify(gd_1, n_classes)
    
        # Selecting which classes represent wood and leaf. Wood classes are masked
        # as True and leaf classes as False.
        class_table = pd.read_csv(class_file)
        class_ref = np.asarray(class_table.ix[:, 1:]).astype(float)
        new_classes = class_select(classes_1, cm_1, class_ref)
        
        ids.append((new_classes == 1) | (new_classes == 2))
    
    idf = np.array(ids[0], ndmin=2).T
    for i in ids[1:]:
        idf = np.hstack((idf, np.array(i, ndmin=2).T))
    votes = np.sum(idf, axis=1)
#        
    mask = votes >= threshold
    
    return arr[mask], arr[~mask]
#    return ids
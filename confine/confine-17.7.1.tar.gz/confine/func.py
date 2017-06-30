import networkx as nx
import pickle
import pkg_resources

LCC_PATH = pkg_resources.resource_filename('confine', 'NET/')
LCC_Zscore= pickle.load(open(LCC_PATH+'LCC_Zscore_10k.p', 'r' ))
import copy

def CONFINE(*args):

    data=args[0]
    G=args[1]
    LCC_min=args[2]
    LCC_max = args[3]
    G_nodes=G.nodes()
    pvalue=[];geneIds=[]
    for row in data:
        if int(row[0]) in G_nodes:
            geneIds.append(int(row[0]))
            pvalue.append(row[1])

    #------- sort genes based on p-values----------
    sorted_index = sorted(range(len(pvalue)), key=lambda k: pvalue[k])
    sorted_genes=[];sorted_pvalues=[]
    for id in sorted_index:
        sorted_genes.append(geneIds[id])
        sorted_pvalues.append(pvalue[id])
    #----------------------------------------------

    z_list=[]
    pval_cut_list=[]
    z_score_old= - 1000000000
    LCC_old=0

    for id_cut in xrange(LCC_min,len(sorted_genes)):

        genes=sorted_genes[0: id_cut+1]
        #-----------------------------------------------Get LCC
        g=nx.subgraph(G,genes)
        num_mapped = int(len(g.nodes()))
        cc=nx.connected_component_subgraphs(g)
        l=[len(i) for i in cc]
        l.sort(reverse=True)
        largest= l[0]

        if largest > LCC_max: break
        if LCC_min <=largest<= LCC_max and largest > LCC_old:
            LCC_old = copy.copy(largest)
            #-----------------------------------------------Randomization
            s_info=LCC_Zscore[num_mapped]
            l_mean = s_info[0]
            l_std = s_info[1]
            #------------------------------------------------------------

            if l_std == 0:
                z_score = 0
            else:
                z_score = (float(largest) - l_mean)/l_std


            z_list.append(z_score)

            pval_cut_list.append(sorted_pvalues[id_cut])

            #----------------------------------Updating for the significant values
            if z_score > z_score_old:

                z_score_old=copy.copy(z_score)
                id_sig=int(len(z_list)-1)
                sig_genes = sorted_genes[0: id_cut + 1]

    # -----------------------------------------------Get sig LCC

    g_sig = nx.subgraph(G, sig_genes)
    Clusters= sorted(list(nx.connected_component_subgraphs(g_sig)), key=len, reverse=True)
    sig_Cluster_LCC=Clusters[0]

    result=[z_list,pval_cut_list,sig_Cluster_LCC,id_sig]
    return result
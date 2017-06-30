def run(*args):
    import pkg_resources
    if args[0]=='test':
        TEST_PATH = pkg_resources.resource_filename('confine', 'TEST/')
        dir_in = TEST_PATH+'test.csv'
        f = 'test'
        lcc_min = 50
        lcc_max = 350
    else:
        f=args[0]
        dir_in=str(raw_input("Where the file is located in? "))
        print "You entered: ------", str(f),' ------'
        lcc_min = int(raw_input("Enter the minimum size of LCC, we recommend a number between 30 and 50: "))
        lcc_max = int(raw_input("Enter the maximum size of LCC, we recommend a number between 300 and 500: "))
    print '.....loading data.....'

    import os
    import pickle
    import time
    start_time = time.time()



    NET_PATH = pkg_resources.resource_filename('confine', 'NET/')
    id_to_sym = pickle.load(open(NET_PATH +'id_to_sym_human.p', 'r' ))

    G = pickle.load(open(NET_PATH+'PPI_2015_raw.p', 'r' ))

    file = open(dir_in, "r")
    initial_data = file.read().splitlines()
    file.close()

    threshold=0.05
    gene=[];pval=[]

    for row in initial_data:
        n=row.strip().split(',')
        p=float(n[1].strip())
        g=int(n[0].strip())
        if p<=threshold:
            gene.append(g)
            pval.append(p)


    print 'Number of genes with P.val<0.05: ',len(gene)
    print '.....Identifying disease module.....'

    data=zip(gene,pval)
    #---------------------
    from func import CONFINE as conf
    result=conf(data,G,lcc_min,lcc_max)

    z_list=result[0]
    pval_cut_list=result[1]
    sig_Cluster_LCC=result[2]
    z_score=z_list[result[3]]
    p_val_cut=pval_cut_list[result[3]]

    print '--------------------'
    print 'LCC size: ',len(sig_Cluster_LCC.nodes())
    print 'Z-score: ',z_score
    print 'P.val cut-off: ',p_val_cut
    print '--------------------'

    directory_name=f+'_'+str(time.time())
    if not os.path.exists(directory_name):os.makedirs(directory_name)
    b=open(directory_name+'/LCC_'+f+'.txt',"w")
    for node in sig_Cluster_LCC.nodes():
        try:
            print>> b, str(id_to_sym[int(node)])+','+ str(int(node))
        except KeyError:
            print>> b, '    ' + ',' + str(int(node))

    b.close()

    from pylab import plt, matplotlib
    fig=plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    #----------------------------------------------------plotting--------


    ax.plot(pval_cut_list,z_list,'o',color='saddlebrown',markersize=4)
    plt.axvline(x=p_val_cut, color='r', linestyle='--')
    ax.set_xlabel('P.value cut-off',fontsize=25,fontweight='bold',labelpad=18)
    ax.set_ylabel('Z-Score',fontsize=25,fontweight='bold', labelpad=18)
    ax.set_title('LCC'+' = '+str(len(sig_Cluster_LCC.nodes()))+'   ,'+' Z-Score'+' = '+str("{0:.3f}".format(round(z_score,4))),
                 fontsize=20, fontweight='bold')
    ax.grid(True)
    plt.ylim(min(z_list)-min(z_list)/5,max(z_list)+max(z_list)/3)

    plt.savefig(directory_name+'/'+f+'.png',dpi=150,bbox_inches='tight'); plt.close()
    print("--- %s seconds ---" % (time.time() - start_time))

def check():

    list=['pip','pickle','networkx','os','time','pylab','pkg_resources']


    for p in list:

        try:

            __import__(p)
            print p, 'is installed'
            import pip

        except ImportError:
            pip.main(['install', p])
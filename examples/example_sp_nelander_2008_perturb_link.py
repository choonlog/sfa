# -*- coding: utf-8 -*-

import copy
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


import sfa
import sfa.vis
from sfa import calc_accuracy
from sfa import AlgorithmSet
from sfa import DataSet


if __name__ == "__main__":

    # Create containers for algorithm and data.
    algs = AlgorithmSet()
    ds = DataSet()

    # Load an algorithm and a data.
    algs.create('SP')
    alg = algs['SP']
    
    ds.create("NELANDER_2008")
    data = ds["NELANDER_2008"]

    results = {}
    alg.data = data
    alg.params.initialize()
    alg.params.use_rel_change = True
    alg.params.exsol_forbidden = True
    alg.initialize()
    
    b = np.zeros((data.A.shape[0],), dtype=np.float)
    b[data.n2i["EGF"]] = 1
    x_cnt = alg.compute(b)
    
    b = np.zeros((data.A.shape[0],), dtype=np.float)
    b[data.n2i["EGF"]] = 1
    alg.W[data.n2i["p-ERK"], data.n2i["p-MEK"]] *= 0.1
#    alg.initialize(data=False)
    x_exp = alg.compute(b)
    
    x_diff = x_exp[alg._iadj_to_idf] - x_cnt[alg._iadj_to_idf]
    #df_sim = pd.DataFrame(alg.result.df_sim.ix[5, :])
    df_sim = pd.DataFrame(x_diff)
    df_exp = pd.DataFrame(data.df_exp.ix[5, :])
    df_sim.columns = df_exp.columns
    df_sim.index = df_exp.index
    
    acc, cons = calc_accuracy(df_sim,
                              df_exp,
                              get_cons=True)
    
    
    print ("Accuracy: ", acc)
    brt = sfa.vis.HeatmapTable(cons)
    brt.column_label_fontsize = 4
    brt.ax.tick_params(axis='x', which='both', pad=0.01)
    
    brt.row_label_fontsize = 4
    brt.ax.tick_params(axis='y', which='both', pad=0.01)

    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.9, top=0.8,
                        wspace=0.1, hspace=0.1)

    brt.fig.set_size_inches(2, 3)
    brt.fig.savefig("%s_%s_MEKi.png"%(alg.abbr, data.abbr), dpi=300)
    
#    
#    ptbs = ['EGF', 'IGF1R','PI3K','mTOR','PKCdelta','p-MEK','EGFR']
#    vals = [1, -1, -1, -1, -1, -1, -1]
#    paths = []
#    for i, src in enumerate(ptbs):
#        x, p = alg.wire([src], [vals[i]], get_path=True)
#        paths.extend(p)
#    
#    paths = sorted(paths, key=lambda p: p[-1])
#    


#    x, paths = alg.wire(['EGF', 'p-MEK', 'EGFR'], [1, -1, -1], get_path=True)
#   
#    def get_link_str(x, y):
#        sign = data.dg.edge[x][y]['sign']
#        if sign>0:
#            return '->'
#        else:
#            return '-|'
#    
#    
#    for p in paths:
#        str_path = str(p[0])
#        if p[-1] != 'p-RAF':
#            continue
#            
#        for i in range(len(p)-1):
#            src = p[i]
#            tgt = p[i+1]            
#            str_link = get_link_str(src, tgt)
#            str_path += " %s %s"%(str_link, tgt)
#    
#        if p[0] == 'EGF':
#            ba = +1
#        else:
#            ba = -1
#            
#        F = alg.wire_single_path(data.dg, ba, p)
#        print (F, str_path)

# end of main

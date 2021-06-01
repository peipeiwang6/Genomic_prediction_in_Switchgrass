import sys,os
import pandas as pd
import numpy as np
from scipy.stats import zscore
df = pd.read_csv('/mnt/ufs18/home-110/peipeiw/Documents/Genome_selection/Distribution_of_markers/Markers_distribution_all_unique.txt',header=None,index_col=None,sep='\t')
gbs = df[df[0]=='GBS']
gbs = gbs.set_index(9)
coef = pd.read_csv('Coef_Training_Anthesis_Date_8632_Anthesis_Date_8632.csv',header=0,index_col=None,sep=',')
coef_median = coef.median(axis=0)
gbs2 = gbs.loc[coef_median.index.tolist(),:]
res = pd.concat([gbs2,coef_median],axis=1)
res.columns = [0,1,2,3,4,5,6,7,8,9,10,11]
genes = res.groupby([2]).sum()
genes['abs_coef'] = abs(genes[11])
genes = genes.sort_values(['abs_coef'], ascending=False)
## strategy 1, select the marker with highest abs coef for each gene
res['abs_coef'] = abs(res[11])
marker = res.sort_values(['abs_coef'], ascending=False).drop_duplicates(2,keep="first")
with open('Markers_first_for_each_gene_GBS_Anthesis_Date_8632.txt', 'w') as filehandle:
    for m in marker.index.tolist():
        filehandle.write('%s\n' % m)

geno = pd.read_csv('geno_training.csv',header=0,index_col=0,sep=',')
subgeno = geno.loc[:,marker.index.tolist()]
subgeno.to_csv('geno_training_first_for_each_gene.csv',header=True,index=True,sep=',')


## strategy 2, select markers of top 4000 genes with highest abs value of coef sum
genelist = genes.index.tolist()[0:4000]
marker = res[res[2].isin(genelist)].index.tolist()
with open('Markers_top4000_genes_GBS_Anthesis_Date_8632.txt', 'w') as filehandle:
    for m in marker:
        filehandle.write('%s\n' % m)

geno = pd.read_csv('geno_training.csv',header=0,index_col=0,sep=',')
subgeno = geno.loc[:,marker]
subgeno.to_csv('geno_training_top4000.csv',header=True,index=True,sep=',')

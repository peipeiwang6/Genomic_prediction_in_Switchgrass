'''
input 1: imputed file
'''

import sys,os
import pandas as pd
df = pd.read_csv(sys.argv[1], sep='\t', index_col = 0, header = 0, low_memory=False,dtype='string')
out = open(sys.argv[1]+'_geno.csv','w')
title = 'ID'
for i in range(0,len(df.index)):
	title = title + ',' + df.index[i]
	
out.write(title + '\n')


for i in range(0,len(df.columns)):
	res = df.columns[i] + ',' + ','.join(df.iloc[:,i])
	out.write(res + '\n')
	
out.close()
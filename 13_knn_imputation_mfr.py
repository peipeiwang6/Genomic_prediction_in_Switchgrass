'''
input 1: file to be imputed
'''

import sys,os
sys.path.append('/mnt/home/mengfanr/Switchgrass/test/Imputer.py/imputer')
from imputer import Imputer
import pandas as pd
from copy import deepcopy
impute = Imputer()
file = sys.argv[1]
df = pd.read_csv(file, sep='\t', index_col = 0, header = 0,low_memory=False)
colname = df.columns.tolist()
df1 = deepcopy(df)
df2 = deepcopy(df)
df3 = deepcopy(df)
df4 = deepcopy(df)	
df5 = deepcopy(df)	
for col in colname:
	df1 = pd.DataFrame(impute.knn(X=df1, column=col, k=3),index=df.index, columns = df.columns)
	df2 = pd.DataFrame(impute.knn(X=df2, column=col, k=4),index=df.index, columns = df.columns)
	df3 = pd.DataFrame(impute.knn(X=df3, column=col, k=5),index=df.index, columns = df.columns)
	df4 = pd.DataFrame(impute.knn(X=df4, column=col, k=6),index=df.index, columns = df.columns)
	df5 = pd.DataFrame(impute.knn(X=df5, column=col, k=7),index=df.index, columns = df.columns)

res = (df1+df2+df3+df4+df5)/5
res.to_csv(sys.argv[1].split('.txt')[0]+'_KNN_impute.txt', index=True, header=True,sep="\t")

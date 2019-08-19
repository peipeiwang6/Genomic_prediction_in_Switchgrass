'''
input 1: file to be imputed
'''

import sys,os
sys.path.append('/mnt/home/mengfanr/Switchgrass/test/Imputer.py/imputer')
from imputer import Imputer
import pandas as pd
impute = Imputer()
file = sys.argv[1]
df = pd.read_csv(file, sep='\t', index_col = 0, header = 0,low_memory=False)
colname = df.columns.tolist()
df1 = df.copy()
df2 = df.copy()
df3 = df.copy()	
df4 = df.copy()	
df5 = df.copy()	
for col in colname:
	impute.knn(X=df1, column=col, k=3)
	impute.knn(X=df2, column=col, k=4)
	impute.knn(X=df3, column=col, k=5)
	impute.knn(X=df4, column=col, k=6)
	impute.knn(X=df5, column=col, k=7)

res = (df1+df2+df3+df4+df5)/5
res.to_csv(sys.argv[1].split('.txt')[0]+'_KNN_impute.txt', index=True, header=True,sep="\t")

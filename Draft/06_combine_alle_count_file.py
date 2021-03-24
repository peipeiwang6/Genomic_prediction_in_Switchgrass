'''
input1: list file with files to be combined
input2: name for output file
'''

import os,sys
import pandas as pd

inp = open(sys.argv[1],'r').readlines()
n = 0
for inl in inp:
	if n == 0:
		df = pd.read_csv(inl.strip(), sep='\t', index_col = 0, header = 0)
		n += 1
	else:
		df2 = pd.read_csv(inl.strip(), sep='\t', index_col = 0, header = 0)
		df = pd.concat([df,df2],axis=0)
#		print(inl)

df.to_csv(sys.argv[2], index=True, header=True,sep="\t")
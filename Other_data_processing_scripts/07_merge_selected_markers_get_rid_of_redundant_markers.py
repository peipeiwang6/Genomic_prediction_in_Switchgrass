import sys,os
import pandas as pd
n = 0
D = {}
for files in os.listdir('./'):
	if files.startswith('Exome') and files.endswith('csv'):
		df = pd.read_csv(files, sep=',', index_col = 0, header = 0)
		colnames = df.columns.tolist()
		for col in colnames:
			if col not in D:
				D[col] = 1
			else:
				df = df.drop([col], axis=1)
		df = df.add_prefix('_'.join(files.split('_')[0:3]) + '_')
		if n == 0:
			res = df
		else:
			res = res.merge(df, left_index=True, right_index=True)
		n += 1
		print(files)

for files in os.listdir('./'):
	if files.startswith('GBS')  and files.endswith('csv'):
		df = pd.read_csv(files, sep=',', index_col = 0, header = 0)  
		colnames = df.columns.tolist()
		for col in colnames:
			if col not in D:
				D[col] = 1
			else:
				df = df.drop([col], axis=1)
		df = df.add_prefix('_'.join(files.split('_')[0:3]) + '_')
		res = res.merge(df, left_index=True, right_index=True)
		print(files)

res.to_csv('geno_nonredundant.csv', index=True, header=True,sep=",")
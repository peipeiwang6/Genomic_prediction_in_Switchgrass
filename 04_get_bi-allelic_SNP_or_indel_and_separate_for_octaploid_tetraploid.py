'''
input1: classification file of variation
input2: file with ploidy of each individual
input3: genotype matrix
input4: indel or SNP
'''
import sys,os
import pandas as pd
type = open(sys.argv[1],'r').readlines()
ploidy = open(sys.argv[2],'r').readlines()
inp = open(sys.argv[3],'r').readlines()

P = {}
for inl in ploidy:
	tem = inl.split('\t')
	ind = tem[0]
	p = int(tem[2])
	P[ind] = p

D = {}	
for inl in type[1:]:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	type = tem[4]
	allelic = int(tem[5])
	if type == sys.argv[4] and allelic == 2:
		D[chr + '-' + pos] = 1

out = open(sys.argv[3].split('.txt')[0] + '_biallelic_%s.txt'%sys.argv[4],'w')
out.write(inp[0])
for inl in inp[1:]:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	if chr + '-' + pos in D:
		out.write(inl)

out.close()
		
df = pd.read_csv(sys.argv[3].split('.txt')[0] + '_biallelic_%s.txt'%sys.argv[4], sep='\t', index_col = 0, header = 0)
colname = df.columns.tolist()
df_4 = df.copy()
df_8 = df.copy()
for col in colname[3:]:
	if P[col] == 8:
		del df_4[col]
	if P[col] == 4:
		del df_8[col]
		
df_4.to_csv(sys.argv[3].split('.txt')[0] + '_biallelic_%s_tetraploid.txt'%sys.argv[4], index=True, header=True,sep="\t")
df_8.to_csv(sys.argv[3].split('.txt')[0] + '_biallelic_%s_octaploid.txt'%sys.argv[4], index=True, header=True,sep="\t")
'''
input1: exome biallelic genotype matrix in tetraploid
input2: GBS biallelic genotype matrix in tetraploid
input3: output file
'''
import sys,os
import pandas as pd
exome = open(sys.argv[1],'r')
inl = exome.readline()
title_exome = inl.strip().split('\t')

## save gbs with the same ID order as in exome matrix
df = pd.read_csv(sys.argv[2], sep='\t', index_col = 0, header = 0)
df2 = df.loc[:,title_exome[1:]]
df2.to_csv(sys.argv[2], index=True, header=True,sep="\t")

gbs = open(sys.argv[2],'r').readlines()
title_gbs = gbs[0].strip().split('\t')
for i in range(0,len(title_exome)):
	if title_exome[i] != title_gbs[i]:
		print(i)

E = {}
G = {}
D = {}
inl = exome.readline()
while inl:
	tem = inl.strip().split('\t')
	E[tem[0] + '_' + tem[1]] = 1
	inl = exome.readline()
	
for inl in gbs[1:]:
	tem = inl.strip().split('\t')
	G[tem[0] + '_' + tem[1]] = 1

for pos in E:
	if pos in G:
		D[pos] = 1

S = {} ### for share loci, save GBS one		
out = open(sys.argv[3],'w')
out.write(gbs[0])
for inl in gbs[1:]:
	tem = inl.strip().split('\t')
	pos = tem[0] + '_' + tem[1]
	if pos not in D:
		out.write(inl) ### if not shared, save
	else:
		if pos not in S:
			S[pos] = {}
		for i in range(4,len(tem)):
			S[pos][title_exome[i]] = tem[i]




exome = open(sys.argv[1],'r')
inl = exome.readline()
inl = exome.readline()
while inl:
	tem = inl.strip().split('\t')
	pos = tem[0] + '_' + tem[1]
	if pos not in D:
		out.write(inl) ### if not shared, save
	else:   ## if shared, save the hetero one
		if pos not in S:
			print(pos)
		else:
			for i in range(4,len(tem)):
				g = S[pos][title_exome[i]]
				if tem[i] != g and tem[i] != '%s/%s'%(g.split('/')[1],g.split('/')[0]):
					if g.split('/')[1] != g.split('/')[0] and tem[i] != './.':  ### GBS SNP is hetero
						tem[i] = g 
					if g.split('/')[1] == g.split('/')[0] and tem[i].split('/')[1] == tem[i].split('/')[0] and tem[i] != './.' and g != './.': ### both homo,but diff:
						tem[i] = '%s/%s'%(g.split('/')[0],tem[i].split('/')[0])	
					if tem[i] == './.':  ### if exome is missing
						tem[i] = g
			out.write('\t'.join(tem[0:]) + '\n')
	inl = exome.readline()

out.close()
	
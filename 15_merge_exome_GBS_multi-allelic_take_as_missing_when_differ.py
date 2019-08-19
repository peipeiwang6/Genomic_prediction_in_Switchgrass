'''
input1: exome multi-allelic variant matrix
input2: gbs multi-allelic variant matrix
input3: output file
'''
import sys,os
import pandas as pd
import numpy as np
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
	ref = tem[2]
	alt = tem[3]
	if pos not in D:
		out.write(inl) ### if not shared, save
	else:
		if pos not in S:
			S[pos] = {}
			S[pos]['ref_alt'] = [ref,alt]
		for i in range(4,len(tem)):
			S[pos][title_exome[i]] = tem[i]


exome = open(sys.argv[1],'r')
inl = exome.readline()
inl = exome.readline()
while inl:
	tem = inl.strip().split('\t')
	pos = tem[0] + '_' + tem[1]
	ref = tem[2]
	alt = tem[3]
	if pos not in D:
		out.write(inl) ### if not shared, save
	elif ref != S[pos]['ref_alt'][0]: ### if ref in exome and GBS are not the same, save exome info
		out.write(inl) 
	elif ref == S[pos]['ref_alt'][0] and alt != S[pos]['ref_alt'][1]: ### if the alt in exome and GBS are not the same, then take the union of two alt
		aa = alt.split(',')
		for bb in S[pos]['ref_alt'][1].split(','):
			aa.append(bb)
		alt = ','.join(np.unique(aa))
		tem[3] = alt
	if pos in D and ref == S[pos]['ref_alt'][0]:   ## if shared, save the hetero one
		if pos not in S:
			print(pos)
		else:
			for i in range(4,len(tem)):
				g = S[pos][title_exome[i]]
				if tem[i] == './.' or tem[i] == './././.': ### if exome is missing, take GBS one
					tem[i] = g
				elif g =='./.' or g == './././.': ### if gbs is missing, not change
					tem[i] = tem[i]
				elif len(np.unique(tem[i].split('/')))==1 and len(np.unique(g.split('/')))>1 and np.unique(tem[i].split('/'))[0] in g.split('/'): ### if exome is homo, while gbs is hetero
					tem[i] = g
				elif len(np.unique(g.split('/')))==1 and len(np.unique(tem[i].split('/')))>1 and np.unique(g.split('/'))[0] in tem[i].split('/'): ### if GBS is homo, while exome is hetero, not change
					tem[i] = tem[i]
				elif len(np.unique(tem[i].split('/')))==1 and len(np.unique(g.split('/')))==1 and np.unique(tem[i].split('/'))[0] != np.unique(g.split('/'))[0] and g != './.' and g!='./././.': ### if both homo, take hetero
					if len(tem[i].split('/')) == 2:
						tem[i] = '%s/%s'%(np.unique(tem[i].split('/'))[0],np.unique(g.split('/'))[0])
					if len(tem[i].split('/')) == 4:
						tem[i] = '%s/%s/%s/%s'%(np.unique(tem[i].split('/'))[0],np.unique(tem[i].split('/'))[0],np.unique(g.split('/'))[0],np.unique(g.split('/'))[0])
				else: ### if too complex, take as missing
					if len(tem[i].split('/')) == 2:
						tem[i] = './.'
					if len(tem[i].split('/')) == 4:
						tem[i] = './././.'
			out.write('\t'.join(tem[0:]) + '\n')
	inl = exome.readline()

out.close()
	
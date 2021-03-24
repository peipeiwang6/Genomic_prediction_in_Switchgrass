'''
imput1: exome capture, biallelic indel matrix
input2: exome capture, biallelic SNP matrix
input3: GBS, biallelic indel matrix
input4: GBS, biallelic SNP matrix
input5: allele count file for exome homozygous or heterozygous genotype
input6: allele count file for GBS homozygous or heterozygous genotype
input7: tetraploid or octaploid
'''
import sys,os
import numpy as np
exome_indel = open(sys.argv[1],'r').readlines()
exome_snp = open(sys.argv[2],'r').readlines()
gbs_indel = open(sys.argv[3],'r').readlines()
gbs_snp = open(sys.argv[4],'r').readlines()
EP = {} #EP[pos] = 1
for inl in exome_indel[1:]:
	tem = inl.split('\t')
	EP[tem[0] + '_' + tem[1]] = 1

for inl in exome_snp[1:]:
	tem = inl.split('\t')
	EP[tem[0] + '_' + tem[1]] = 1

S = {} #shared position, S[pos] = 1
for inl in gbs_indel[1:]:
	tem = inl.split('\t')
	if tem[0] + '_' + tem[1] in EP:
		S[tem[0] + '_' + tem[1]] = 1

for inl in gbs_snp[1:]:
	tem = inl.split('\t')
	if tem[0] + '_' + tem[1] in EP:
		S[tem[0] + '_' + tem[1]] = 1

E = {} # E[pos][ind] = A/T
G = {} # G[pos][ind] = A/T
EN = {} # EN[i] = ind
GN = {} # GN[i] = ind
IND = {} # IND[ind] = 1
tem = exome_indel[0].strip().split('\t')
for i in range(4,len(tem)):
	EN[i] = tem[i]
	IND[tem[i]] = 1

tem = gbs_indel[0].strip().split('\t')
for i in range(4,len(tem)):
	GN[i] = tem[i]

for inl in exome_indel[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		E[pos] = {}
		E[pos]['ref'] = tem[2]
		E[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			E[pos][EN[i]] = tem[i]
			
for inl in exome_snp[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		E[pos] = {}
		E[pos]['ref'] = tem[2]
		E[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			E[pos][EN[i]] = tem[i]
			
for inl in gbs_indel[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		G[pos] = {}
		G[pos]['ref'] = tem[2]
		G[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			G[pos][GN[i]] = tem[i]

for inl in gbs_snp[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		G[pos] = {}
		G[pos]['ref'] = tem[2]
		G[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			G[pos][GN[i]] = tem[i]

out = open('Biallelic_variation_%s_Exome_VS_GBS.txt'%sys.argv[7],'w')
Ind = sorted(IND.keys())
title = 'Chr\tPos\tRef\tAlt'
for ind in Ind:
	title = title + '\t' + ind

out.write(title + '\n')

for pos in S:
	res = pos.split('_')[0] + '\t' + pos.split('_')[1]
	if E[pos]['ref'] == G[pos]['ref']:
		res = res + '\t' + E[pos]['ref']
	else:
		res = res + '\t' + E[pos]['ref'] + '|' + G[pos]['ref']
	if E[pos]['alt'] == G[pos]['alt']:
		res = res + '\t' + E[pos]['alt']
	else:
		res = res + '\t' + E[pos]['alt'] + '|' + G[pos]['alt']
	for ind in Ind:
		if E[pos][ind] == G[pos][ind] or (E[pos][ind].split('/')[0] == G[pos][ind].split('/')[1] and E[pos][ind].split('/')[1] == G[pos][ind].split('/')[0]):
			res = res + '\t' + E[pos][ind]
		else:
			res = res + '\t' + E[pos][ind] + '|' + G[pos][ind]
	out.write(res + '\n')
	
out.close()

ori_exome_indel = open(sys.argv[1],'r').readlines()
ori_exome_snp = open(sys.argv[2],'r').readlines()
ori_gbs_indel = open(sys.argv[3],'r').readlines()
ori_gbs_snp = open(sys.argv[4],'r').readlines()
ori_out = open('Shared_Biallelic_variation_%s_original_Exome_VS_GBS.txt'%sys.argv[7],'w')
out = open('Distribution_of_discrepancy_Biallelic_variation_%s_between_exome_and_GBS.txt'%sys.argv[7],'w')
ori_out.write(title + '\n')
O_exome = {}
O_gbs = {}
EN = {} # EN[i] = ind
GN = {} # GN[i] = ind
tem = ori_exome_indel[0].strip().split('\t')
for i in range(4,len(tem)):
	EN[i] = tem[i]
	IND[tem[i]] = 1

tem = ori_gbs_indel[0].strip().split('\t')
for i in range(4,len(tem)):
	GN[i] = tem[i]


for inl in ori_exome_indel[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		O_exome[pos] = {}
		O_exome[pos]['ref'] = tem[2]
		O_exome[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			O_exome[pos][EN[i]] = tem[i]
			
for inl in ori_exome_snp[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		O_exome[pos] = {}
		O_exome[pos]['ref'] = tem[2]
		O_exome[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			O_exome[pos][EN[i]] = tem[i]
			
for inl in ori_gbs_indel[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		O_gbs[pos] = {}
		O_gbs[pos]['ref'] = tem[2]
		O_gbs[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			O_gbs[pos][GN[i]] = tem[i]
			
for inl in ori_gbs_snp[1:]:
	tem = inl.strip().split('\t')
	if tem[0] + '_' + tem[1] in S:
		pos = tem[0] + '_' + tem[1]
		O_gbs[pos] = {}
		O_gbs[pos]['ref'] = tem[2]
		O_gbs[pos]['alt'] = tem[3]
		for i in range(4,len(tem)):
			O_gbs[pos][GN[i]] = tem[i]

if sys.argv[7] == 'octaploid':			
	N1 = 0  ### Exome has variation, GBS is ./.
	N2 = 0  ### have same variation
	N3 = 0  ### Exome has heteo(AATT), GBS has homo
	N3_02 = 0  ### Exome has heteo(ATTT or AAAT), GBS has homo
	N3_03 = 0  ### Exome has heteo(ATTT or AAAT), GBS has hetero(AATT)
	N4 = 0  ### Exome is ./., GBS has variation
	N5 = 0  ### Exome has homo, GBS has heteo(AATT)
	N5_02 = 0  ### Exome has homo, GBS has heteo(ATTT or AAAT)
	N5_03 = 0  ### Exome has hetero(AATT), GBS has heteo(ATTT or AAAT)
	N5_04 = 0  ### Exome has hetero(ATTT), GBS has heteo(TTTA)
	N6 = 0  ### both are ./.
	N7 = 0	### both homo but different variation	
	out.write('Chr\tpos\tID\tExome_SNP\tGBS_SNP\tType\n')
	for pos in S:
		res = pos.split('_')[0] + '\t' + pos.split('_')[1]
		if O_exome[pos]['ref'] == O_gbs[pos]['ref']:
			res = res + '\t' + O_exome[pos]['ref']
		else:
			res = res + '\t' + O_exome[pos]['ref'] + '|' + O_gbs[pos]['ref']
			print(pos)
		if O_exome[pos]['alt'] == O_gbs[pos]['alt']:
			res = res + '\t' + O_exome[pos]['alt']
		else:
			res = res + '\t' + O_exome[pos]['alt'] + '|' + O_gbs[pos]['alt']
			print(pos)
		for ind in Ind:
			if O_exome[pos][ind] == O_gbs[pos][ind] or sorted(O_exome[pos][ind].split('/')) == sorted(O_gbs[pos][ind].split('/')):
				res = res + '\t' + O_exome[pos][ind]
			else:
				res = res + '\t' + O_exome[pos][ind] + '|' + O_gbs[pos][ind]
	### have same SNPs, AATT == TTAA, ATTT == TTTA
			if (O_exome[pos][ind] == O_gbs[pos][ind] or sorted(O_exome[pos][ind].split('/')) == sorted(O_gbs[pos][ind].split('/'))) and O_exome[pos][ind]!= './././.':
				N2 += 1
	### both are ./.
			elif O_exome[pos][ind] == O_gbs[pos][ind] and O_exome[pos][ind]== './././.':
				N6 += 1
	### Exome has SNPs, GBS is ./.
			elif O_exome[pos][ind] != './././.' and O_gbs[pos][ind] == './././.':
				N1 += 1
	### Exome is ./., GBS has SNPs
			elif O_exome[pos][ind] == './././.' and O_gbs[pos][ind] != './././.':
				N4 += 1
	### Exome has homo, GBS has hetero(AATT)
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 1 and len(np.unique(O_gbs[pos][ind].split('/'))) == 2 and O_exome[pos][ind]!= './.' and O_gbs[pos][ind].split('/')[1] != O_gbs[pos][ind].split('/')[2]:
				N5 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_homo_GBS_hetero_AATT\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has homo, GBS has hetero(ATTT or AAAT)
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 1 and len(np.unique(O_gbs[pos][ind].split('/'))) == 2 and O_exome[pos][ind]!= './.' and O_gbs[pos][ind].split('/')[1] == O_gbs[pos][ind].split('/')[2]:
				N5_02 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_homo_GBS_hetero_ATTT\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has AATT, GBS has hetero(ATTT or AAAT)
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 2 and len(np.unique(O_gbs[pos][ind].split('/'))) == 2 and O_gbs[pos][ind].split('/')[1] == O_gbs[pos][ind].split('/')[2] and O_exome[pos][ind].split('/')[1] != O_exome[pos][ind].split('/')[2]:
				N5_03 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_hetero_AATT_GBS_hetero_ATTT\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has ATTT, GBS has heteroTTTA
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 2 and len(np.unique(O_gbs[pos][ind].split('/'))) == 2 and O_gbs[pos][ind].split('/')[1] == O_gbs[pos][ind].split('/')[2] and O_exome[pos][ind].split('/')[1] == O_exome[pos][ind].split('/')[2] and sorted(O_exome[pos][ind].split('/')) != sorted(O_gbs[pos][ind].split('/')):
				N5_04 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_hetero_ATTT_GBS_hetero_AAAT\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has hetero(AATT), GBS has homo
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 2 and len(np.unique(O_gbs[pos][ind].split('/'))) == 1 and O_exome[pos][ind].split('/')[1] != O_exome[pos][ind].split('/')[2] and O_gbs[pos][ind] != './.':
				N3 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_hetero_AATT_GBS_homo\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has hetero(ATTT or AAAT), GBS has homo
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 2 and len(np.unique(O_gbs[pos][ind].split('/'))) == 1 and O_exome[pos][ind].split('/')[1] == O_exome[pos][ind].split('/')[2] and O_gbs[pos][ind] != './.':
				N3_02 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_hetero_ATTT_GBS_homo\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has hetero(ATTT or AAAT), GBS has hetero(AATT)
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 2 and len(np.unique(O_gbs[pos][ind].split('/'))) == 2 and O_exome[pos][ind].split('/')[1] == O_exome[pos][ind].split('/')[2] and O_gbs[pos][ind].split('/')[1] != O_gbs[pos][ind].split('/')[2] :
				N3_03 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_hetero_ATTT_GBS_hetero_AATT\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### both homo, but diff
			elif len(np.unique(O_exome[pos][ind].split('/'))) == 1 and len(np.unique(O_gbs[pos][ind].split('/'))) == 1 and O_exome[pos][ind]!=O_gbs[pos][ind] and O_exome[pos][ind] != './././.' and O_gbs[pos][ind]!= './././.':
				N7 += 1
				print([O_exome[pos][ind],O_gbs[pos][ind]])
				out.write('%s\t%s\t%s\t%s\t%s\tBoth_homo_differ\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
		ori_out.write(res + '\n')
		
	ori_out.close()
	out.close()
	print([N1,N2,N3,N3_02,N3_03,N4,N5,N5_02,N5_03,N5_04,N6,N7])

if sys.argv[7] == 'tetraploid':
	N1 = 0  ### Exome has SNPs, GBS is ./.
	N2 = 0  ### have same SNPs
	N3 = 0  ### Exome has heteo, GBS has homo
	N4 = 0  ### Exome is ./., GBS has SNPs
	N5 = 0  ### Exome has homo, GBS has heteo
	N6 = 0  ### both are ./.
	N7 = 0	### both homo but different SNPs	
	out.write('Chr\tpos\tID\tExome_SNP\tGBS_SNP\tType\n')
	for pos in S:
		res = pos.split('_')[0] + '\t' + pos.split('_')[1]
		if O_exome[pos]['ref'] == O_gbs[pos]['ref']:
			res = res + '\t' + O_exome[pos]['ref']
		else:
			res = res + '\t' + O_exome[pos]['ref'] + '|' + O_gbs[pos]['ref']
		if O_exome[pos]['alt'] == O_gbs[pos]['alt']:
			res = res + '\t' + O_exome[pos]['alt']
		else:
			res = res + '\t' + O_exome[pos]['alt'] + '|' + O_gbs[pos]['alt']
		for ind in Ind:
			if O_exome[pos][ind] == O_gbs[pos][ind] or (O_exome[pos][ind].split('/')[0] == O_gbs[pos][ind].split('/')[1] and O_exome[pos][ind].split('/')[1] == O_gbs[pos][ind].split('/')[0]):
				res = res + '\t' + O_exome[pos][ind]
			else:
				res = res + '\t' + O_exome[pos][ind] + '|' + O_gbs[pos][ind]
	### have same SNPs
			if (O_exome[pos][ind] == O_gbs[pos][ind] or (O_exome[pos][ind].split('/')[0] == O_gbs[pos][ind].split('/')[1] and O_exome[pos][ind].split('/')[1] == O_gbs[pos][ind].split('/')[0])) and O_exome[pos][ind]!= './.':
				N2 += 1
	### both are ./.
			elif O_exome[pos][ind] == O_gbs[pos][ind] and O_exome[pos][ind]== './.':
				N6 += 1
	### Exome has SNPs, GBS is ./.
			elif O_exome[pos][ind] != './.' and O_gbs[pos][ind] == './.':
				N1 += 1
	### Exome is ./., GBS has SNPs
			elif O_exome[pos][ind] == './.' and O_gbs[pos][ind] != './.':
				N4 += 1
	### Exome has homo, GBS has hetero
			elif O_exome[pos][ind].split('/')[0] == O_exome[pos][ind].split('/')[1] and O_exome[pos][ind]!= './.' and O_gbs[pos][ind].split('/')[0] != O_gbs[pos][ind].split('/')[1]:
				N5 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_homo_GBS_hetero\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
	### Exome has hetero, GBS has homo
			elif O_exome[pos][ind].split('/')[0] != O_exome[pos][ind].split('/')[1] and O_gbs[pos][ind].split('/')[0] == O_gbs[pos][ind].split('/')[1] and O_gbs[pos][ind] != './.':
				N3 += 1
				out.write('%s\t%s\t%s\t%s\t%s\tExome_hetero_GBS_homo\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
			else:
				N7 += 1
				print([O_exome[pos][ind],O_gbs[pos][ind]])
				out.write('%s\t%s\t%s\t%s\t%s\tBoth_homo_differ\n'%(pos.split('_')[0],pos.split('_')[1],ind,O_exome[pos][ind],O_gbs[pos][ind]))
		ori_out.write(res + '\n')
		
	ori_out.close()
	out.close()
	print([N1,N2,N3,N4,N5,N6,N7])

inp = open('Distribution_of_discrepancy_Biallelic_variation_%s_between_exome_and_GBS.txt'%sys.argv[7],'r').readlines()
out = open('Distribution_of_discrepancy_Biallelic_variation_%s_between_exome_and_GBS_alle_count.txt'%sys.argv[7],'w')
P = {}
for inl in inp[1:]:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	ind = tem[2]
	if chr not in P:
		P[chr] = {}
	if pos not in P[chr]:
		P[chr][pos] = {}
	if ind not in P[chr][pos]:
		P[chr][pos][ind] = [0,0,0,0]
		
Exome = open(sys.argv[5],'r')
inl = Exome.readline()
inl = Exome.readline()
while inl:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	ind = tem[2]
	if chr in P:
		if pos in P[chr]:
			if ind in P[chr][pos]:
				P[chr][pos][ind][0] = int(tem[6])
				P[chr][pos][ind][1] = int(tem[7])
	inl = Exome.readline()
		
GBS = open(sys.argv[6],'r')
inl = GBS.readline()
inl = GBS.readline()
while inl:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	ind = tem[2]
	if chr in P:
		if pos in P[chr]:
			if ind in P[chr][pos]:
				P[chr][pos][ind][2] = int(tem[6])
				P[chr][pos][ind][3] = int(tem[7])
	inl = GBS.readline()
		

out.write('Chr\tPos\tInd\tExome_SNP\tGBS_SNP\tType\tExome_alle_count\tExome_read_count\tGBS_alle_count\tGBS_read_count\n')
for inl in inp[1:]:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	ind = tem[2]
	if chr not in P:
		P[chr] = {}
	if pos not in P[chr]:
		P[chr][pos] = {}
	if ind not in P[chr][pos]:
		P[chr][pos][ind] = [0,0,0,0]
	out.write('%s\t%s\t%s\t%s\t%s\n'%(inl.strip(),P[chr][pos][ind][0],P[chr][pos][ind][1],P[chr][pos][ind][2],P[chr][pos][ind][3]))
	
out.close()

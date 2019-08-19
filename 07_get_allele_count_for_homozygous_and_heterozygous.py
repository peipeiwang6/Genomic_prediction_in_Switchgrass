'''
Get the allele count for biallelic homozygous and heterozygous variations
input1: genotype matrix
input2: variation classification file
input3: Exome or GBS
'''
import sys,os
snp = open(sys.argv[1],'r')
Class = open(sys.argv[2],'r').readlines()
out = open('%s_biallelic_alle_count_more_info.txt'%sys.argv[3],'w')
alle = open('%s_alle_count.txt'%sys.argv[3],'r')
P = {}  ### for pos of biallelic SNPs
for inl in Class[1:]:
	tem = inl.split('\t')
	if tem[5] == '2':
		if tem[0] not in P:
			P[tem[0]] = {}
		P[tem[0]][tem[1]] = {}
	
inl = alle.readline()
title = inl.strip().split('\t')
T_alle = {} ### alle frequency file title line
for i in range(5,len(title)):
	T_alle[i] = title[i]

F = {}	
inl = alle.readline()
while inl:
	tem = inl.strip().split('\t')
	chr = tem[0]
	pos = tem[1]
	ref = tem[2]
	alt = tem[3]
	if chr in P:
		if pos in P[chr]:
			for i in range(5,len(tem)):
				r = int(tem[i].split(',')[0].split(':')[1])
				a = int(tem[i].split(',')[1].split(':')[1])
				f = '%s/%s'%(r,r+a)
				P[chr][pos][T_alle[i]] = '%s\t%s\t%s'%(r,r+a,f)
	inl = alle.readline()


inl = snp.readline()
title = inl.strip().split('\t')
T_snp = {} ### snp file title line
for i in range(4,len(title)):
	T_snp[i] = title[i]

out.write('Chr\tPos\tInd\tPloidy\thomo_or_hetero\tType\tRef_count\tRead_count\tFrequency\n')
inl = snp.readline()
while inl:
	tem = inl.strip().split('\t')
	chr = tem[0]
	pos = tem[1]
	ref = tem[2]
	alt = tem[3]
	if chr in P:
		if pos in P[chr]:
			for i in range(4,len(tem)):
				if tem[i] == '%s/%s'%(ref,ref):
					out.write('%s\t%s\t%s\ttetraploid\thomo\tRR\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == '%s/%s'%(alt,alt):
					out.write('%s\t%s\t%s\ttetraploid\thomo\tAA\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == '%s/%s'%(ref,alt) or tem[i] == '%s/%s'%(alt,ref):
					out.write('%s\t%s\t%s\ttetraploid\thetero\tRA\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == './.':
					out.write('%s\t%s\t%s\ttetraploid\tmissing\t..\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == '%s/%s/%s/%s'%(ref,ref,ref,ref):
					out.write('%s\t%s\t%s\toctaploid\thomo\tRRRR\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == '%s/%s/%s/%s'%(alt,alt,alt,alt):
					out.write('%s\t%s\t%s\toctaploid\thomo\tAAAA\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == '%s/%s/%s/%s'%(ref,ref,alt,alt) or tem[i] == '%s/%s/%s/%s'%(alt,alt,ref,ref):
					out.write('%s\t%s\t%s\toctaploid\thetero\tRRAA\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == '%s/%s/%s/%s'%(ref,alt,alt,alt) or tem[i] == '%s/%s/%s/%s'%(alt,ref,ref,ref) or tem[i] == '%s/%s/%s/%s'%(alt,alt,alt,ref) or tem[i] == '%s/%s/%s/%s'%(ref,ref,ref,alt):
					out.write('%s\t%s\t%s\toctaploid\thetero\tRRRA\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				if tem[i] == './././.':
					out.write('%s\t%s\t%s\toctaploid\tmissing\t....\t%s\n'%(chr,pos,T_snp[i],P[chr][pos][T_snp[i]]))
				out.flush()
	inl = snp.readline()

out.close()
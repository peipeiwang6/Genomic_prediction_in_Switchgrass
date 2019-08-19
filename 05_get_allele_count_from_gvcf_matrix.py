'''
input1: genotype matrix
input2: dictionary for gvcf files
input3: Exome or GBS

'''
import sys,os
inp = open(sys.argv[1],'r')
dict = open(sys.argv[2],'r').readlines()
D = {}
for inl in dict:
	D[inl.strip().split('\t')[1]] = inl.split('\t')[0]

R = {}
inl = inp.readline()
inl = inp.readline()
while inl:
	tem = inl.split('\t')
	chr = tem[0]
	pos = tem[1]
	ref = tem[2]
	alt = tem[3]
	if chr not in R:
		R[chr] = {}
	R[chr][pos] = [ref,alt]
	inl = inp.readline()
	
for chr in R:	
	if chr.startswith('Chr'):
		file = D[chr]
	if chr.startswith('scaffold'):
		file = D['scaffold']
	dat = open(file,'r')
	inl = dat.readline()
	out = open('%s_alle_count_%s.txt'%(sys.argv[3],chr),'w')
	while inl:
		if inl.startswith('#CHROM'):
			tem = inl.strip().split('\t')[9:]
			out.write('Chr\tPos\tRef\tAlt\tQual\t%s\n'%'\t'.join(tem))
			out.flush()
		if not inl.startswith('#'):
			tem = inl.strip().split('\t')
			chr = tem[0]
			pos = tem[1]
			if chr in R:
				if pos in R[chr]:
					ref = tem[3]
					alt = tem[4].split(',')
					geno = tem[9:]
					res = '%s\t%s\t%s\t%s\t%s'%(chr,pos,ref,tem[4],tem[5])
					for g in geno:
						type = g.split(':')[0]
						type = type.replace('0',ref)
						if '1' in type:
							type = type.replace('1',alt[0])
						if '2' in type:
							type = type.replace('2',alt[1])
						if '3' in type:
							type = type.replace('3',alt[2])
						if '4' in type:
							type = type.replace('4',alt[3])
						if '5' in type:
							type = type.replace('5',alt[4])
						if '6' in type:
							type = type.replace('6',alt[5])
						if '7' in type:
							type = type.replace('7',alt[6])
						freq = g.split(':')[1]
						f = freq.split(',')
						alle_f = ''
						for j in range(0,len(f)):
							if j == 0:
								alle_f = '%s:%s'%(ref,f[j])
							else:
								alle_f = alle_f + ',' + '%s:%s'%(alt[j-1],f[j])
						res = res + '\t' + alle_f
					out.write(res + '\n')
					out.flush()
		inl = dat.readline()
	out.close()


import sys,os
inp = open(sys.argv[1],'r').readlines()
snp = open(sys.argv[1] + '_SNP','w')
indel = open(sys.argv[1] + '_indel','w')
snp.write(inp[0])
indel.write(inp[0])
D = {}
for inl in inp[1:]:
	tem = inl.split('\t')
	if '%s__%s'%(tem[0],tem[1]) not in D:
		D['%s__%s'%(tem[0],tem[1])] = 1
		if len(tem[3])==1 and len(tem[2])==1 and tem[3] != '*':
			snp.write(inl)
		else:
			indel.write(inl)
	else:
		print(inl)

snp.close()
indel.close()
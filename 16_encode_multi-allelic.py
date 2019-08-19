'''
input1: matrix with multi-allelic variants
'''

import sys,os
import numpy
inp = open(sys.argv[1],'r')
out = open(sys.argv[1] + '_encoding','w')
inl = inp.readline()
out.write(inl)
inl = inp.readline()
while inl:
	tem = inl.strip().split('\t')
	chr = tem[0]
	pos = tem[1]
	ref = tem[2]
	alt = tem[3]
	denominator = 2**len(alt.split(','))
	V = {}
	V[ref] = 0
	alternative = alt.split(',')
	for i in range(0,len(alternative)):
		V[alternative[i]] = 2**i
	for n in range(4,len(tem)):
		marker = tem[n]
		if marker == './.' or marker == './././.':
			tem[n] = 'NaN'
		else:
			if len(marker.split('/')) == 2:
				alle = marker.split('/')
				tem[n] = '%s'%(float(V[alle[0]] + V[alle[1]])/denominator)
			elif len(marker.split('/')) == 4:
				alle = marker.split('/')
				if len(numpy.unique(alle)) >= 3:
					print('%s\t%s\t%s'%(chr,pos,marker))
				tem[n] = '%s'%(float(V[alle[0]] + V[alle[1]] + V[alle[2]] + V[alle[3]])/(denominator*2))
	out.write('\t'.join(tem) + '\n')		
	inl = inp.readline()

out.close()
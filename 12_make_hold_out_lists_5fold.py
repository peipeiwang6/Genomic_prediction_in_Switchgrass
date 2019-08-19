'''
input1: pheno.csv
'''
import sys,os
import numpy as np
import random
inp = open(sys.argv[1],'r').readlines()[1:]
D = {}
for inl in inp:
	D[inl.split(',')[0]] = 1

for i in range(1,101):
	out = open('Holdout_%s.txt'%i,'w')
	holdout = np.random.choice(list(D.keys()), len(D)//5, replace=False)
	for ind in holdout:
		out.write('%s\n'%ind)
	out.close()

import sys,os
import numpy as np
import random
inp = open(sys.argv[1],'r').readlines()[1:]
D = {}
for inl in inp:
	D[inl.split(',')[0]] = 1

for i in range(1,2):
	out = open('Test.txt','w')
	holdout = np.random.choice(list(D.keys()), len(D)//6, replace=False)
	for ind in holdout:
		out.write('%s\n'%ind)
	out.close()

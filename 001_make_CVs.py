import sys, os
import pandas as pd
import numpy as np
import math
import random

file_name = sys.argv[1]

df = pd.read_csv(file_name, sep=',', header =0, index_col = 0)

cvs = pd.DataFrame(index = df.index)

n_lines = len(df)
n_reps = int((n_lines/5) + 1) #math.ceil
print(n_lines)

for i in range(1,101):
	name = 'cv_' + str(i)
	mix = np.repeat(range(1,6), n_reps)
	np.random.shuffle(mix)
	cvs[name] = mix[0:n_lines]

cvs.to_csv('CVFs.csv', sep=',')

import sys,os
import pickle
with open('/mnt/home/peipeiw/Documents/Genome_selection/Other_markers/Intermediate_files/Corresponding_marker_locus_for_multiallelic.pkl', 'rb') as f1:
	Corr = pickle.load(f1)


file = sys.argv[1]
marker = open(file,'r').readlines()
inp = open('/mnt/home/peipeiw/Documents/Genome_selection/Distribution_of_markers/Markers_distribution_all_markers_unique.txt','r').readlines()
D = {}
for inl in inp:
	tem = inl.strip().split('\t')
	D[tem[9]] = tem[2]

R = {}
out = open('Genes_closest_to_%s'%file,'w')
for inl in marker:
	tem = inl.strip().split('_')
	if 'scaffold' not in inl:
		m = '_'.join(tem[3:5])
		m2 = '_'.join(tem[3:])
		if m in D:
			if D[m] not in R:
				R[D[m]] = 1
				out.write(D[m] + '\n')
		else:
			m = '_'.join(Corr[m2].split('_')[0:2])
			if D[m] not in R:
				R[D[m]] = 1
				out.write(D[m] + '\n')
	else:
		m = '_'.join(tem[3:6])
		m2 = '_'.join(tem[3:])
		if m in D:
			if D[m] not in R:
				R[D[m]] = 1
				out.write(D[m] + '\n')
		else:
			m = '_'.join(Corr[m2].split('_')[0:3])
			if D[m] not in R:
				R[D[m]] = 1
				out.write(D[m] + '\n')

out.close()

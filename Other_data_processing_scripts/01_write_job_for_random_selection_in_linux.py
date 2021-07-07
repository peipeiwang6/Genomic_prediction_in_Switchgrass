import sys,os
for num in range(250,40250,250):
	out = open('Random_selection_%s.sh'%num,'w')
	out.write('#!/bin/sh --login\n#SBATCH --time=1:00:00\n#SBATCH --ntasks=1\n#SBATCH --cpus-per-task=1\n#SBATCH --mem=40G\n#SBATCH --job-name Random_selection_%s.sh\n#SBATCH -e Random_selection_%s.sh.e\n#SBATCH -o Random_selection_%s.sh.o\ncd /mnt/home/peipeiw/Documents/Genome_selection/CV/All_markers/\n'%(num,num,num))
	if num <= 10000:
		out.write("columns=1,$( for (( ii=2; ii<=2566743; ii++ )); do echo $ii; done | sort -R | head -%s | sort -n | tr '\\n' ',' | sed 's/,$//' )\n"%(num+1))
		out.write("cut --fields=${columns} All_markers.csv -d ',' > Random_%s_markers.csv\n"%(num))
	if num > 10000 and num <= 20000:
		out.write("columns=1,$( for (( ii=2; ii<=2566743; ii++ )); do echo $ii; done | sort -R | head -%s | sort -n | tr '\\n' ',' | sed 's/,$//' )\n"%(num+1))
		out.write("columns1=1,$(echo $columns | cut -d ',' -f2-10000 | tr '\\n' ',' | sed 's/,$//')\n")
		out.write("columns2=10001,$(echo $columns | cut -d ',' -f10002-%s | tr '\\n' ',' | sed 's/,$//')\n"%(num + 1))
		out.write("cut --fields=${columns1} All_markers.csv -d ',' > Random_%s_markers_1.tem\n"%num)
		out.write("cut --fields=${columns2} All_markers.csv -d ',' > Random_%s_markers_2.tem\n"%num)
		out.write("paste Random_%s_markers_1.tem Random_%s_markers_2.tem  -d ',' > Random_%s_markers.csv\n"%(num,num,num))
		out.write("rm Random_%s_markers_1.tem Random_%s_markers_2.tem\n"%(num,num))
	if num > 20000 and num <= 30000:
		out.write("columns=1,$( for (( ii=2; ii<=2566743; ii++ )); do echo $ii; done | sort -R | head -%s | sort -n | tr '\\n' ',' | sed 's/,$//' )\n"%(num+1))
		out.write("columns1=1,$(echo $columns | cut -d ',' -f2-10000 | tr '\\n' ',' | sed 's/,$//')\n")
		out.write("columns2=10001,$(echo $columns | cut -d ',' -f10002-20000 | tr '\\n' ',' | sed 's/,$//')\n")
		out.write("columns3=20001,$(echo $columns | cut -d ',' -f20002-%s | tr '\\n' ',' | sed 's/,$//')\n"%(num + 1))
		out.write("cut --fields=${columns1} All_markers.csv -d ',' > Random_%s_markers_1.tem\n"%num)
		out.write("cut --fields=${columns2} All_markers.csv -d ',' > Random_%s_markers_2.tem\n"%num)
		out.write("cut --fields=${columns3} All_markers.csv -d ',' > Random_%s_markers_3.tem\n"%num)
		out.write("paste Random_%s_markers_1.tem Random_%s_markers_2.tem Random_%s_markers_3.tem  -d ',' > Random_%s_markers.csv\n"%(num,num,num,num))
		out.write("rm Random_%s_markers_1.tem Random_%s_markers_2.tem Random_%s_markers_3.tem\n"%(num,num,num))
	if num > 30000 and num <= 40000:
		out.write("columns=1,$( for (( ii=2; ii<=2566743; ii++ )); do echo $ii; done | sort -R | head -%s | sort -n | tr '\\n' ',' | sed 's/,$//' )\n"%(num+1))
		out.write("columns1=1,$(echo $columns | cut -d ',' -f2-10000 | tr '\\n' ',' | sed 's/,$//')\n")
		out.write("columns2=10001,$(echo $columns | cut -d ',' -f10002-20000 | tr '\\n' ',' | sed 's/,$//')\n")
		out.write("columns3=20001,$(echo $columns | cut -d ',' -f20002-30000 | tr '\\n' ',' | sed 's/,$//')\n")
		out.write("columns4=30001,$(echo $columns | cut -d ',' -f30002-%s | tr '\\n' ',' | sed 's/,$//')\n"%(num + 1))
		out.write("cut --fields=${columns1} All_markers.csv -d ',' > Random_%s_markers_1.tem\n"%num)
		out.write("cut --fields=${columns2} All_markers.csv -d ',' > Random_%s_markers_2.tem\n"%num)
		out.write("cut --fields=${columns3} All_markers.csv -d ',' > Random_%s_markers_3.tem\n"%num)
		out.write("cut --fields=${columns4} All_markers.csv -d ',' > Random_%s_markers_4.tem\n"%num)
		out.write("paste Random_%s_markers_1.tem Random_%s_markers_2.tem Random_%s_markers_3.tem Random_%s_markers_4.tem  -d ',' > Random_%s_markers.csv\n"%(num,num,num,num,num))
		out.write("#rm Random_%s_markers_1.tem Random_%s_markers_2.tem Random_%s_markers_3.tem Random_%s_markers_4.tem\n"%(num,num,num,num))
	out.close()


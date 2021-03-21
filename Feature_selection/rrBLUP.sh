#!/bin/sh --login

#SBATCH --time=4:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=20G
#SBATCH --job-name rrBLUP.sh
#SBATCH -e rrBLUP.sh.e
#SBATCH -o rrBLUP.sh.o
cd /mnt/home/peipeiw/Documents/Genome_selection/CV/Both_ploidy_bi_SNP_GBS_v5_FS_Anthesis_Date_8632/

module load R
module load Python/3.6.4
# get the training set
python 01_holdout_test_stratified.py pheno.csv Anthesis_Date_8632
Rscript 02_split_geno_pheno.r geno.csv pheno.csv Test.txt 
python ../../001_make_CVs.py pheno_training.csv
Rscript ../../000_rrBLUP.r geno_training.csv pheno_training.csv all Anthesis_Date_8632 Training_Anthesis_Date_8632
# do the feature selection based on training models
python 05_FS_based_on_genes.py
# report the cv and test performance using selected features
Rscript 000_rrBLUP_FS.r geno.csv pheno.csv all Anthesis_Date_8632 Test.txt Training_test_all_marker_Anthesis_Date_8632
Rscript 000_rrBLUP_FS.r geno.csv pheno.csv Markers_first_for_each_gene_GBS_Anthesis_Date_8632.txt Anthesis_Date_8632 Test.txt Training_test_first_for_each_gene_Anthesis_Date_8632
Rscript 000_rrBLUP_FS.r geno.csv pheno.csv Markers_top4000_genes_GBS_Anthesis_Date_8632.txt Anthesis_Date_8632 Test.txt Training_test_top4000_genes_Anthesis_Date_8632

#Rscript ../../000_rrBLUP.r geno.csv pheno.csv Markers_first_for_each_gene_GBS_Anthesis_Date_8632.txt Anthesis_Date_8632 FS_first_for_each_gene_Anthesis_Date_8632
#Rscript ../../000_rrBLUP.r geno.csv pheno.csv Markers_top4000_genes_GBS_Anthesis_Date_8632.txt Anthesis_Date_8632 FS_top4000_genes_Anthesis_Date_8632
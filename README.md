# Genomic_prediction_in_Switchgrass

## Pre-processing

> 1. convert vcf file to genetic matrix
 - python 01_conver_genotype_gvcf_to_genotype_matrix.py -file your_vcf
 
> 2. filter the genotype matrix
 - python 02_filter_genotype_matrix_MAF_missing_data.py -file genotype_matrix
 
> 3. classify the variation into SNP, indel, or SNP/indel; biallelic or non-biallelic; in genic or intergenic, three_UTR or five_UTR region, exonic or intronic, splicing regions
** Note that, this script is for switchgrass specifically. For other species, be careful about the gff format and the how the gene names are encoded**
 - python 03_classify_variations.py -file genotype_matrix_filtered -gff gff_file

> 4. extract the biallelic SNPs or indels
 - python 04_get_bi-allelic_SNP_or_indel.py -classification marker_classification -file genotype_matrix_filtered -type SNP_or_indel

** Note that if you only want to get the biallelic SNPs or indels, rather than the classification of markers to genic, intergenic, etc, please skip step 3 and 4, and try the script below:**
 - python 03_get_biallelic_markers_directly.py -file 1011Matrix_genotype_matrix.txt_filtered -type SNP
 
> 5. convert the genotype matrix to the fastPHASE format
 - python 05_convert_genotype_matrix_to_fastPHASE_format.py -file 1011Matrix_genotype_matrix.txt_filtered_biallelic_SNP.txt
 
> 6. download and install the fastPHASE (http://scheet.org/software.html or copy from /mnt/home/peipeiw/Documents/Genome_selection/fastPHASE/phase.2.1.1.linux.tar)
./fastPHASE -T10 -oName_for_output 1011Matrix_genotype_matrix.txt_filtered_biallelic_SNP.txt_fastPHASE.txt

> 7. convert the imputed genotype matrix back to the format used previously
 - python 06_convert_imputed_biallelic_variation_to_genotype.py -matrix 1011Matrix_genotype_matrix.txt_filtered_biallelic_SNP.txt -imputed_matrix Name_for_output_hapguess_switch.out
 
 


# Genomic_prediction_in_Switchgrass

## Pre-processing

> 1. convert vcf file to genetic matrix
 - python 01_conver_genotype_gvcf_to_genotype_matrix.py -file your_vcf
 
> 2. filter the genotype matrix
 - python 02_filter_genotype_matrix_MAF_missing_data.py -file genotype_matrix
 
> 3. classify the variation into SNP, indel, or SNP/indel; biallelic or non-biallelic; in genic or intergenic, three_UTR or five_UTR region, exonic or intronic, splicing regions
 - python 03_classify_variations.py -file genotype_matrix_filtered -gff gff_file
 
> 4. extract the biallelic SNPs or indels
 - python 04_get_bi-allelic_SNP_or_indel.py -classification marker_classification -file genotype_matrix_filtered -type SNP_or_indel
 
 


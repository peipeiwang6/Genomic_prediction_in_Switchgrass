library(rrBLUP)
library(data.table)
args = commandArgs(trailingOnly=TRUE)
number <- as.numeric(args[1])
total_number <- as.numeric(args[2]) + 1
for(i in 1:100){
	dir.create(paste('Subset_',i,sep=''))
	file.copy(c('CVFs.csv','pheno.csv'),paste('Subset_',i,sep=''))
	setwd(paste('Subset_',i,sep=''))
	geno <- fread('../geno.csv',select=c(1,sample(seq(2,total_number),number,replace = FALSE)))
	fwrite(geno,'geno.csv',sep = ",",quote=FALSE)
	setwd('../')
	}


library(rrBLUP)
args = commandArgs(trailingOnly=TRUE)
X_file <- args[1]
Y_file <- args[2]
number <- as.numeric(args[3])
X <- read.csv(X_file, row.names=1) 
Y <- read.csv(Y_file, row.names=1) 
for(i in 1:100){
	dir.create(paste('Subset_',i,sep=''))
	file.copy(c('CVFs.csv','pheno.csv'),paste('Subset_',i,sep=''))
	setwd(paste('Subset_',i,sep=''))
	geno <- X[,sample(seq(1,ncol(X)),number,replace = FALSE)]
	write.csv(geno,'geno.csv',row.names=T,quote=F)
	setwd('../')
	}




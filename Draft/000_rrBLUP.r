library(rrBLUP)
set.seed(42)
args = commandArgs(trailingOnly=TRUE)
X_file <- args[1]
Y_file <- args[2]
feat_file <- args[3]
trait <- args[4]
save_name <- args[5]

Y <- read.csv(Y_file, row.names=1) 
X <- read.csv(X_file, row.names=1) 
# make X and Y have the same order of rows
X <- X[rownames(Y),]
cvs <- read.csv('CVFs.csv', row.names=1)
# Make the relationship matrix from the markers
M=tcrossprod(scale(X))  # centered and scaled XX'
M=M/mean(diag(M))
rownames(M) <- 1:nrow(X)

# Subset X if feat_file is not all
if (feat_file != 'all'){
  print('Pulling features to use...')
  FEAT <- scan(feat_file, what='character')
  X <- X[FEAT]
  feat_method <- tail(unlist(strsplit(feat_file, '/')), n=1)
}

if (trait == 'all') {
  print('Modeling all traits')
} else {
  Y <- Y[trait]
}

R2 <- c()
for(i in 1:length(Y)){
	print(names(Y)[i])
	Accuracy <- c()
	Coef <- c()
	for(k in 1:10){
		print(k)
		tst = cvs[,k]
		Coeff <- c()
		yhat <- data.frame(cbind(Y, yhat = 0))
		yhat$yhat <- as.numeric(yhat$yhat)
		row.names(yhat) <- row.names(Y)
		for(j in 1:5){
			validation <- which(tst==j)
			training <- which(tst!=j)
			yNA <- Y[,i]
			yNA[validation] <- NA # Mask yields for validation set
			# Build rrBLUP model and save yhat for the masked values
			#rrblup <- kin.blup(df,K=M,geno="gid",pheno='y') #optional parameters: fixed effects, gaussian kernel, covariates
			# predict marker effects
			coeff <- mixed.solve(y=Y[training,i], Z=X[training,], K=NULL, method='ML', SE=FALSE, return.Hinv=FALSE)
			Coeff <- rbind(Coeff,coeff$u)
			# predict breeding 
			rrblup <- mixed.solve(y=yNA, K=A.mat(X))
			yhat$yhat[validation] <- rrblup$u[validation]
			}
		accuracy <- cor(yhat[,i], yhat$yhat)
		Accuracy <- c(Accuracy,accuracy^2)
		Coef <- rbind(Coef,colMeans(Coeff))
		}
	R2 <- cbind(R2,Accuracy)
	write.csv(Coef,paste('Coef_',save_name,'_',names(Y)[i],'.csv',sep=''),row.names=F,quote=F)
	}
colnames(R2) <- names(Y)
write.csv(R2,paste('R2_results_',save_name,'.csv',sep=''),row.names=F,quote=F)
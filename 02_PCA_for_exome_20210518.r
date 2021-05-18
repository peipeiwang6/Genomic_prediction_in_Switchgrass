library(data.table)
X <- as.matrix(fread('geno.csv'),rownames=1)
X_tem <- c()
col_names <- c()
for(i in 1:ncol(X)){
	if(length(unique(X[,i:i])) > 1){
		X_tem <- cbind(X_tem,as.matrix(X[,i:i]))
		col_names <- c(col_names,colnames(X)[i])
		}
	else{
		print(i)
		}
	if(i%%1000 == 0){
		print(i)
		}
	}
rownames(X_tem) <- rownames(X)
colnames(X_tem) <- col_names
X = X_tem	

X2=scale(X) # Centers (subtract the column means) and Scales (dividing the centered columns by their stdev)
G=tcrossprod(X2) # Take the cross product X transpose
G=G/mean(diag(G))
EVD=eigen(G)
rownames(EVD$vectors)=rownames(G)
save(EVD,file='EVD.RData')
write.csv(EVD$vectors,"PCA_matrix_test.csv",row.names=T,quote=F)
write.csv(EVD$vectors[,1:5],"PCA5_geno_test.csv",row.names=T,quote=F)


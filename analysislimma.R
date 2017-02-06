library(limma)
raw.data <- read.delim("INPUT-QuantileNormalizedLog2Transformed-RPKM-Data.txt")
attach(raw.data)
names(raw.data)
d <- raw.data[, 2:5]
rownames(d) <- raw.data[, 1]
##To design matrix---
Group<-factor(pheno$Status,levels=levels(pheno$Status))
design<-model.matrix(~0+Group)  
###Assigning colnames###
colnames(design)<-c("Control", "Tumor")
###To assign the designed matrix in linear model using limma
fit <-lmFit(eset,design)
###Designing contrast matrix#
cont.wt<-makeContrasts("Tumor-Control",levels=design)
fit2 <-contrasts.fit(fit,cont.wt)
## eBayes step for calculating p-values, fold change etc###
fit3<-eBayes(fit

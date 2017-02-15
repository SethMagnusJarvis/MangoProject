#load libraries
library("limma")
library("Biobase")

#correctly load the data as a matrix
#load data
data <- as.matrix(read.csv("CSV/DataSet(1).csv"))
#produce a list of ascession numbers
list <- data[,1]
#turn the data into a data matrix
data <- data.matrix(read.csv("CSV/DataSet(1).csv"))
#add ascession numbers as row names
row.names(data) <- list
#remove weird random column which I think is a numerical interpretation of the Ascession code
data <- data[,-1]
#add sample names as col names
colnames(data)<-c("G1S1", "G1S2", "G1S3","GS1", "G2S2", "G2S3","G3S1", "G3S2", "G3S3")
#log the matrix
logdata <- log2(data)

#produce a model matrix, setting 3 sample groups and naming them
design <- model.matrix(~ 0+factor(c(1,1,1,2,2,2,3,3,3)))
colnames(design) <- c("Uninfected", "EightHours", "OneDay")

#produce an expression set from the matrix
eset <- ExpressionSet(assayData=logdata)

#Produces a linear model
fit <- lmFit(eset, design)

#creates the contrast matrix then looks for emperical Bayes method to examine variance
contrast.matrix <- makeContrasts(EightHours-Uninfected, OneDay-Uninfected, OneDay-EightHours, levels=design)
fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)

#produce a matrix of the top differentially expressed genes and output them to files
#Uninfected vs 8 hours
U8TT <- topTable(fit2, coef=1, adjust="BH")
U8TT <- U8TT[,c(1,3,4,5)]
write.table(U8TT, file='ROutput/U8TT.tsv', quote=FALSE, sep='\t')


#Uninfected vs 24 hours
U24TT <- topTable(fit2, coef=2, adjust="BH")
U24TT <- U24TT[,c(1,3,4,5)]
write.table(U24TT, file='ROutput/U24TT.tsv', quote=FALSE, sep='\t')

#8 Hours vs 24 hours
infectedTT <- topTable(fit2, coef=1, adjust="BH")
infectedTT <- infectedTT[,c(1,3,4,5)]
write.table(infectedTT, file='ROutput/infectedTT.tsv', quote=FALSE, sep='\t')

#produce plots and output as png files
#pca plot
pc = prcomp(t(exprs(eset)))
png('ROutput/PCA.png')
plot( pc$x[ , 1:2 ])
text(pc$x[,1:2], colnames(data), pos = 4)
dev.off()

#heatmap of top 100 genes
png('ROutput/Top100Heat.png')
heatmap(exprs(eset[1:100,]))
dev.off()

#Prouce volcano pot of the fited model
png('ROutput/VolcanoPlot.png')
volcanoplot(fit2)
dev.off()

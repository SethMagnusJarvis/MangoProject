library(limma)
library(Glimma)

???# read the data
raw.data<-read.csv("DataSet.csv")
f<-factor(targets2$f,levels = c("G1S1","G1S2","G1S3","G2S2","G2S3","G3S1","G3S2","G3S3"))


???# create design matrix
data <- as.matrix(read.csv("CSV/DataSet.csv"))
list <- data[,1]
data <- data.matrix(read.csv("DataSet.csv"))
row.names(data) <- list
data <- data[,-1]
logdata <- log2(data)


???# Fit the linear model
fit <- lmFit(eset, design)

???# Define a contrast matrix
cont.matrix <- makeContrasts(E10="present10-absent10",E48="present48-absent48",Time="absent48-absent10",levels=design)
fit2  <- contrasts.fit(fit, cont.matrix)
fit2  <- eBayes(fit2)

???# Assessing differiental expression
topTable(fit2,coef=1)

???# the most statistically signifcant genes
> genes=geneNames(brainBatch)
> topTable(efit.contrast,coef=1,adjust.method="BY",n=10,p.value=1e-5,genelist=genes)

???# For a quick look at differential expression levels, the number of significantly up- and down-regulated genes can be summarised in a table
summary(decideTests(efit))

???# Make a basic venn diagram
vennDiagram(dt[,1:2], circle.col=c("G1S1", "G2S3"))

???# Make a basic volcano plot
(toptable, plot(logFC, -log10(P.Value), pch=20, main="Volcano plot",xlim = c(-1,1)))

???# Make a basic pca plot
Xpca <- prcomp(t(X[topGenesIndx, ]), scale= TRUE)

???# A heatmap is created for the top 100 DE genes (as ranked by adjusted p-value) from th G1S1s LP contrast using the heatmap.2 function from the gplots package. The heatmap correctly clusters samples 
library(gplots)
G1S1.lp.topgenes <- G2S2.vs.lp$ENTREZID[1:100]
i <- which(v$genes$ENTREZID %in% G2S2.vs.lp.topgenes)
mycol <- colorpanel(1000,"blue","white","red")
heatmap.2(v$E[i,], scale="row",
          labRow=v$genes$SYMBOL[i], labCol=group, 
          col=mycol, trace="none", density.info="none", 
          margin=c(8,6), lhei=c(2,10), dendrogram="column")
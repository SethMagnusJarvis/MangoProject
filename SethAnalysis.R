
data <- as.matrix(read.csv("CSV/DataSet.csv"))
list <- data[,1]
data <- data.matrix(read.csv("DataSet.csv"))
row.names(data) <- list
data <- data[,-1]
logdata <- log2(data)
logdata

ExpSet <- ExpressionSet(assayData=logdata)



pca <- prcomp(logdata, centre=TRUE, scale.=TRUE)
pca
plot(pca, type = "l")

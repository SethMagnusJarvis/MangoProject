library("limma")
library("ggplot2")

setwd(getwd())

#load data
data <- as.matrix(read.csv("CSV/DataSet.csv"))

#produce a list of ascession numbers
list <- data[,1]

#turn the data into a data matrix
data <- data.matrix(read.csv("CSV/DataSet.csv"))

#add ascession numbers as row names
row.names(data) <- list

#remove weird random column which I think is a numerical interpretation of the Ascession code
data <- data[,-1]

#log the matrix
logdata <- log2(data)

#produce a model matrix
design <- model.matrix(~ 0+factor(c(1,1,1,2,2,2,3,3,3)))
colnames(design) <- c("Uninfected", "EightHours", "OneDay")


#produce an expression set from the data
eset <- ExpressionSet(assayData=logdata)

#Produces a linear model
fit <- lmFit(eset, design)

contrast.matrix <- makeContrasts(EightHours-Uninfected, OneDay-Uninfected, OneDay-EightHours, levels=design)
fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)

#produce a matrix of the top differentially expressed genes
#Uninfected vs 8 hours
topTable(fit2, coef=1, adjust="BH")

#Uninfected vs 24 hours
topTable(fit2, coef=2, adjust="BH")

#8 Hours vs 24 hours
topTable(fit2, coef=1, adjust="BH")

results <- decideTests(fit2)

vennDiagram(results)

plot(eset)


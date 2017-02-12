library("limma")

setwd("D:/MangoProject/PlayData")

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
group <- factor(c(1,1,1,2,2,2,3,3,3))

#currently looking at using http://genomicsclass.github.io/book/pages/expressing_design_formula.html for help

#produce an expression set from the data
ExpSet <- ExpressionSet(assayData=logdata)

#doesn't work, says "Error in NCOL(y) : argument "y" is missing, with no default"
lm <- lm.fit(ExpSet)

#currently useless, prooduces something which isn't any good
pca <- prcomp(logdata, centre=TRUE, scale.=TRUE)
pca
plot(pca, type = "l")

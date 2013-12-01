read.csv(file.choose(),header=TRUE) -> data
cor_data <- cor(data)
var <- ccf(data$V2, data$V4, plot = FALSE) # got to do for every feature
plot(var,type='l',main="NASDAQ vs some feature") 
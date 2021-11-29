library(ggplot2)

data <- (read.csv("../data/models.csv"))


ggplot(data, aes(x=mutation_rate, y=mutation_change)) + geom_jitter(aes(color=generations, size=error)) 

## ggplot(data, aes(x=generations, y=error)) + geom_jitter()

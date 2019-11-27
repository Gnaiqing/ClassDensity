# This is the basic framework for ClassSpamFilter
import jieba
import jieba.analyse

# get keywords of class theme
# e.g. keywords = ["贝叶斯","向量"]
keywords = ...

# get input sentences of tapescripts
# e.g. sentences = ["这是一个句子","那是一个句子"]
sentences = ...

# calculate the importance of each sentence
# e.g. sentence_scores = [3.2,5.1]
sentence_scores = ...

# display the result in various ways

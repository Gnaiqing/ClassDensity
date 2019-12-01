# This is the basic framework for ClassSpamFilter
import jieba
import jieba.analyse

# get keywords of class theme
def extract_keywords(topK_for_textbook=8, topK_for_blog=4):
    jieba.analyse.set_stop_words('stopwords.txt')
    textbook = open('textbook.txt', 'r', encoding='gbk')
    lines = textbook.readlines()
    keywords = dict()
    for line in lines:
        line = line.strip()
        extracted = jieba.analyse.extract_tags(sentence=line, topK=topK_for_textbook)
        for i in extracted:
            if i in keywords.keys():
                keywords[i] += 1
            else:
                keywords[i] = 1
    #print(keywords)
    keywords = dict(sorted(keywords.items(), key=lambda x:x[1], reverse=True))
    #print(keywords)

    blog = open('blog.txt', 'r', encoding='gbk')
    lines = blog.readlines()
    for line in lines:
        line = line.strip()
        extracted = jieba.analyse.extract_tags(sentence=line, topK=topK_for_blog)
        for i in extracted:
            if i in keywords.keys():
                keywords[i] += 1
            else:
                keywords[i] = 1
    #print(keywords)
    keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True))
    #print(keywords)
    
# e.g. keywords = {'文档': 10, '文本': 10, '聚类': 10}, the value is the extracted frequency of the keywords, which can be interpreted as importance
keywords = extract_keywords(topK_for_textbook=8, topK_for_blog=4)

# get input sentences of tapescripts
# e.g. sentences = ["这是一个句子","那是一个句子"]
sentences = ...

# calculate the importance of each sentence
# e.g. sentence_scores = [3.2,5.1]
sentence_scores = ...

# display the result in various ways

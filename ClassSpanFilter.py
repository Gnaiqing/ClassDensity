# This is the basic framework for ClassSpamFilter
import jieba
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re

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
    
    return keywords
    
# e.g. keywords = {'文档': 10, '文本': 10, '聚类': 10}, the value is the extracted frequency of the keywords, which can be interpreted as importance
keywords = extract_keywords(topK_for_textbook=8, topK_for_blog=4)

# get input sentences of tapescripts
# e.g. sentences = ["这是一个句子。","那是一个句子。"]
paragraph = "生活对我们KNN来说都不容易！我们必须努力，最重要的是我们必须相信K-Means。 \
我们必须相信，我们每个KNN都能够做得很好，而且，当我们发现这是什么时，我们必须努力工作，直到我们成功。"
tmp_sents = re.split('(。|！|\!|\.|？|\?)',paragraph)
sentences = []
sentence_num = int(len(tmp_sents)/2)
for i in range(sentence_num):
    sent = tmp_sents[2*i] + tmp_sents[2*i+1]
    sentences.append(sent)
print(sentences)

# retrieve corpus from sentences.
corpus = []
for i in range(sentence_num):
    words_list = jieba.cut(sentences[i])
    words = ""
    for item in words_list:
        words = words + item + " "
    corpus.append(words)
print(corpus)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

# get all words appeared in corpus
word = vectorizer.get_feature_names()
word_num = len(word)
print(word)
# get words appeared in keywords
keywords_index = []
for j in range(word_num):
    if word[j] in keywords:
        keywords_index.append(j)
appeared_keywords_num = len(keywords_index)

# get term frequency of each word at each sentence
counts = X.toarray()
print(counts)

# get tf-idf value of each word at each sentence
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)
tfidf_array = tfidf.toarray()
print(tfidf_array)


# calculate the importance of each sentence
# e.g. sentence_scores = [3.2,5.1]
sentence_scores = []
for i in range(sentence_num):
    score = 0
    for j in range(appeared_keywords_num):
        score = score + tfidf_array[i][keywords_index[j]]
    sentence_scores.append(score)
print(sentence_scores)

# display the result in various ways

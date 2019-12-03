# This is the basic framework for ClassSpamFilter
import jieba
import math
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
    # print(keywords)
    keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True))
    # print(keywords)

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
    # print(keywords)
    keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True))
    # print(keywords)

    return keywords


# e.g. keywords = {'文档': 10, '文本': 10, '聚类': 10}, the value is the extracted frequency of the keywords, which can be interpreted as importance
keywords = extract_keywords(topK_for_textbook=8, topK_for_blog=4)
keywords_list = []
for k, v in keywords.items():
    keywords_list.append(k.lower())
print("keywords_list:", keywords_list)

# get input sentences of tapescripts
# e.g. sentences = ["这是一个句子。","那是一个句子。"]
# paragraph = "生活对我们KNN来说都不容易！我们必须努力，最重要的是我们必须相信K-Means。 \
# 我们必须相信，我们每个KNN都能够做得很好，而且，当我们发现这是什么时，我们必须努力工作，直到我们成功。"
f = open("record.txt", "r", encoding="UTF-8")
paragraph = f.read()
tmp_sents = re.split('(。|！|\!|\.|？|\?)', paragraph)
sentences = []
sentence_num = int(len(tmp_sents) / 2)
for i in range(sentence_num):
    sent = tmp_sents[2 * i] + tmp_sents[2 * i + 1]
    sentences.append(sent)
# print("sentences:", sentences)

# retrieve corpus from sentences.
corpus = []
for i in range(sentence_num):
    words_list = jieba.cut(sentences[i])
    words = ""
    for item in words_list:
        words = words + item + " "
    corpus.append(words)
# print("corpus:", corpus)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

# get all words appeared in corpus
word = vectorizer.get_feature_names()
word_num = len(word)
# print("word:", word)

# get words appeared in keywords
keywords_index = []
for j in range(word_num):
    if word[j] in keywords_list:
        keywords_index.append(j)
appeared_keywords_num = len(keywords_index)

# get term frequency of each word at each sentence
counts = X.toarray()
# print("counts:", counts)

# get tf-idf value of each word at each sentence
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)
tfidf_array = tfidf.toarray()
# print("tfidf:", tfidf_array)

# calculate the importance of each sentence
# e.g. sentence_scores = [3.2,5.1]
sentence_scores = []
for i in range(sentence_num):
    score = 0
    for j in range(appeared_keywords_num):
        score = score + tfidf_array[i][keywords_index[j]]
    sentence_scores.append((i, score))


#print("scores:", sentence_scores)

# 将整个得分放到一个正方形中，存在文件里
grids = []
grid_len = int(math.sqrt(len(sentence_scores))) + 1
for sc in sentence_scores:
    pos,val = sc
    grids.append([pos/grid_len,pos%grid_len,val])

with open("grids_res.txt",'w') as f:
    print(grids,file=f)

pseudo_time = []
inc = 0
for sc in sentence_scores:
    pos,_ = sc
    pseudo_time.append(inc)
    inc += len(sentences[pos])

with open("time_res.txt",'w') as f:
    print([list(x) for x in list(zip(pseudo_time,[x[1] for x in sentence_scores]))],file=f)


# display the result in various ways
def takeSecond(elem):
    return elem[1]

sentence_scores.sort(key=takeSecond)
k = 10
print("Top ", k, "Relevant Sentences:")
for i in range(k):
    print(sentences[sentence_scores[-i-1][0]])
    #print(sentence_scores[-i-1])

print("Top ",k, "Irrelevant Sentences:")
for i in range(k):
    print(sentences[sentence_scores[i][0]])
    


# coding=utf-8
import nltk
newsfile = open('../data/news.csv', encoding = 'UTF-8')
text = newsfile.read()
tokens = nltk.word_tokenize(text)  #分词
tagged = nltk.pos_tag(tokens)  #词性标注
entities = nltk.chunk.ne_chunk(tagged)  # NER
a1 = str(entities)
ner_result = open('../data/ner_result','w',encoding = 'UTF-8')
ner_result.write(a1)
ner_result.close()
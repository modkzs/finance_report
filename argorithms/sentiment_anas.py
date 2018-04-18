# encoding=utf-8
import jieba
import sys
import codecs

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn


def doSeg(filename) :
    f = open(filename, 'r+',encoding="utf-8")
    file_list = f.read()
    f.close()

    seg_list = jieba.cut(file_list)

    stopwords = []
    for word in open("../data/stop_words.txt", "r",encoding="utf-8"):
        stopwords.append(word.strip())

    ll = []
    for seg in seg_list :
        if (seg.encode("utf-8") not in stopwords and seg != ' ' and seg != '' and seg != "\n" and seg != "\n\n"):
            ll.append(seg)
    return ll

def loadWordNet():
    f = codecs.open("../data/cow-not-full.txt", "rb", "utf-8")
    known = set()
    for l in f:
        if l.startswith('#') or not l.strip():
            continue
        row = l.strip().split("\t")
        if len(row) == 3:
            (synset, lemma, status) = row
        elif len(row) == 2:
            (synset, lemma) = row
            status = 'Y'
        else:
            print ("illformed line: ", l.strip())
        if status in ['Y', 'O' ]:
            if not (synset.strip(), lemma.strip()) in known:
                known.add((synset.strip(), lemma.strip()))
    return known

def findWordNet(known, key):
    ll = [];
    for kk in known:
        if (kk[1] == key):
             ll.append(kk[0])
    return ll

def id2ss(ID):
    return wn._synset_from_pos_and_offset(str(ID[-1:]), int(ID[:8]))

def getSenti(word):
    return swn.senti_synset(word.name())

if __name__ == '__main__' :
    known = loadWordNet()
    words = doSeg("../data/news.csv")

    n = 0
    p = 0
    for word in words:
      ll = findWordNet(known, word)
      if (len(ll) != 0):
          n1 = 0.0
          p1 = 0.0
          for wid in ll:
              desc = id2ss(wid)
              swninfo = getSenti(desc)
              p1 = p1 + swninfo.pos_score()
              n1 = n1 + swninfo.neg_score()
          if (p1 != 0.0 or n1 != 0.0):
              print (word, '-> n ', (n1 / len(ll)), ", p ", (p1 / len(ll)))
          p = p + p1 / len(ll)
          n = n + n1 / len(ll)
    print( "n", n, ", p", p)
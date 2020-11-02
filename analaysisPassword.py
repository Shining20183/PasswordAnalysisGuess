import pkuseg
from collections import Counter
import analysis_pingyin
import pandas as pd
from nltk.corpus import  stopwords
english_words = pd.read_csv('data/NSGL.csv')
english_words=list(english_words['Word'])
sp_word=stopwords.words('english')
pinyin=open("data/pinyin.txt").read().split()
def analysis_CSDN():
    c=0
    res = []
    with open('data/processed_csdn.sql','r',encoding='utf-8') as f:
        line=f.readline()
        while line:
            if c%100000==0:
                print(c)
            line=line.strip('\n')
            text=analysis_pingyin.infer_spaces(line)
            for t in text:

                res.append(t)
            line=f.readline()
            c+=1

    a=Counter(res)
    a=sorted(a.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    c=0
    for k,v in a:
        if k not in pinyin and k not in 'bcdefghijklmnopqrstuvwxyz' and k not in sp_word and k in english_words:
            c+=1
            if c>30:
                break
            print(k,v)
def analysis_YAHOO():
    res = []
    c=0
    with open('data/processed_yahoo.txt', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            if c % 100000 == 0:
                print(c)
            line = line.strip('\n')
            text = analysis_pingyin.infer_spaces(line)
            for t in text:
                res.append(t)
            line = f.readline()
            c += 1

    a = Counter(res)
    a = sorted(a.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    c = 0
	
    for k, v in a:
        if k not in pinyin and k not in 'bcdefghijklmnopqrstuvwxyz' and k not in sp_word and k in english_words:
            c += 1
            if c > 30:
                break
            print(k, v)



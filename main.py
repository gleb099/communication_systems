import re
import nltk

from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords as nltk_stopwords

from bs4 import BeautifulSoup
import requests
import pandas as pd

import time

from ruwordnet import RuWordNet

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\-]+"
nltk.download('stopwords')
stopwords_ru = nltk_stopwords.words("russian")
morph = MorphAnalyzer()


def lemmatizeDoc(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None


f = open('words.txt', encoding='utf-8')
mass = list()
dictDoc = dict()
for line in f:
    tempList = lemmatizeDoc(line)
    try:
        for item in tempList:
            if len(item) >= 4:
                mass.append(item)
    except:
        pass
print(mass)
f.close()

for item in mass:
    if item not in list(dictDoc.keys()):
        dictDoc[item] = 1
    else:
        dictDoc[item] += 1

sorted_dictDoc = dict(sorted(dictDoc.items(), key=lambda item: item[1], reverse=True))

print(sorted_dictDoc)

sin1, sin2, sin3, sin4 = list(), list(), list(), list()
count = 1
for word in list(sorted_dictDoc.keys()):
    if count == 180:
        break
    url = f'https://text.ru/synonym/{word}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    print(count, page.status_code)
    if page.status_code != 200:
        sin1.append("")
        sin2.append("")
        sin3.append("")
        sin4.append("")
        time.sleep(2)
        continue

    soup = BeautifulSoup(page.text, "html.parser")

    allS = soup.findAll('a')
    print(word, "||", allS[45].text, ",", allS[48].text, ",", allS[51].text, ",", allS[54].text)
    sin1.append(allS[45].text)
    sin2.append(allS[48].text)
    sin3.append(allS[51].text)
    sin4.append(allS[54].text)

    time.sleep(2)
    count += 1
print(len(sin1))
print(len(sin2))
print(len(sin3))
print(len(sin4))
print(len(list(sorted_dictDoc.keys())[:150]))
df = pd.DataFrame({'Слово': list(sorted_dictDoc.keys())[:150], 'Синоним 1': sin1[:150], 'Синоним 2': sin2[:150],
                   'Синоним 3': sin3[:150], 'Синоним 4': sin4[:150]})
df.to_excel("lab1.xlsx")

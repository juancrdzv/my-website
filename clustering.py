import urllib3
import os
import json
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords

QUEJAS_PAGE = 'https://www.apestan.com/searchresult/company_Nextel'
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))+"/json"

def startClustering():
    path = UPLOAD_FOLDER + "/clustering.json"
    my_file = Path(path)

    if my_file.is_file() == False:
        info = getFirstPageInfo()
        complains = getOtherComplains(info['pages'])
        complains = complains + info['complains']
        complainsAndTitles = getComplainTextAndTitle(complains)

    with open(path) as json_file:
        data = json.load(json_file)
        return clustering(data)

def clustering(data):
    forClustering = []
    for d in data:
        d['text'] = " ".join(d['text'].split("\n"))
        forClustering.append(d['text'])

    forClustering = list(set(forClustering))

    vec = TfidfVectorizer(stop_words = stopwords.words('spanish'),
                          norm='l1', # ELL - ONE
                          use_idf=False)

    matrix = vec.fit_transform(forClustering)

    number_of_clusters = 60

    km = KMeans(n_clusters=number_of_clusters)
    km.fit(matrix)

    pd.set_option('display.max_colwidth', -1)
    results = pd.DataFrame()
    results['text'] = forClustering
    results['category'] = km.labels_

    return results

def createJSONFILE(complains):
    my_file = UPLOAD_FOLDER+"/clustering.json"
    with open(my_file, "w") as outfile:
        json.dump(complains,outfile)

def getComplainTextAndTitle(complains):
    main_page = 'https://www.apestan.com'
    new_complains = []

    for c in complains:
        http = urllib3.PoolManager()
        currentUrl = main_page + c
        response = http.request('GET', currentUrl)

        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.find('h1', { 'itemprop' : 'itemreviewed' }).text

        text = soup.find('div', { 'class': 'text-block'}).text.replace('<!--','')
        text = text.replace('(adsbygoogle = window.adsbygoogle || []). push ({});','')
        text = text.replace('-->','')
        text = text.strip()

        new_complains.append({'title': title, 'text':text})

    createJSONFILE(new_complains)

def getFirstPageInfo():
    http = urllib3.PoolManager()
    response = http.request('GET', QUEJAS_PAGE)
    soup = BeautifulSoup(response.data, 'html.parser')
    firstPageInfo = getInfoForFirstPage(soup)

    return firstPageInfo

def getOtherComplains(pages):
    complains = []

    for p in pages:
        currentPage = QUEJAS_PAGE + p
        http = urllib3.PoolManager()
        response = http.request('GET', currentPage)
        soup = BeautifulSoup(response.data, 'html.parser')
        complains = complains + getComplainsLinks(soup)

    return complains

def getComplainsLinks(soup):
    complains = []
    for a in soup.find_all('a', href=True):
        if 'cases' in a['href']:
            complains.append(a['href'])
    return complains

def getInfoForFirstPage(soup):
    otherPages = []
    complains = []
    for a in soup.find_all('a', href=True):
        if 'pagenumber' in a['href']:
            otherPages.append(a['href'])
        if 'cases' in a['href']:
            complains.append(a['href'])

    otherPages = list(set(otherPages))
    complains = list(set(complains))

    return { 'pages': otherPages, 'complains':complains }

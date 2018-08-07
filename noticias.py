import urllib3
import json
from bs4 import BeautifulSoup
from gensim.summarization import summarize

NEWS_PAGE = 'https://www.milenio.com/'

def scrapping_news():
    soup = set_page()
    urls = get_urls(soup)
    news = extract_news(urls)

    return json.dumps(news)

def set_page():
    http = urllib3.PoolManager()
    response = http.request('GET', NEWS_PAGE + 'policia')
    soup = BeautifulSoup(response.data, 'html.parser')
    return soup

def get_urls(soup):
    policiaca = []

    for a in soup.find_all('a', href=True):
        if 'policia' in a['href']:
            policiaca.append(NEWS_PAGE+a['href'])

    policiaca = list(set(policiaca))

    return policiaca

def extract_news(urls):
    news = []

    for url in urls:
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, 'html.parser')
        info = extract_info(soup)
        if(info):
            news.append({ "title":info["title"], "text":info["text"], "url":url })

    return news

def extract_info(soup):
    title = soup.findAll("h1", { "class": "title" })
    container = soup.find("div", { "class": "media-container news" })
    if(container):
        texts = container.findAll("p")

    if len(title) > 0 and texts:
        title = soup.findAll("h1", { "class": "title" })[0].text
        text = get_text(texts)
        return { "title":title, "text":text }

    return None

def get_text(texts):
    try:
        text = []
        for p in texts:
            text.append(p.text)

        text = '\n'.join(text)

        return summarize(text)
    except ValueError:
        print("Error in summarize")

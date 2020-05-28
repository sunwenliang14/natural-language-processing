from requests import get
from bs4 import BeautifulSoup
import os
import re
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import pprint


def get_blog_articles():
    articles = []
    urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
        'https://codeup.com/data-science-myths/', 
        'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
        'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
        'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/'
       ]
    for i in urls:
        headers = {'User-Agent': 'Codeup Curie Data Science'} 
        response = get(i, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text
        text = soup.find('div', class_='jupiterx-post-content clearfix').text
        date = soup.select("header > ul > li.jupiterx-post-meta-date.list-inline-item > time")[0]["datetime"]
        articles.append({"title": title, "content": text, "date_published": date})
    return articles


def get_url(topic):
    url = f"https://inshorts.com/en/read/{topic}"
    headers = {'User-Agent': 'Codeup Curie Data Science'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    # Find all links within that topic
    for link in soup.find_all("a", href=True):
        urls.append(link["href"])
        lines = pd.Series(urls)
        urls = lines[lines.str.contains(r"^/en/news")].tolist()
        new_urls = []
        for i in urls:
            new_urls.append("https://inshorts.com" + i)
    return new_urls

def get_article_info(new_urls, topic):
    news = []
    for new_url in new_urls:
        headers = {'User-Agent': 'Codeup Curie Data Science'} 
        response = get(new_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.select("body > div.container > div > div.card-stack > div > div > div.news-card-title.news-right-box > a > span")[0].text
        body = soup.select("body > div.container > div > div.card-stack > div > div > div.news-card-content.news-right-box > div:nth-child(1)")[0].text
        author = soup.find("span", class_ = "author").text
        date_published = soup.find("span", class_="time")["content"]
        news.append({"title": title, "author": author, "topic": topic, "article": body, "date_published": date_published, "page_url": new_url})
    return news
    
def get_news_articles(topics = []):
    all_news = []
    for topic in topics:
        new_urls = get_url(topic)
        news = get_article_info(new_urls, topic)
        all_news.append(news)
    all_news = sum(all_news, [])
    return all_news
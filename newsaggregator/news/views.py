from unicodedata import category
from django.shortcuts import render, redirect
from lxml import html
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup as BSoup
from news.models import Article
from itertools import chain

requests.packages.urllib3.disable_warnings()

# Global variables
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
cats = ['prog','bi','crypto','robotics']

# This functions updates the whole database 
# (not optimal, but we are not getting salary for this project)
def scrape(req):
    session = requests.Session()
    session.headers = headers
    # Empty database (Can be commented out)
    Article.objects.all().delete()
    # Urls and categories (key values are critical, any changes here will lead to several changes elsewhere and vise versa)
    urls = {cats[0]:"https://hub.packtpub.com/category/programming/",
            cats[1]:'https://hub.packtpub.com/category/data/business-intelligence/',
            cats[2]:'https://hub.packtpub.com/category/security/cryptography/',
            cats[3]:'https://hub.packtpub.com/category/iot-and-hardware/robotics/'}
    
    for src in urls.keys():

        content = session.get(urls[src], verify=False).content
        soup = BSoup(content, "html.parser")
        News = soup.find_all('div', {"class":"td_module_10"}) # <<-- Site specific class name

        for article in News:
            main = article.find_all('a')[0]
            link = main['href']
            # Tools
            response = requests.get(link, headers=headers)
            dom = html.fromstring(response.text)
            # Elements (Site specific)
            source = dom.xpath(".//div[@class='td-post-author-name']/a//text()")[0]
            image_src = str(main.find('img')['src'])
            title = main['title']
            # Get original styled date (Site specific)
            date = dom.xpath(".//header//span[@class='td-post-date']//time//text()")[0]
            date = re.match("(.*) -.*", date).groups(1)
            date = datetime.strptime(date[0], "%B %d, %Y").strftime('%d.%m.%Y')

            new_article = Article()
            new_article.title = title
            new_article.link = link
            new_article.img = image_src
            new_article.date = date
            new_article.source = source
            new_article.category = src
            new_article.save()

    return redirect("../")


def index(req):
    prog_news = Article.objects.filter(category=cats[0])[:2]
    bi_news = Article.objects.filter(category=cats[1])[:2]
    crypt_news = Article.objects.filter(category=cats[2])[:2]
    robot_news = Article.objects.filter(category=cats[3])[:2]
    articles = list(chain(prog_news, bi_news, crypt_news, robot_news))

    context = {'object_list': articles,
               'home': 'active'}
    return render(req, "news/index.html", context)

def categories(req):
    context = {'categories': 'active'}
    return render(req, 'news/categories.html', context)

def about(req):
    context = {'about': 'active'}
    return render(req, 'news/about.html', context)

# Categoty views
def bi(req):
    bi_news = Article.objects.filter(category=cats[1])
    return render(req, 'news/bi.html', {'bi_news': bi_news})

def prog(req):
    prog_news = Article.objects.filter(category=cats[0])
    return render(req, 'news/prog.html', {'prog_news':prog_news})

def robotics(req):
    robot_news = Article.objects.filter(category=cats[3])
    return render(req, 'news/robotics.html', {'robotics_news': robot_news})

def crypto(req):
    crypt_news = Article.objects.filter(category=cats[2])
    return render(req, 'news/crypto.html', {'crypto_news': crypt_news})    


'''
# Programming News
prog_url = 'https://hub.packtpub.com/category/programming/'

prog_response = requests.get(prog_url, headers=headers)
prog_dom = html.fromstring(prog_response.text)
prog_news_elements = prog_dom.xpath("//div[contains(@class, 'td_module_mx')]")

prog_news_list = []

for element in prog_news_elements:
    prog_img = element.xpath('.//img/@src')[0]
    prog_link = element.xpath(".//div[contains(@class, 'td-module-thumb')]//a/@href")[0]

    response = requests.get(prog_link, headers=headers)
    dom = html.fromstring(response.text)

    prog_title = dom.xpath(".//h1[@class='entry-title']/text()")[0]
    prog_publication_date = dom.xpath(".//header//span[@class='td-post-date']//time//text()")[0]
    prog_publication_date = re.match("(.*) -.*", prog_publication_date).groups(1)
    prog_publication_date = datetime.strptime(prog_publication_date[0], "%B %d, %Y").strftime('%d.%m.%Y')

    prog_source = dom.xpath(".//div[@class='td-post-author-name']/a//text()")[0]

    prog_news = {
        'title': prog_title,
        'link': prog_link,
        'date': prog_publication_date,
        'source': prog_source,
        'img': prog_img
    }

    prog_news_list.append(prog_news)


# Business Intelligence News
bi_url = 'https://hub.packtpub.com/category/data/business-intelligence/'

bi_response = requests.get(bi_url, headers=headers)
bi_dom = html.fromstring(bi_response.text)
bi_news_elements = bi_dom.xpath("//div[contains(@class, 'td_module_mx')]")

bi_news_list = []

for element in bi_news_elements:
    bi_img = element.xpath('.//img/@src')[0]
    bi_link = element.xpath(".//div[contains(@class, 'td-module-thumb')]//a/@href")[0]

    response = requests.get(bi_link, headers=headers)
    dom = html.fromstring(response.text)

    bi_title = dom.xpath(".//h1[@class='entry-title']/text()")[0]
    bi_publication_date = dom.xpath(".//header//span[@class='td-post-date']//time//text()")[0]
    bi_publication_date = re.match("(.*) -.*", bi_publication_date).groups(1)
    bi_publication_date = datetime.strptime(bi_publication_date[0], "%B %d, %Y").strftime('%d.%m.%Y')

    bi_source = dom.xpath(".//div[@class='td-post-author-name']/a//text()")[0]

    bi_news = {
        'title': bi_title,
        'link': bi_link,
        'date': bi_publication_date,
        'source': bi_source,
        'img': bi_img
    }

    bi_news_list.append(bi_news)


# Robotics News
robotics_url = 'https://hub.packtpub.com/category/iot-and-hardware/robotics/'

robotics_response = requests.get(robotics_url, headers=headers)
robotics_dom = html.fromstring(robotics_response.text)
robotics_news_elements = robotics_dom.xpath("//div[contains(@class, 'td_module_mx')]")

robotics_news_list = []

for element in robotics_news_elements:
    robotics_img = element.xpath('.//img/@src')[0]
    robotics_link = element.xpath(".//div[contains(@class, 'td-module-thumb')]//a/@href")[0]

    response = requests.get(robotics_link, headers=headers)
    dom = html.fromstring(response.text)

    robotics_title = dom.xpath(".//h1[@class='entry-title']/text()")[0]
    robotics_publication_date = dom.xpath(".//header//span[@class='td-post-date']//time//text()")[0]
    robotics_publication_date = re.match("(.*) -.*", robotics_publication_date).groups(1)
    robotics_publication_date = datetime.strptime(robotics_publication_date[0], "%B %d, %Y").strftime('%d.%m.%Y')

    robotics_source = dom.xpath(".//div[@class='td-post-author-name']/a//text()")[0]

    robotics_news = {
        'title': robotics_title,
        'link': robotics_link,
        'date': robotics_publication_date,
        'source': robotics_source,
        'img': robotics_img
    }

    robotics_news_list.append(robotics_news)


# Cryptography News
crypto_url = 'https://hub.packtpub.com/category/security/cryptography/'

crypto_response = requests.get(crypto_url, headers=headers)
crypto_dom = html.fromstring(crypto_response.text)
crypto_news_elements = crypto_dom.xpath("//div[contains(@class, 'td_module_mx')]")

crypto_news_list = []

for element in crypto_news_elements:
    crypto_img = element.xpath('.//img/@src')[0]
    crypto_link = element.xpath(".//div[contains(@class, 'td-module-thumb')]//a/@href")[0]

    response = requests.get(crypto_link, headers=headers)
    dom = html.fromstring(response.text)

    crypto_title = dom.xpath(".//h1[@class='entry-title']/text()")[0]
    crypto_publication_date = dom.xpath(".//header//span[@class='td-post-date']//time//text()")[0]
    crypto_publication_date = re.match("(.*) -.*", crypto_publication_date).groups(1)
    crypto_publication_date = datetime.strptime(crypto_publication_date[0], "%B %d, %Y").strftime('%d.%m.%Y')

    crypto_source = dom.xpath(".//div[@class='td-post-author-name']/a//text()")[0]

    crypto_news = {
        'title': crypto_title,
        'link': crypto_link,
        'date': crypto_publication_date,
        'source': crypto_source,
        'img': crypto_img
    }
    crypto_news_list.append(crypto_news)

def index(req):
    context = {'home': 'active',
               'prog_news': prog_news_list, 
               'bi_news': bi_news_list }
    return render(req, 'news/index.html', context)
'''
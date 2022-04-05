from django.shortcuts import render
from lxml import html
import requests
import re
from datetime import datetime

# Create your views here.
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

# Programming News
prog_url = 'https://hub.packtpub.com/category/programming/'

prog_response = requests.get(prog_url, headers=headers)
prog_dom = html.fromstring(prog_response.text)
prog_news_elements = prog_dom.xpath("//div[contains(@class, 'td_module_mx')]")

prog_news_list = []

for element in prog_news_elements:
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
        'source': prog_source
    }

    prog_news_list.append(prog_news)


# Business Intelligence News
bi_url = 'https://hub.packtpub.com/category/data/business-intelligence/'

bi_response = requests.get(bi_url, headers=headers)
bi_dom = html.fromstring(bi_response.text)
bi_news_elements = bi_dom.xpath("//div[contains(@class, 'td_module_mx')]")

bi_news_list = []

for element in bi_news_elements:
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
        'source': bi_source
    }

    bi_news_list.append(bi_news)


def index(req):
    return render(req, 'news/index.html', {'prog_news':prog_news_list, 'bi_news': bi_news_list})
    
import requests
import bs4
import json
import csv
import os

if (os.path.exists('results')):
    os.removedirs('results')
os.makedirs('results')


class Author(object):
    def __init__(self, url, author_title, born_date, born_place, about):
        self.url = url
        self.author_title = author_title
        self.born_date = born_date
        self.born_place = born_place
        self.about = about

    @staticmethod
    def get_author_data(url, quotes):
        link = url + quotes.select('span > a')[0].get('href')[1:] + '/'
        author_title = quotes.select('small.author')[0].text
        about_author_page = requests.get(url=link)
        about_author_soup = bs4.BeautifulSoup(about_author_page.content, 'html.parser')
        born_date = about_author_soup.select('span.author-born-date')[0].text
        born_place = about_author_soup.select('span.author-born-location')[0].text.split('in ')[1]
        about = about_author_soup.select('div.author-description')[0].text.strip()
        return Author(link, author_title, born_date, born_place, about).__dict__


class Tags(object):
    def __init__(self, tag_name, tag_url, text, author, author_url):
        self.tag_name = tag_name
        self.tag_url = tag_url
        self.text = text
        self.author = author
        self.author_url = author_url

    @staticmethod
    def get_tag_data(url, quotes):
        tag = []
        for i in range(0, len(quotes.select('a.tag'))):
            tag_name = quotes.select('a.tag')[i].text
            tag_url = url + quotes.select('a.tag')[i].get('href')[1:]
            text = quotes.select('span.text')[0].text[1:-1].strip()
            author = quotes.select('small.author')[0].text
            author_url = url + quotes.select('span > a')[0].get('href')[1:]
            tag.append(Tags(tag_name, tag_url, text, author, author_url).__dict__)
        return tag


class Info(object):
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

    @staticmethod
    def get_info(url, quotes):
        text = quotes.select('span.text')[0].text[1:-1]
        return Info(text, Author.get_author_data(url, quotes), Tags.get_tag_data(url, quotes)).__dict__


page_number = 1
has_next_page = True
next_page_url = ''
url = "http://quotes.toscrape.com/"
r = requests.get(url=url)
data = {}
j = 0
headers = []

while has_next_page:
    print(page_number)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    quotes = soup.select('div.quote')

    for i in range(0, len(quotes)):
        data[j] = Info.get_info(url, quotes[i])
        with open('./results/data.cvs', 'a', encoding='utf-8') as cvs_file:
            writer = csv.writer(cvs_file)
            if j == 0:
                headers = ['Text'] + list(data[0]['author'].keys()) + list(data[0]['tags'][0].keys())
                writer.writerow(headers)
            row = [(data[i]['text'])] + list(data[i]['author'].values()) + list(data[i]['tags'][0].values())
            writer.writerow(row)
        j += 1
    page_number += 1
    next_page_url = 'page/%s/' % str(page_number)
    r = requests.get(url=url + next_page_url)
    if r.status_code != 200 or not soup.select('li.next'):
        has_next_page = False

with open('./results/data.txt', 'a', encoding='utf-8') as txt_file, open('./results/data.json', 'a', encoding='utf-8') as json_file:
    txt_file.write(str(data))
    json.dump(data, json_file, separators=(',', ':'), indent=4)


def get_autho_by_id(*args):
    args = list(args)
    page_number = 1
    has_next_page = True
    next_page_url = ''
    url = "http://quotes.toscrape.com/"
    r = requests.get(url=url)
    authors_id = set()
    author_list = []
    j = 0
    i = 0
    while has_next_page:
        print(page_number)
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        quotes = soup.select('div.quote')

        for i in range(0, len(quotes)):
            author = quotes[i].select('small.author')[0].text
            if (author in args) and (author not in authors_id):
                print('OK')
                author_list += [Author.get_author_data(url, quotes[i])]
                authors_id.add(author)

        page_number += 1
        next_page_url = 'page/%s/' % str(page_number)
        r = requests.get(url=url + next_page_url)
        if r.status_code != 200 or not soup.select('li.next'):
            has_next_page = False

    return author_list

print(json.dumps(get_autho_by_id('Albert Einstein', 'Jane Austen'), separators=(',', ':'), indent=4))


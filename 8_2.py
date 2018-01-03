import requests
import bs4
from xlwt import Workbook
import csv
import os
import time
import random


def integer_generator(start=1):
    while True:
        yield start
        start = start + 1

book = Workbook()
sheet1 = book.add_sheet('Sheet 1')

if (os.path.exists('results2')):
    os.removedirs('results2')
os.makedirs('results2')

def saveDomains(domains):
    for i in range(0, len(domains)):
        saveDomains_cvs(domains[i])
        print(domains[i].text)
        saveDomains_txt(domains[i].text)
        saveDomains_xls(domains[i].text)

def saveDomains_cvs(domains):
    with open('./results2/data.cvs', 'a', encoding='utf-8') as cvs_file:
        writer = csv.writer(cvs_file)
        row = domains
        writer.writerow(row)


def saveDomains_txt(domains):
    with open('./results2/data.txt', 'a', encoding='utf-8') as txt_file:
        txt_file.write(str(domains) + '\n')


def saveDomains_xls(domains, column=integer_generator()):
    sheet1.write(next(column), 0, domains)
    sheet1.col(0).width = 10000
    book.save('./results2/data.xls')

page_number = 0
has_next_page = True
data = {}
# url = ('https://www.expireddomains.net/backorder-expired-domains/?start=%s&ftlds[]=4' % str(page_number * 25))
# r = requests.get(url=url)
# soup = bs4.BeautifulSoup(r.content, 'html.parser')

while has_next_page:
    url = ('https://www.expireddomains.net/backorder-expired-domains/?start=%s&ftlds[]=4' % str(page_number * 25))
    r = requests.get(url=url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    domains = soup.select('tbody tr a.namelinks')
    saveDomains(domains)
    page_number += 1
    if (len(soup.select('table.base1')) == 0 or len(soup.select('a.next')) == 0 or len(soup.select(
            'head link[rel="next"]')) == 0):
        has_next_page = False
    if page_number % 5 == 0:
        time.sleep(random.randint(17, 25))

    print(page_number)

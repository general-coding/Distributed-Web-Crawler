__author__ = 'Tarun'
import requests
from bs4 import BeautifulSoup

from string import ascii_lowercase

Alpha_Num= {}
Num_Alpha={}

## i represnts numbers j represents alphabhets
Num_Alpha=dict((j,i) for i,j in enumerate(ascii_lowercase, 1))
Alpha_Num= dict((i,j) for i,j in enumerate(ascii_lowercase, 1))
##print(Alpha_Num)

def trade_spider(max_pages):
    page=1
    while page <= max_pages:
        ##url = 'https://buckysroom.org/trade/search.php?page='+ str(page)
        url='http://www.uta.edu/uta/alpha-index.php?alpha='+Alpha_Num[page]
        ##print(url)
        source_code= requests.get(url)
        plain_text= source_code.text
       ## print(plain_text)
        ##print(type(plain_text))
        soup = BeautifulSoup(plain_text)
        ##print(soup)
        ## unique to links
        ##for link in soup.findAll('a',{'class':'item-name'}):
        for link in soup.findAll('p',{'class':'az-list'}):
            ##print(type(link))
            ##print(link)
            SumOfLinks=BeautifulSoup(str(link))
            ##print(SumOfLinks)
            for sublink in SumOfLinks.findAll('a'):
                title=sublink.string
                print(title)
                href= "http://www.uta.edu/uta/alpha-index.php"+ sublink.get('href')
                print(href)
                get_data_from_url(href)
        page+=1


def get_data_from_url(target_url):
    source_code= requests.get(target_url)
    plain_text= source_code.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        print(str(link.string)+"\n")


trade_spider(1)


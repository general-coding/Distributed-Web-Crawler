'''
Created on Apr 9, 2015

@author: puneeth
'''

from bs4 import BeautifulSoup
import urllib3

crawl_url = 'http://www.nytimes.com/'
http = urllib3.PoolManager()
response = http.request('GET', crawl_url)
soup = BeautifulSoup(response.data)
# soup.prettify()
# print(soup)
# exit()

all_links = soup.find_all('href')
print(all_links)
exit()
list_of_links = []
# print(all_links)
for link in all_links:
    try:
        link_httpx = link.get('href')
        print(link_httpx, link_httpx.startswith('http'), link_httpx.startswith('https'))
        if link_httpx.startswith('http') or link_httpx.startswith('https'): 
            list_of_links.append(link.get('href'))
        if link_httpx.startswith('#'):
            list_of_links.append(crawl_url + link.get('href'))
    except Exception:
        pass

list_links = list(set(list_of_links))
print(len(list_of_links))
print(len(list_links))

f = open("list_links.txt", mode='w')
for link in list_links:
    f.write(link + '\n')
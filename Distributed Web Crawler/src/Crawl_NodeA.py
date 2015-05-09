'''
Created on Apr 9, 2015

@author: puneeth
'''

from bs4 import BeautifulSoup
from boto.s3.connection import S3Connection, Bucket, Key
from boto.exception import S3ResponseError
import urllib3, urllib, os
from urllib3.exceptions import MaxRetryError, LocationValueError
from urllib.error import HTTPError

def crawl(url):
    try:
#         url = 'http://en.wikipedia.org/wiki/The_New_York_Times'
        print('Crawling:', url)
        http = urllib3.PoolManager()
#         response = http.request('GET', url)
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response)
        soup.prettify()
#         print(soup)
#         exit()
        
        all_links = soup.find_all('a')
#         print('here1', all_links)
#         exit()
        list_of_links = []
        # print(all_links)
        for link in all_links:
            try:
                link_httpx = link.get('href')
#                 print(link_httpx)
    #             print(link_httpx.startswith('http'), link_httpx.startswith('https'))
                if link_httpx.startswith('http') or link_httpx.startswith('https'): 
                    list_of_links.append(link.get('href'))
#                 if link_httpx.startswith('#'):
#                     list_of_links.append(url + link.get('href'))
            except Exception:
                pass
        
        list_links = list(set(list_of_links))
        list_links.sort()
#         print(len(list_of_links))
#         print(len(list_links))
        
        fa = open("list_links_a.txt", 'a')
        for link in list_links:
            print('here')
            fa.write(link + '\n')
            
        fa.close()
        http.clear()
        
    except MaxRetryError:
        print('MaxRetryError')
    except LocationValueError:
        print('LocationValueError')
    except HTTPError:
        print('HTTPError')
        
def s3():
    access_token_file = open('key.txt')
    access_token = access_token_file.read()
    access_token_file.close()
    
    AWSAccessKeyId, AWSSecretKey = access_token.split('|')
    
    s3_conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
    
    return s3_conn

def upload():
    s3_conn = s3()
    
#     bucket = s3_conn.create_bucket('distributed-web-crawler')
    bucket = Bucket(s3_conn, 'distributed-web-crawler')
    
    k = Key(bucket)
    
    k.key = 'list_links_a.txt'
    k.set_contents_from_filename('input_links_a.txt')
    
    os.remove('input_links_a.txt')
    os.remove('list_links_a.txt')
    
    s3_conn.close()

def download():
    s3_conn = s3()
    
#     bucket = s3_conn.create_bucket('distributed-web-crawler')
    bucket = Bucket(s3_conn, 'distributed-web-crawler')
    
    while True:
        try:
            k = Key(bucket)
            
            k.key = 'list_links_a.txt'
            k.get_contents_to_filename('input_links_a.txt')
            bucket.delete_key(k)
            
            break
            
        except S3ResponseError:
            pass
    
    s3_conn.close()

print('download')
download()

print('crawl')
url_input_file = open('input_links_a.txt', 'r')
for url in url_input_file:
    crawl(url)

print('upload')
upload()
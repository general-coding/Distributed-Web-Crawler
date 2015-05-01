'''
Created on Apr 9, 2015

@author: puneeth
'''

from bs4 import BeautifulSoup
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
import urllib3, os, urllib
from urllib3.exceptions import MaxRetryError, LocationValueError
# from time import sleep
from urllib.error import HTTPError

def crawl(url):
    try:
#         print('Crawling:', url)
        http = urllib3.PoolManager()
#         response = http.request('GET', url)
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response)
        soup.prettify()
        # print(soup)
        # exit()
        
        all_links = soup.find_all('a')
        # print(all_links)
        # exit()
        list_of_links = []
        # print(all_links)
        for link in all_links:
            try:
                link_httpx = link.get('href')
#                 print(link_httpx)
    #             print(link_httpx.startswith('http'), link_httpx.startswith('https'))
                if link_httpx.startswith('http') or link_httpx.startswith('https'): 
                    list_of_links.append(link.get('href'))
                if link_httpx.startswith('#'):
                    list_of_links.append(url + link.get('href'))
            except Exception:
                pass
        
        list_links = list(set(list_of_links))
        list_links.sort()
#         print(len(list_of_links))
#         print(len(list_links))
        
        fa = open("list_links_a.txt", mode='w')
        fb = open("list_links_b.txt", mode='w')
        counter = 0
        for link in list_links:
            if counter % 2 == 0: 
                fa.write(link + '\n')
            else:
                fb.write(link + '\n')
            
            counter = counter + 1
            
        fa.close()
        fb.close()
        http.clear()
        
    except MaxRetryError:
        pass
#     except LocationValueError:
    except LocationValueError:
        pass
    except HTTPError:
        pass

def s3():
    access_token_file = open('/home/puneeth/workspace/App/src/crawler/key.txt')
    access_token = access_token_file.read()
    access_token_file.close()
    
    AWSAccessKeyId, AWSSecretKey = access_token.split('|')
    
    s3_conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
    
    return s3_conn

def upload():
    s3_conn = s3()
    
    bucket = s3_conn.create_bucket('distributed-web-crawler')
    
    k = Key(bucket)
    
    k.key = 'list_links_a.txt'
    k.set_contents_from_filename('list_links_a.txt')
    
    k.key = 'list_links_b.txt'
    k.set_contents_from_filename('list_links_b.txt')
    
    s3_conn.close()
    
    os.remove('list_links_a.txt')
    os.remove('list_links_b.txt')

def download():
    s3_conn = s3()
    
    bucket = s3_conn.create_bucket('distributed-web-crawler')
    
    while True:
        try:
            k = Key(bucket)
            
            k.key = 'list_links_a.txt'
            k.get_contents_to_filename('list_links_a.txt')
            
            k.key = 'list_links_b.txt'
            k.get_contents_to_filename('list_links_b.txt')
            
            break
            
        except S3ResponseError:
            pass
    
    s3_conn.close()

def concat_file():
    input_file = open('list_links_a.txt', 'r')
    output_file = open('input.txt', 'w')
    for line in input_file:
        output_file.write(line)
        
    input_file.close()
    output_file.close()
        
    input_file = open('list_links_b.txt', 'r')
    output_file = open('input.txt', 'a')
    for line in input_file:
        output_file.write(line)
    
    input_file.close()
    output_file.close()


def init(url):
    # url = input('Please enter the source URL: ')
    crawl(url)
    
    # sleep(5)
    upload()
    
    # sleep(5)
    download()
    
    # sleep(5)
    concat_file()
    
#     url_input_file = open('input.txt', 'r')
#     for url in url_input_file:
#         crawl(url)
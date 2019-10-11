# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:38:52 2019

@author: dell
"""

from lxml import etree
import requests
BASE_DOMAIN = 'http://dytt8.net'

url = "https://www.dytt8.net/html/gndy/dyzz/list_23_1.html"
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
def get_detail_urls(url):    
    respons = requests.get(url,headers=headers)
    text = respons.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    #for detail_url in detail_urls:
        #print(BASE_DOMAIN+detail_url)
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

def parse_detail_page(url):
    respons = requests.get(url,headers = headers)
    text = respons.content.decode('gbk','ignore')
    html = etree.HTML(text)
    title = html.xpath("//font[@color='#07519a'")
    for x in title:
        print(etree.tostring(x,encoding='utf-8').decode('utf-8'))              

def spider():
    base_url="https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    for x in range(1,8):
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            movie = parse_detail_page(detail_url)
            break
        break
    
        

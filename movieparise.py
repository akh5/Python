# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:38:52 2019

@author: dell
"""

from lxml import etree
import requests
import re
BASE_DOMAIN = 'http://dytt8.net'

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }

def get_detail_urls(url):    
    respons = requests.get(url,headers=headers)
    text = respons.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

def parse_detail_page(url):
    movie = {}
    respons = requests.get(url,headers = headers)
    text = respons.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    download = html.xpath("//div[@id='Zoom']//a/@href")[0]
    movie['title'] = title
    movie['download'] = download
    return movie

def find_what_u_want(movies):
    find_out = []
    for movie in movies:
        text = movie['title']
        if(bool(re.search('.+悬疑*',text))):
            find_out.append(movie)
        
    print(find_out)
        

def spider():
    base_url="https://www.dytt8.net/html/gndy/dyzz/list_23_1.html"
    movies = []
    url = base_url
    detail_urls = get_detail_urls(url)
    for detail_url in detail_urls:
        movie = parse_detail_page(detail_url)   
        movies.append(movie)
        #print(movie)
    #print(movies)
    find_what_u_want(movies)
spider()
       

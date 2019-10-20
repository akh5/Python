# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 21:56:59 2019

@author: akh5
"""

from lxml import etree
import requests
import re
import os
from queue import Queue
import threading
from urllib import request

class get_DownLoadList(threading.Thread):
    def __init__(self,page_queue,pic_queue,*args,**kwargs):
        super(get_DownLoadList,self).__init__(*args,**kwargs)     
        self.page_queue = page_queue
        self.pic_queue = pic_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.get_pic(url)
            
    def get_pic(self,url):
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        respons = requests.get(url,headers=headers)
        text = respons.text
        html = etree.HTML(text)
        pics = html.xpath('//div[@class="page-content text-center"]//img')
        for pic in pics: 
            suffix = os.path.splitext(pic.get('data-original'))[1]
            picname = re.sub('[\*\-\.!！,，？\?]','',str(pic.get('alt')))
            filename = picname+suffix
            href=pic.get('data-original')
            self.pic_queue.put((href,filename))
            
class download(threading.Thread):
    def __init__(self,page_queue,pic_queue,*args,**kwargs):
        super(download,self).__init__(*args,**kwargs)
        self.page_queue=page_queue
        self.pic_queue=pic_queue
        
    def run(self):
        while True:
            if self.page_queue.empty() and self.pic_queue.empty():
                break
            pic_hrf,filename = self.pic_queue.get()
            request.urlretrieve(pic_hrf,'imges/'+filename)
                
#    def downloadTofolder(self):
#        pic_hrf,filename = self.pic_queue.get()
#        print(pic_hrf,filename)
#        request.urlretrieve(pic_hrf,'imges/'+filename)
#        

def spider():
    page_queue = Queue(5)
    pic_queue = Queue(1000)
    for x in range(1,2):
        url = 'https://www.doutula.com/photo/list/?page=%d'%x
        page_queue.put(url)
    for x in range(5):
        t1 = get_DownLoadList(page_queue,pic_queue)
        t1.start()
    for x in range(5):
        t2 = download(page_queue,pic_queue)
        t2.start()

spider()
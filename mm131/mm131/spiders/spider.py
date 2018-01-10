# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import requests
import re

class SpiderSpider(scrapy.Spider):
    deck_url = r'C:/Users/ASUS/Desktop/image'
    name = 'spider'
    allowed_domains = ['mm131.com']
    start_urls = [
                  'http://www.mm131.com/xinggan/',
                  'http://www.mm131.com/qingchun/',
                  'http://www.mm131.com/xiaohua/',
                  'http://www.mm131.com/chemo/',
                  'http://www.mm131.com/qipao/',
                  'http://www.mm131.com/mingxing/'
                  ]

    def start_requests(self):
        pattern = re.compile(r'<dd><a target="_blank" href="(.*?)"><img src=".*?" alt=".*?" width="120" height="160">(.*?)</a></dd>',re.S)
        num = re.compile(r'<a href="list_(.)_(.*?).html" class="page-en">末页</a>',re.S)
        res = requests.get(self)
        main = re.findall(num,res.text)
        last_num = main[1]
        for n in range(last_num-1):
            url =''
            if(n==0):
                url = self
            else:
                url = self +'list_'+ main[0]+'_'+(n+1)+'.html'
            yield Request(url,callback=self.parse_one)

    def parse_one(self, response):
        
         pass




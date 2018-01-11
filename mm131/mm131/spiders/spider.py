# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from mm131.items import Item
import re
import uuid
import datetime
import os
import random

class SpiderSpider(scrapy.Spider):

    name = 'spider'
    allowed_domains = ['mm131.com']

    def start_requests(self):
        start_urls = [
                      'http://www.mm131.com/'
                      ]
        #分类集合
        category_set = [
                      'xinggan',
                      'qingchun',
                      'xiaohua',
                      'chemo',
                      'qipao',
                      'mingxing'
                      ]
        for category_code in category_set:
            #创建分类文件夹
            if not os.path.isdir(''):
                os.mkdir()
            url_category = start_urls + category_code +'/'
            yield Request(url_category, meta={'category_code': category_code}, callback=self.parse_one)

    #1.获取每个分类的总页数
    #2.获取每页url
    def parse_one(self, response):
        category_code = response.meta['category_code']
        #获取当前分类下的所有页数
        num = re.compile(r'<a href="list_(.)_(.*?).html" class="page-en">末页</a>', re.S)
        main = re.findall(num, response)
        last_num = main[1]
        for n in range(last_num-1):
            url = response.url
            if(n != 0):
                url = response.url + 'list_' + main[0]+'_'+(n+1)+'.html'
            yield Request(url, meta={'category_code': category_code}, callback=self.parse_two)

    #1.获取每个image的标题，url入口，分类
    #2.随机生成一个image_id
    def parse_two(self, response):
        category_code = response.meta['category_code']
        #主文件夹路径
        disk = r'C:/python/image'
        disk_dir = disk + '/' + category_code
        item = Item()
        #获取当前页面下的所有image属性
        content = response.xpath('//div[@class="main"]/dl/dd').extract()
        for c in content:
            #递归创建文件夹
            if not os.path.isdir(disk_dir):
                os.mkdir(disk_dir)
            #生成当前的时间
            nowTime = re.sub(r'[^0-9]','',str(datetime.datetime.now()))
            item['image_id'] = uuid.uuid1()
            item['category_code'] = category_code
            item['image_directory'] = category_code + '/' + nowTime
            item['image_title'] = content.xpath('.//a/img/@alt').extract()
            item['image_href'] = content.xpath('.//a/@href').extract()
            yield Request(item.image_href, meta={'item': item}, callback=self.parse_three())

    #1.获取image时间
    #2.获取每个image页码总数
    def parse_three(self, response):
        item = Item()
        item_from = response.meta['item']
        pattern = re.compile(r'<span class="page-ch">共(.*?)页</span>', re.S)
        last_page = re.compile(r'<a href="(.*?)" class="page-ch">下一页</a>', re.S)
        image_url = response.xpath('//div[@class="content-pic"]/a/img/@src').extract()
        main = re.findall(pattern, response)
        num = main[0]

        item['image_id'] = item_from['image_id']
        item['image_title'] = item_from['image_title']
        item['category_code'] = item_from['category_code']
        item['image_directory'] = item_from['image_directory']
        item['image_url'] = image_url
        item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item
        for n in range(num-1):
            last_page_url = response.url
            if(n != 0):
                last_page_url = response.url + '/' + re.findall(last_page, response)
            yield Request(last_page_url, meta={'item': item}, callback=self.parse_three())

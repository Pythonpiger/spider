# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from mm131.items import Item
import re
import uuid
import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderSpider(scrapy.Spider):

    name = 'spider'
    allowed_domains = ['mm131.com']
    disk = r'C:/python/image/mm131'
    image_from = 'mm131'
    main_url = 'http://www.mm131.com/'
    def start_requests(self):

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
            category_path = self.disk + '/' +category_code
            if not os.path.isdir(category_path):
                os.makedirs(category_path)
            url_category = self.main_url + category_code +'/'
            yield Request(url_category, meta={'category_code': category_code}, callback=self.parse_one)

    #1.获取每个分类的总页数
    #2.获取每页url
    def parse_one(self, response):
        category_code = response.meta['category_code']
        #1.判断是否存在下一页extract(): 序列化该节点为Unicode字符串并返回list列表。
        is_last_page = response.xpath("//a[@class='page-en']/text()='下一页'")
        last_page_url = response.xpath("//a[@class='page-en' and text()='下一页']/@href").extract()
        if(is_last_page == 1):
            yield Request(self.main_url+last_page_url, meta={'category_code': category_code}, callback=self.parse_one)
        images = response.xpath('//dl/dd')
        for image in images:
            url = images.xpath('//a/@href').extract()[0]
            item = Item()
            item['image_title'] = images.xpath("//a/img/@alt").extract()[0]
            nowTime = re.sub(r'[^0-9]', '', str(datetime.datetime.now()))
            item['image_url'] = self.image_from + '/' + category_code + '/' + nowTime
            item['image_id'] = str(uuid.uuid1())
            item['category_code'] = category_code
            item['image_from'] = self.image_from
            yield Request(url, meta={'item': item}, callback=self.parse_two)

    #1.获取每个image的标题，url入口，分类
    #2.随机生成一个image_id
    def parse_two(self, response):
        item = response.meta['item']
        category_code = item['category_code']
        item['path'] = self.disk + '/' + item['image_url'] + '.jpg'
        item['image_title'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #判断是否有下一页
        is_page_last = response.xpath('//div/a[@class="page-ch"]/text()="下一页"')
        page_last_url = response.xpath('//div/a[@class="page-ch" and text()="下一页"]/@href')
        if(is_page_last == 1):
            yield Request(self.main_url+category_code+'/'+page_last_url, meta={'item': item}, callback=self.parse_two)
        yield item
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from mm131.items import Item
import re
import uuid
import datetime
import os
import sys
import random
import string
from lxml import html
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderSpider(scrapy.Spider):

    name = 'spider'
    allowed_domains = ['mm131.com', 'img1.mm131.me']
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
        is_last_page = response.xpath(u"//a[@class='page-en']/text()='下一页'").extract()[0]
        if(int(is_last_page) == 1):
            last_page_url = response.xpath(u"//a[text()='下一页']/@href").extract()[0]
            yield Request(self.main_url + category_code + '/' + last_page_url, meta={'category_code': category_code}, callback=self.parse_one)
        images = response.xpath(u'//div[@class="main"]/dl/dd[not(@class="page")]').extract()
        for image in images:
            image = html.fromstring(image)
            image_html_url = image.xpath(u'//a[@target="_blank"]/@href')[0].encode('utf-8')
            item = Item()
            #图片标题
            image_title = image.xpath(u"//a[@target='_blank']/img/@alt")[0].encode('utf-8')
            item['image_title'] = image_title
            #随机生成10位图片文件夹名称 mm131/xinggan/028e3md7  salt
            salt = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
            #图片路径目录（保存在数据库的）image_url_dir
            image_url_dir = self.image_from + '/' + category_code + '/' + salt
            item['image_url_dir'] = image_url_dir
            dir_path = self.disk + '/' + category_code + '/' + salt
            item['dir_path'] = dir_path
             #创建分类文件夹
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            item['image_id'] = str(uuid.uuid1())
            item['category_code'] = category_code
            item['image_from'] = self.image_from

            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                'referer': response.url,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
                }
            yield Request(image_html_url, meta={'item': item}, callback=self.parse_two, headers=headers)

    #1.获取每个image的标题，url入口，分类
    #2.随机生成一个image_id
    def parse_two(self, response):
        item = response.meta['item']
        category_code = item['category_code']
        is_page_last = response.xpath(u'.//div/a[@class="page-ch"]/text()="下一页"').extract()[0].encode('utf-8')
        #判断是否有下一页
        if(int(is_page_last) == 1):
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                'referer': response.url,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
                }
            page_last_url = response.xpath(u'.//div/a[@class="page-ch" and text()="下一页"]/@href').extract()[0].encode('utf-8')
            yield Request(self.main_url+category_code+'/'+page_last_url, meta={'item': item}, callback=self.parse_two, headers=headers)
        item['image_down_url'] = response.xpath(u'//div[@class="content-pic"]/a/img/@src').extract()[0].encode('utf-8')
        file_name = re.sub(r'[^0-9]', '', str(datetime.datetime.now()))
        item['file_path'] = item['dir_path'] + '/' + file_name + '.jpg'
        item['image_url'] = item['image_url_dir'] + '/' + file_name + '.jpg'
        item['image_html'] = response.url

        yield item

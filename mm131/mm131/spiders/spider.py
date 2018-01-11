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
    disk = r'C:/python/image'
    main_url = 'http://www.mm131.com/'
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
            category_path = self.disk + '/' +category_code
            if not os.path.isdir(category_path):
                os.makedirs(category_path)
            url_category = self.main_url + category_code +'/'
            yield Request(url_category, meta={'category_code': category_code}, callback=self.parse_one)

    #1.获取每个分类的总页数
    #2.获取每页url
    def parse_one(self, response):
        category_code = response.meta['category_code']
        #获取当前分类下的所有页数
        main = re.findall(r'</a><a.*?href=.list_(.*?)_(.*?).html.*?class="page-en">.*?</a></dd>', response.text.encode('utf-8'))
        print response.url
        print main
        last_num = main[0][1]
        for n in range(int(last_num)-1):
            url = response.url
            if(n != 0):
                url = self.main_url + category_code + '/' + 'list_' + main[0][1]+'_'+str(n+1)+'.html'
            yield Request(url, meta={'category_code': category_code}, callback=self.parse_two)

    #1.获取每个image的标题，url入口，分类
    #2.随机生成一个image_id
    def parse_two(self, response):
        category_code = response.meta['category_code']
        #主文件夹路径
        disk_dir = self.disk + '/' + category_code
        item = Item()
        #获取当前页面下的所有image属性
        content = response.xpath('//div[@class="main"]/dl/dd')
        print content
        for c in content:
            #递归创建分类文件夹
            if not os.path.isdir(disk_dir):
                os.makedirs(disk_dir)
            #生成当前的时间
            nowTime = re.sub(r'[^0-9]','',str(datetime.datetime.now()))
            item['image_id'] =str(uuid.uuid1())
            item['category_code'] = category_code
            item['path'] = category_code + '/' + nowTime + '.jpg'
            item['image_title'] = content.xpath('.//a/img/@alt').extract()[0]
            image_href = content.xpath('.//a/@href').extract()[0]
            print image_href
            yield Request(image_href, meta={'item': item}, callback=self.parse_three)

    #1.获取image时间
    #2.获取每个image页码总数
    def parse_three(self, response):
        item = Item()
        item_from = response.meta['item']
        pattern = re.compile(r'<span.*?class="page-ch">共(.*?)页</span>', re.S)
        last_page = re.compile(r'<a.*?href="(.*?)" class="page-ch">下一页</a></div>', re.S)
        #seq = re.findall(r'<div class="content"><h5>.*?((.*?))</h5>', response.text.encode('utf-8'))
        image_url = response.xpath('//div[@class="content-pic"]/a/img/@src').extract()

        num = re.findall(pattern, response.text.encode('utf-8'))
        print num
        #print seq
        #item['image_seq'] = seq
        item['image_id'] = item_from['image_id']
        item['image_title'] = item_from['image_title']
        item['category_code'] = item_from['category_code']
        item['path'] = item_from['path']
        item['image_url'] = image_url
        item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        down_page = response.xpath('//a[@class="page-ch"]/@href').extract()
        print down_page
        yield item
        print '@@@@@@@@@@@@@@@@@@@'
        print num
        for n in range(int(num[0])-1):
            last_page_url = self.main_url + item_from['category_code']
            if(n != 0):
                print n
                last_page_url = self.main_url + item_from['category_code'] + '/' + down_page[0]
            yield Request(last_page_url, meta={'item': item}, callback=self.parse_three)

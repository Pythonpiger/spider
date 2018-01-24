# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
import uuid
import datetime
import os
import sys
from kehuan.items import BookItem
import random
import string
from lxml import html
reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderSpider(scrapy.Spider):

    name = 'spider'
    allowed_domains = ['kehuan.net.cn']
    disk = r'C:/python/book/kehuan'
    image_from = 'kehuan'
    url = 'http://www.kehuan.net.cn'
    main_url = 'http://www.kehuan.net.cn/book.html'

    def start_requests(self):
        yield Request(self.main_url, callback=self.parse_one)

    #获取作者名称和书名
    def parse_one(self, response):
        books = response.xpath(u"//tbody/tr/td/p").extract()
        for book in books:
            book_item = BookItem()
            book_item["book_id"] = str(uuid.uuid1())
            book_item["book_name"] = book.xpath(u"//a/strong/text()")
            book_item["book_author"] = book.xpath(u"//span/a/text()")
            href = book.xpath(u"//a/@href")
            yield Request(self.url+href, meta={'book_item': book_item}, callback=self.parse_two)

    #获取书简介内容或者url
    def parse_two(self, response):
        book_item = response.meta['book_item']
        sections = response.xpath(u"//div[@class='book']/dl/dd/a/@href").extract()

        if(sections != None):
            book_item["book_intro"] = response.xpath(u"//html/body/div[@id='main']/div[@class='book']/div[@class='description']/p/text()").extract()[0]
            for section in sections:
                yield Request(self.url+section, meta={'book_item': book_item}, callback=self.parse_three)
        else:
            #book_item["section_content"] = response.xpath(u"//html/body/div[@id='main']/div[@class='book']/div[@class='text']/p/text()").extract()[0]
            book_item["section_content"] = response.xpath(u"//html/body/div[@id='main']/div[@class='book']/div[@class='text']").extract()[0]
            book_item["book_intro"] = '无'
            book_item["section_title"] = '无'
            book_item["section_seq"] = 1
            yield book_item

    #获取下一页
    def parse_three(self, response):
        book_item = response.meta['book_item']
        # is_last = response.xpath(u'//a[@href="javascript:alert(\'没有了哦\');"]')
        # if (int(is_last) == 0):
        #     url = response.xpath(u'//div[@class="next"]/a[text()="下一章"]/@href')
        #     yield Request(self.url+url, meta={'book_item': book_item}, callback=self.parse_three)
        #获取标题和排序
        seq_and_title = response.xpath(u'html/body/div/h1').extract()[0]
        result = seq_and_title.split('\.', 1)
        #book_item["section_content"] = response.xpath(u"//html/body/div[@id='container']/div[@class='text']/p/text()").extract()[0]
        #获取章节内容
        book_item["section_content"] = response.xpath(u"//html/body/div[@id='container']/div[@class='text']").extract()[0]
        book_item["section_title"] = result[1]
        book_item["section_seq"] = result[0]

        yield book_item
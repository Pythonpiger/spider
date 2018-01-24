# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import uuid
import sys
from kehuan.items import BookItem
from lxml import html
import re
reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderSpider(scrapy.Spider):

    name = 'spider'
    allowed_domains = ['kehuan.net.cn']
    disk = r'C:/python/book/kehuan'
    url = 'http://www.kehuan.net.cn'
    main_url = 'http://www.kehuan.net.cn/book.html'

    def start_requests(self):
        yield Request(self.main_url, callback=self.parse_one)
        print self.main_url

    #获取作者名称和书名
    def parse_one(self, response):
        headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                'referer': response.url,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
                }
        books = response.xpath("//tr/td[@class='tb']/p").extract()
        for book in books:
            book_item = BookItem()
            book = html.fromstring(book)
            book_item["book_id"] = str(uuid.uuid1())
            book_item["book_name"] = book.xpath(".//a/@title")[0]
            book_item["book_author"] = book.xpath(".//span/a/text()")[0]
            href = book.xpath(".//a/@href")[0]
            yield Request(self.url+href, meta={'book_item': book_item}, callback=self.parse_two, headers=headers)

    #获取书简介内容或者url
    def parse_two(self, response):
        book_item = response.meta['book_item']
        sections = response.xpath(u"//div[@class='book']/dl/dd/a/@href").extract()
        headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                'referer': response.url,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
                }
        if(len(sections) > 0):
            intro = response.xpath(u"//html/body/div[@id='main']/div[@class='book']/div[@class='description']/p/text()").extract()
            if(len(intro) > 0):
                book_item["book_intro"] = intro[0]
            for section in sections:
                yield Request(self.url+section, meta={'book_item': book_item, 'section': section}, callback=self.parse_three, headers=headers)
        else:
            #book_item["section_content"] = response.xpath(u"//html/body/div[@id='main']/div[@class='book']/div[@class='text']/p/text()").extract()[0]
            book_item["section_content"] = response.xpath(u"//html/body/div[@id='main']/div[@class='book']/div[@class='text']").extract()[0].encode('utf-8')
            book_item["book_intro"] = '无'
            book_item["section_title"] = '无'
            book_item["section_seq"] = 1
            yield book_item

    #获取下一页
    def parse_three(self, response):
        book_item = response.meta['book_item']
        section = response.meta['section']
        seq_html = re.split('/', section)[-1]
        seq = re.split('\.', seq_html)[0]
        #获取标题和排序
        seq_and_title = response.xpath(u'//html/body/div/h1').extract()[0].encode('utf-8')
        #获取章节内容
        book_item["section_content"] = response.xpath(u"//html/body/div[@id='container']/div[@class='text']").extract()[0].encode('utf-8')
        book_item["section_title"] = seq_and_title
        book_item["section_seq"] = seq
        yield book_item
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class XiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    siteURL=scrapy.Field() #首页中各MM的URL
    pageURL=scrapy.Field() #每一张图片入口URL
    detailURL=scrapy.Field() #图片原图地址
    title=scrapy.Field()  #MM标题
    fileName=scrapy.Field() #文件夹名，每一个MM一个文件夹
    path=scrapy.Field()  #图片存储路径（绝对路径）

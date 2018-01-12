# -*- coding: utf-8 -*-

import scrapy


class Item(scrapy.Item):
    #标题
    image_title = scrapy.Field()
     #图片Id
    image_id = scrapy.Field()
    #来自哪里
    image_from = scrapy.Field()
    #图片路径（保存在数据库的）
    image_url = scrapy.Field()
    #分类编号
    category_code = scrapy.Field()
    #分类Id
    category_id = scrapy.Field()
    #存储的目录=disk+image_url（磁盘绝对路径）
    path = scrapy.Field()
    #文件名
    file_name = scrapy.Field()

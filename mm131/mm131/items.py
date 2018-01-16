# -*- coding: utf-8 -*-

import scrapy


class Item(scrapy.Item):

    #标题
    image_title = scrapy.Field()
    #图片Id
    image_id = scrapy.Field()
    #来自哪里
    image_from = scrapy.Field()
    #分类编号
    category_code = scrapy.Field()
    #图片保存在数据库的目录
    image_url_dir = scrapy.Field()
    #图片路径（保存在数据库的）
    image_url = scrapy.Field()
    #存储的目录=disk+image_url（磁盘绝对路径）
    dir_path = scrapy.Field()
    #存储的目录=disk+image_url（磁盘绝对路径）+file_name.jpg
    file_path = scrapy.Field()
    #每张图片的访问下载地址
    image_down_url = scrapy.Field()
    #
    image_html = scrapy.Field()

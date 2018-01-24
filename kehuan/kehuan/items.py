# -*- coding: utf-8 -*-
import scrapy


class BookItem(scrapy.Item):

    #书Id
    book_id = scrapy.Field()

    #书名
    book_name = scrapy.Field()

    #书简介
    book_intro = scrapy.Field()

    #书作者
    book_author = scrapy.Field()

    #章节标题
    section_title = scrapy.Field()

    #章节排序
    section_seq = scrapy.Field()

    #章节内容
    section_content = scrapy.Field()
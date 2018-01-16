# -*- coding: utf-8 -*-

class TestPipeline(object):
    def process_item(self, item, spider):
        print 'parse_two图片Id' + item['image_id']
        print 'parse_two图片标题' + item['image_title']
        print 'parse_two图片保存在数据库的目录' + item['image_url']
        print 'parse_two图片存储的目录' + item['file_path']
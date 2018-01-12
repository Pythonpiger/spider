# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#用requests的get方法获取图片并保存入文件
class FilePipeline(object):
    def process_item(self, item, spider):
        detailURL = item['detailURL']
        path = item['path']
        file_name = item['file_name']

        print u'正在保存图片：',detailURL
        print u'图片路径：',path
        print u'文件：',file_name

        image = requests.get(detailURL, timeout=5)
        f = open(path, 'wb')
        try:
            f.write(image.content)
        except Exception,e:
                print u'超时：',file_name
        finally:
            f.close()
        return item
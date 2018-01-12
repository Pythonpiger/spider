# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#用requests的get方法获取图片并保存入文件
class FilePipeline(object):
    def process_item(self, item, spider):
        image_down_url = item['image_down_url']
        path = item['path']

        print u'正在保存图片：',image_down_url
        print u'图片路径：',path

        image = requests.get(image_down_url, timeout=5)
        f = open(path, 'wb')
        try:
            f.write(image.content)
        except Exception,e:
                print u'超时：',image_down_url
        finally:
            f.close()
        return item
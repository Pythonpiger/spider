# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#用requests的get方法获取图片并保存入文件
class FilePipeline(object):
    def process_item(self, item, spider):
        image_down_url = item['image_down_url']
        file_path = item['file_path']

        print '正在保存图片：',image_down_url
        print '图片路径：',file_path
        headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                'referer': item['image_html'],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
                }
        image = requests.get(image_down_url, timeout=5, headers=headers)
        f = open(file_path, 'wb')
        try:
            f.write(image.content)
        except Exception,e:
                print '超时：',image_down_url
        finally:
            f.close()
        return item
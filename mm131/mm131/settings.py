# -*- coding: utf-8 -*-

BOT_NAME = 'mm131'

SPIDER_MODULES = ['mm131.spiders']
NEWSPIDER_MODULE = 'mm131.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#下载延迟
DOWNLOAD_DELAY=0.72
#禁止重试
RETRY_ENABLED = False

FEED_EXPORT_ENCODING = 'utf-8'

#添加请求头
DEFAULT_REQUEST_HEADERS = {
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
      "Accept-Language":"zh-CN,zh;q=0.9",
      "Accept-Encoding":"gzip, deflate",
'referer': 'https://www.mm131.com/*/*',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
}

ITEM_PIPELINES = {
'mm131.mysqlpipelines.MySqlPipeline': 300,
'mm131.filepipelines.FilePipeline': 200,
    #'mm131.testpipelines.TestPipeline': 300,
}

#Mysql数据库的配置信息
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'beautiful_set'        #数据库名字，请修改
MYSQL_USER = 'root'             #数据库账号，请修改
MYSQL_PASSWD = 'root'         #数据库密码，请修改
MYSQL_PORT = 3306               #数据库端口，
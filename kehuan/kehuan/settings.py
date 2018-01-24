# -*- coding: utf-8 -*-
BOT_NAME = 'kehuan'

SPIDER_MODULES = ['kehuan.spiders']
NEWSPIDER_MODULE = 'kehuan.spiders'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 200

FEED_EXPORT_ENCODING = 'utf-8'

#添加请求头
DEFAULT_REQUEST_HEADERS = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Language":"zh-CN,zh;q=0.8",
"Accept-Encoding":"gzip, deflate",
'referer': 'http://www.kehuan.net.cn/',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.25 Safari/537.36',
}

#连接数据库
ITEM_PIPELINES = {
'kehuan.mysqlpipelines.MySqlPipeline': 300,
}

#Mysql数据库的配置信息
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'kehuan'         #数据库名字，请修改
MYSQL_USER = 'root'             #数据库账号，请修改
MYSQL_PASSWD = 'root'           #数据库密码，请修改
MYSQL_PORT = 3306               #数据库端口
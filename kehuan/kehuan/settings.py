# -*- coding: utf-8 -*-
BOT_NAME = 'kehuan'

SPIDER_MODULES = ['kehuan.spiders']
NEWSPIDER_MODULE = 'kehuan.spiders'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 200

#添加请求头
DEFAULT_REQUEST_HEADERS = {
'accept': 'image/webp,*/*;q=0.8',
'accept-language': 'zh-CN,zh;q=0.8',
'referer': 'https://www.kehuan.net.cn/',
'user-agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
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
# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors

class MySqlPipeline(object):

    '''
    异步机制将数据写入到mysql数据库中
    '''
    #创建初始化函数，当通过此类创建对象时首先被调用的方法
    def __init__(self, dbpool):
        self.dbpool=dbpool

    #创建一个静态方法,静态方法的加载内存优先级高于init方法，java的static方法类似，
    #在创建这个类的对之前就已将加载到了内存中，所以init这个方法可以调用这个方法产生的对象
    @classmethod
    def from_settings(cls, settings):
        dbpool=adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"], user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWD"], charset="utf8", cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        #这里不往下传入item,spider，handle_error则不需接受,item,spider)
        query.addErrback(self.handle_error,item,spider)

    def do_insert(self, cursor, item):
        sql = "INSERT INTO image(image_id,image_title,create_time) SELECT %s,%s,NOW() FROM image WHERE not exists (SELECT 1 FROM image WHERE image_id = %s);" \
              "INSERT INTO image_url (image_id,image_url) VALUES (%s,%s);"
        cursor.execute(sql, (item['image_id'], item['image_title'], item['image_id'], item['image_id'], item['image_url']))

    def handle_error(self, failure, item, spider):
        #处理异步插入异常
        print("错误在这里>>>>>>>>>>>>>",failure,"<<<<<<<<<<<<<错误在这里")
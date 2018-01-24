# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
from scrapy import log

class MySqlPipeline(object):

    '''
    异步机制将数据写入到mysql数据库中
    '''
    #创建初始化函数，当通过此类创建对象时首先被调用的方法
    def __init__(self, dbpool):
        self.dbpool = dbpool

    #创建一个静态方法,静态方法的加载内存优先级高于init方法，java的static方法类似，
    #在创建这个类的对之前就已将加载到了内存中，所以init这个方法可以调用这个方法产生的对象
    @classmethod
    def from_settings(cls, settings):
        dbpool=adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"], user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWD"], charset="utf8", cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)
        return cls(dbpool)

    def process_item(self, item, spider):
        for i in item:
             print 'key : ' + i + 'value : ' + str(item[i])
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        #这里不往下传入item,spider，handle_error则不需接受,item,spider)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        try:
            sql = "INSERT INTO book (book_id,book_name,book_intro,book_author) " \
                  "SELECT * FROM(SELECT %s book_id,%s book_name,%s book_intro,%s book_author FROM DUAL) a " \
                  "WHERE NOT EXISTS (SELECT book_id FROM book WHERE book.book_id = a.book_id);"\
                  "INSERT INTO section (book_id,section_title,section_seq,section_content) VALUES (%s,%s,%s,%s);"
            cursor.execute(sql, (item['book_id'], item['book_name'], item['book_intro'], item['book_author']
                            , item['book_id'], item['section_title'], item['section_seq'], item['section_content']
                            ))
        except Exception as e:
            for i in item:
             print 'key : ' + i + 'value : ' + str(item[i])
    def handle_error(self, failure, item, spider):
        #处理异步插入异常
        for i in item:
            print 'key : ' + i + 'value : ' + str(item[i])
        #log.msg('错误在这里', failure, level=log.ERROR)
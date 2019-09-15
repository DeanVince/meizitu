# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymysql import Connect
import re

client = MongoClient("mongodb://root:123456@39.96.63.98:27017/")
col = client["meizitu"]['title']

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'meizitu':
            col.insert(item)
        return item

class MyspiderPipelineMysql(object):


    def process_item(self, item, spider):
        title = item['title']
        href = item['href']
        html = re.findall('.+(a/\d+.html)',href)
        limg_path = item['limg_path']
        tags = item['tags']
        pic_path = item['pic_path']
        save_pics_info_sql = 'insert into pics_info (title,url,tags,limg_path) values (%s,%s,%s,%s)'
        params_pics_info = [title,html,tags,limg_path]
        self.cursor.execute(save_pics_info_sql,params_pics_info)
        id = self.cursor.lastrowid
        self.save_pic_detail(pic_path,id)
        self.conn.commit()
        return item


    def save_pic_detail(self,pic_detail_list,pic_info_id):
        save_pics_detail_sql = 'insert into pic_detail (pic_info_id,pic_path) values (%s,%s)'
        for pic_detail in pic_detail_list:
            params = [pic_info_id,pic_detail]
            self.cursor.execute(save_pics_detail_sql,params)


    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()


    def open_spider(self,spider):

        self.conn = Connect(host='39.96.63.98', port=3306, database='meizitu', user='test',
                    password='123456', charset='utf8')
        self.cursor = self.conn.cursor()
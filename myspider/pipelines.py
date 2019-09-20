# -*- coding: utf-8 -*-
from scrapy.utils.misc import md5sum
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import re,logging
from pymysql import Connect
from fdfs_client.client import Fdfs_client

class MyspiderPipeline(ImagesPipeline):

    def open_spider(self, spider):
        self.spiderinfo = self.SpiderInfo(spider)
        self.client = Fdfs_client(spider.settings.get('FDSF_CONF'))
        self.nginx = spider.settings.get("FDSF_NGINX")

    def get_media_requests(self, item, info):
        for urls in item['image_urls']:
            urls = urls.replace('http://mm.howkuai.com/','https://www.meizitu.com/')
            yield scrapy.Request(urls)


    def item_completed(self, results, item, info):
        # 将下载的图片路径（传入到results中）存储到 image_paths 项目组中，如果其中没有图片，我们将丢弃项目:
        paths = [x['checksum'] for ok, x in results if ok]
        if not paths:
            raise DropItem("Item contains no images")
        item['image_path'] = paths
        return item

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            res = self.client.upload_appender_by_buffer(buf.getvalue(),'jpg')
            if res["Status"] == 'Upload successed.':
                checksum = res.get("Remote file_id")
        return self.nginx + checksum




class SaveSqlPipeline(object):

    def process_item(self, item, spider):
        self.save_pics_info(item)
        self.save_pics_detail(item)
        self.conn.commit()
        return item

    def save_pics_info(self, item):
        url = item['image_path'][0]
        title = item['title']
        tags = item['tags']
        date = item['date']
        params = [url, title, tags, date]
        sql = 'insert into pics_info (url,title,tags,date) values (%s,%s,%s,%s)'
        logging.info(sql % tuple(params))
        self.cursor.execute(sql, params)

    def save_pics_detail(self, item):
        id = self.cursor.lastrowid
        image_urls = item['image_path'][1:]
        for url in image_urls:
            params = [id,url]
            sql = 'insert into pic_detail (pic_info_id,url) values (%s,%s)'
            logging.info(sql % tuple(params))
            self.cursor.execute(sql, params)

    def open_spider(self, spider):
        self.conn = Connect(
            host = spider.settings.get('MYSQL_HOST'),
            port=spider.settings.get('MYSQL_PORT'),
            database=spider.settings.get('MYSQL_DATABASE'),
            user=spider.settings.get('MYSQL_USER'),
            password=spider.settings.get('MYSQL_PASSWORD'),
            charset=spider.settings.get('MYSQL_CHARSET'),
        )
        self.cursor = self.conn.cursor()
    # spider (Spider 对象) – 被开启的spider
    # 可选实现，当spider被开启时，这个方法被调用。

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

# spider (Spider 对象) – 被关闭的spider
# 可选实现，当spider被关闭时，这个方法被调用



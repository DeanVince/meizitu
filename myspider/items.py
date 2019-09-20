# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()  # 图片的下载地址， 该字段是存储图片的列表
    tags = scrapy.Field()  # 关键字
    date = scrapy.Field()  # 日期
    detail_urls = scrapy.Field()  # fdfs链接
    image_path = scrapy.Field()
    title = scrapy.Field()  # 标题
    small_url = scrapy.Field() #缩略图
# -*- coding: utf-8 -*-
import scrapy
from myspider.items import MyspiderItem


class FreebufSpider(scrapy.Spider):
    name = "freebuf"
    allowed_domains = ["freebuf.com"]
    start_urls = ['http://freebuf.com/']

    def parse(self, response):
        self.log(response.headers)
        # 获取 freebuf 首页所有的图片, 以列表形式保存到 image_urls 字段中。
        piclist = response.xpath("//div[@class='news-img']/a/img/@src").extract()
        if piclist:
            item = MyspiderItem()
            item['image_urls'] = piclist
            yield item

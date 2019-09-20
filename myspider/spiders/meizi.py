# -*- coding: utf-8 -*-
import scrapy
import logging
from myspider.items import MyspiderItem
import time
class MeiziSpider(scrapy.Spider):
    name = "meizi"
    allowed_domains = ["meizitu.com",'topmeizi.com',]
    start_urls = [
                  'https://meizitu.com/a/list_1_12.html',
                 ]

    def parse(self, response):
        logging.info("*" * 100)
        logging.info(u"爬虫开始")
        li_list = response.xpath("//ul[@class='wp-list clearfix']//li")
        for li in li_list:
            urls = []
            small_url = li.xpath(".//div[@class='pic']/a/img/@src").extract_first()
            urls.append(small_url)
            item = MyspiderItem()
            item['image_urls'] = urls
            detail_href = li.xpath(".//div[@class='pic']/a/@href").extract_first().replace(
                "http", "https")
            yield scrapy.Request(
                url= detail_href,
                callback=self.parse_detail,
                meta={'item': item},
            )
        next_url = response.xpath(u"//a[text()='下一页1']/@href").extract_first()
        if next_url is not None :

            next_url = 'https://meizitu.com/a/' + next_url
            logging.info("*"*100)
            logging.info("开如睡眠10分钟")
            logging.info(next_url)
            time.sleep(600)
            logging.info("睡眠结束继续爬行")
            logging.info("*"*100)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
        else:
            logging.info("="*100)
            logging.info("--------->spider close<---------")


    def parse_detail(self,response):
        item = response.meta['item']
        img_list = response.xpath("//div[@id='picture']//img/@src").extract()
        item['image_urls'] += img_list
        heads = response.xpath("//div[@class='postmeta  clearfix']")
        item["tags"] = heads.xpath(".//p/text()").extract_first().replace("Tags:", "").replace(
            ", \r\n    ", "")
        item["title"] = heads.xpath(".//h2/a/text()").extract_first()
        day = heads.xpath(".//div[@class='day']/text()").extract_first()
        month_Year = heads.xpath(".//div[@class='month_Year']/text()").extract_first()
        item["date"] = (month_Year + day).replace("\\xa", "")
        yield item



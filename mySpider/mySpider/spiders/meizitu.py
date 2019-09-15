# -*- coding: utf-8 -*-
import scrapy
import requests
import os
import re
import time
import logging
logger = logging.getLogger("__name__")
class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    start_urls = ['https://meizitu.com/a/list_1_1.html']

    def __init__(self):
        self.index = 0

    def parse(self, response):
        li_list = response.xpath("//ul[@class='wp-list clearfix']//li")
        for li in li_list:
            item = {}
            item["title"] = li.xpath(".//h3/a/text()").extract_first()
            if item["title"] == None:
                item["title"] = li.xpath(".//h3/a/b/text()").extract_first()
            item["href"] = li.xpath(".//div[@class='pic']/a/@href").extract_first().replace(
                "http","https")
            limg_src = li.xpath(".//div[@class='pic']/a/img/@src").extract_first()
            limg = re.findall('http://pic.topmeizi.com/wp-content/uploads/(20\d{2}a/\d{2}/\d{2})/('
                              '\w+.jpg)',
                              limg_src)[0]
            if len(limg)==2:
                limg_root = 'limg/' + str(limg[0]).replace('/', '')
                limg_name = limg[1]
                # self.save_img(limg_root,limg_name,limg_src)
                item['limg_path'] = limg_root+"/"+limg_name

            yield scrapy.Request(
                url = item["href"],
                callback = self.parse_detail,
                meta={'item':item}
            )

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        self.index += 1
        if next_url is not None and self.index < 2:
            next_url = 'https://meizitu.com/a/' + next_url
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self,response):
        item = response.meta['item']
        heads = response.xpath("//div[@class='postmeta  clearfix']")
        # item["title"] = heads.xpath(".//a/text()").extract_first()
        item["tags"] = heads.xpath(".//p/text()").extract_first().replace("Tags:","").replace(", \r\n    ","")
        day= heads.xpath(".//div[@class='day']/text()").extract_first()
        month_Year = heads.xpath(".//div[@class='month_Year']/text()").extract_first()
        item["date"] = (month_Year + day).replace("\\xa","")
        img_list = response.xpath("//div[@id='picture']//img")
        pic_path = []
        for img in img_list:
            src = img.xpath("./@src").extract_first()
            path = re.findall('.+/(uploads/)(\d{4}\w/\d{'
                              '2}/\d{2})/(\d+.jpg)',
                              src)[0]
            root= path[0]+path[1].replace('/','')
            name= path[2]
            # self.save_img(root,name,src)
            pic_path.append(root+name)
        item['pic_path'] = pic_path
        yield item


    def save_img(self, root, name, url):
        start = time.time()
        root_name = root + "/" + name
        logging.info("%s 开始保存图片" % root_name)
        content = requests.get(url).content
        if not os.path.exists(root):
            os.makedirs(root)
        with open(root_name, 'wb') as file:
            file.write(content)
        end = time.time()
        logging.info("%s 图片保存完成" % root_name)
        logging.info(end-start)


    def test(self,root,name):
        print(root)
        print(name)
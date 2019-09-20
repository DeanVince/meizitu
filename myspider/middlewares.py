# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

class RandomUserAgentMiddleware:

    def process_request(self,request,spider):
        ua = random.choice(spider.settings.get('USER_AGENT_LIST'))
        request.headers["User-Agent"] = ua


class CheckUserAgent:
    def process_response(self,request,response,spider):
        return response


class AoisolasSpiderMiddleware(object):
     # '''中间键破解防盗链'''
    def process_request(self, request, spider):
        referer = request.url
        if referer :
            request. headers['referer'] = referer
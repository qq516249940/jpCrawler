import scrapy
from scrapy_splash import SplashRequest

import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')



links=list()
links.append("http://jp.tingroom.com/kouyu/ryqjdh")
link_range =range(2,23)


file = open("links.txt",'a')

for num in link_range:
    links.append("http://jp.tingroom.com/kouyu/ryqjdh/list_{num}.html".format(num=num))


import requests
import re
import random


lua_script = '''
function main(splash)                     
    splash:go(splash.args.url)        --打开页面
    splash:wait(3)                    --等待加载
    return splash:html()              --返回页面数据
end
'''

class JpspdSpider(scrapy.Spider):
    name = 'jpspd'
    allowed_domains = ['jd.com']
    start_urls = links[:]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'],
                                callback=self.parse)
    def parse(self, response):
        print("-----------------")
        hrefs = response.xpath('//ul[@class="e2"]/li/a/@href').extract()
        for href in hrefs:
            print(href,file=file)

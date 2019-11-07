import scrapy
from scrapy_splash import SplashRequest

import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')



links=open('links.txt')
#file_to_write = open("export.txt",'a+')
links= links.readlines()

def file_to_write():
    with open('export.txt', 'a+') as f:
      print(f.read())



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
    allowed_domains = ['tingroom.com']
    start_urls = links

    def start_requests(self):
        for url in self.start_urls:
            
            #yield SplashRequest(url=url, callback=self.parse)
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'],
                                callback=self.parse)
    def parse(self, response):
        f"{response.xpath('//title')}"
        contents = response.xpath('//div[@id="article"]/p')

        for content in contents:
            print(content.get())
            if content != '[]':
                print('----------------------------------')
                print(content.extract(),file=file_to_write)

import scrapy
from scrapy_splash import SplashRequest

import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')



links=list()

link_range =range(4563,7072)


file = open("jp.txt",'a')

for num in link_range:
    links.append("http://jp.tingroom.com/kouyu/ryqjdh/{num}.html".format(num=num))



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
    start_urls = links

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'],
                                callback=self.parse)
    def parse(self, response):
        print("-----------------")
        price = response.xpath('//div[@class="content"]').extract_first()
        pos = price.find('</div><div class="content" id="article"><p>')
        if pos:
            print("content：", price[pos:],file=file)
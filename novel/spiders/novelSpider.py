# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import requests

from baseSpider import BaseSpider
from novel.items import NovelItem


class NovelspiderSpider(BaseSpider):
    name = 'novelSpider'
    allowed_domains = ['www.lingdianshuwu.com']
    start_urls = ['https://www.lingdianshuwu.com/','https://www.lingdianshuwu.com/search.asp?searchlist=%s&SearchClass=1']

    def startUrl(self,input_novelName):
        return self.start_urls[1] % urllib.parse.quote(self.input_novelName.encode('gbk'))

    def parseSeachNovel(self, response):
        novel_list = []
        for sel in response.xpath('//span[@class="M"]'):
            title = sel.xpath('a/text()').extract()
            url = sel.xpath('a/@href').extract()
            if len(title) > 0 and len(url) > 0:
                novel_list.append((title[0], self.start_urls[0] + url[0].replace('books', 'contents')))
        return novel_list



    def parseCatalog(self, response):
        catalog = []
        for sel in response.xpath('//table[@class="border"]/tr/td/table/tr/td'):
            title = sel.xpath('a/text()').extract()
            url = sel.xpath('a/@href').extract()
            catalog.append((title[0],self.start_urls[0] + url[0]))

            item = NovelItem()
            item['novelName'] = self.input_novelName
            item['name'] = title[0]
            item['content'] = url[0]
            # item['num'] = url[0]
            yield item

        # for cata in catalog:
        #     yield scrapy.http.Request(url=cata[1], callback=self.parseContent, dont_filter=True)




    novel = {}

    def parseContent(self,response):
        name= response.xpath('// *[ @ id = "content"]/div[1]/b[2]/text()').extract()[0]
        url = u'https://www.lingdianshuwu.com'+response.xpath('//*[@id="content"]/p/script/@src').extract()[0]

        self.novel[url] = name
        return scrapy.http.Request(url=url, callback=self.parse_item, dont_filter=True)


    def parse_item(self,response):
        print('----------------------------------111111--------------------------------------------')
        name = self.novel[response.url]
        content = response.text.encode(response.encoding).decode('gb18030').replace('<br>','\n').replace('&nbsp;','').\
            replace('document.write(\'','').replace('</content>\');','').replace('<content>','')

        item = NovelItem()
        item['novelName'] = self.input_novelName
        item['name'] = name
        item['content'] = content
        yield item

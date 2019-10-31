# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append(r'D:\Scrapy Workspace\ScrapyNovel\novel\spiders')
import urllib.parse
from baseSpider import BaseSpider
from novel.items import NovelItem

import os

#
# curPath = os.path.abspath(os.path.dirname(__file__))
# parentPath = os.path.split(curPath)[0]
# rootPath = os.path.split(parentPath)[0]
# sys.path.append(rootPath)




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
        catalogs = []
        for sel in response.xpath('//table[@class="border"]/tr/td/table/tr/td'):
            title = sel.xpath('a/text()').extract()
            url = sel.xpath('a/@href').extract()
            catalogs.append((title[0],self.start_urls[0] + url[0]))
        return catalogs

    novel = {}
    novelNum = {}

    def parse_content(self,response):
        name= response.xpath('// *[ @ id = "content"]/div[1]/b[2]/text()').extract()[0]
        url = u'https://www.lingdianshuwu.com'+response.xpath('//*[@id="content"]/p/script/@src').extract()[0]

        self.novel[url] = name
        self.novelNum[name] = response.url
        print("parse_content"+str(url))
        return scrapy.http.Request(url=url, callback=self.parse_item, dont_filter=True)


    def parse_item(self,response):
        name = self.novel[response.url]
        content = response.text.encode(response.encoding).decode('gb18030').replace('<br>','\n').replace('&nbsp;','').\
            replace('document.write(\'','').replace('</content>\');','').replace('<content>','')

        item = NovelItem()
        item['novelName'] = self.novelName
        item['name'] = name
        item['num'] = self.novelNum[name]
        item['content'] = content

        print(item)
        yield item

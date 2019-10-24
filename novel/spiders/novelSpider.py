# -*- coding: utf-8 -*-
import scrapy
import urllib.parse


class NovelspiderSpider(scrapy.Spider):
    name = 'novelSpider'
    allowed_domains = ['www.lingdianshuwu.com']
    start_urls = ['http://www.xbiquge.la/']

    def start_requests(self):
        # self.input_novelName = input("请输入小说名：")
        # url = 'https://www.lingdianshuwu.com/search.asp?searchlist=%s&SearchClass=1' % urllib.parse.quote(self.input_novelName.encode('gbk'))
        url = 'https://www.lingdianshuwu.com/search.asp?searchlist=%CA%A5&SearchClass=1'
        # print(url)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        novel = self.getSeachNovel(response)
        print(novel)
        return scrapy.http.Request(url=novel[1], callback=self.parseCatalog, dont_filter=True)



    def selectNovel(self, novel_list):
        for index, novel in enumerate(novel_list):
            print(str(index + 1) + '：' + novel[0])

        return 1;
        index = input("请选择：")
        try:
            index = int(index)
            if (index <= 0 and index > len):
                index = self.selectNovel('请输入正确下载的序号:', len)
        except Exception as e:
            index = self.selectNovel('请输入正确下载的序号:', len)
        return index

    def getSeachNovel(self, response):
        novel_list = []
        for sel in response.xpath('//span[@class="M"]'):
            title = sel.xpath('a/text()').extract()
            url = sel.xpath('a/@href').extract()
            if len(title) > 0 and len(url) > 0:
                novel_list.append((title[0], 'https://www.lingdianshuwu.com/' + url[0].replace('books', 'contents')))

        index = self.selectNovel(novel_list)
        return novel_list[index-1]


    def parseCatalog(self, response):
        catalog = []
        for sel in response.xpath('//table[@class="border"]/tr/td/table/tr/td'):
            title = sel.xpath('a/text()').extract()
            url = sel.xpath('a/@href').extract()
            catalog.append((title[0], url[0]))

        print(catalog)

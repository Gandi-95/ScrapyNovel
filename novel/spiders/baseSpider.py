# -*- coding: utf-8 -*-
import scrapy


class BaseSpider(scrapy.Spider):
    name = 'baseSpider'
    allowed_domains = ['d.com']
    start_urls = ['http://d.com/']

    def startUrl(self, input_novelName):
        pass

    def start_requests(self):
        # self.input_novelName = input("请输入小说名：")
        self.input_novelName = "圣墟"
        url = self.startUrl(self.input_novelName)
        yield scrapy.Request(url=url, callback=self.parse)

    # 解析搜索结果
    def parse(self, response):
        novel = self.getSeachNovel(response)
        self.novelName = novel[0]
        print('parse:'+str(novel))
        return scrapy.http.Request(url=novel[1], callback=self.parse_catalog, dont_filter=True)

    def parseSeachNovel(self, response):
        pass

    def selectNovel(self, novel_list):
        for index, novel in enumerate(novel_list):
            print(str(index + 1) + '：' + novel[0])
        index = input("请选择：")
        try:
            index = int(index)
            if (index <= 0 and index > len):
                index = self.selectNovel('请输入正确下载的序号:', len)
        except Exception as e:
            index = self.selectNovel('请输入正确下载的序号:', len)
        return index

    def getSeachNovel(self, response):
        novel_list = self.parseSeachNovel(response)
        if (len(novel_list) > 0):
            index = self.selectNovel(novel_list)
            return novel_list[index - 1]
        else:
            print('为搜索到%s.' % self.input_novelName)
            self.start_requests()


    def parse_catalog(self,response):
        catalogs = self.parseCatalog(response)
        for catalog in catalogs:
            print('parse_catalog'+str(catalog))
            yield scrapy.http.Request(url=catalog[1], callback=self.parse_content, dont_filter=True)

    def parseCatalog(self,response):
        pass

    def parse_content(self,response):
        pass

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

class NovelPipeline(object):

    def __init__(self):
        self.num_enum = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2
        }
        self.multi_cov = {'百': 100, '十': 10}

        self.content_list = []

    def open_spider(self, spider):
        self.file = open('yuanzun.txt', 'w',encoding='gb18030')

    def process_item(self, item, spider):
        name = item['name']
        # chapter = re.findall(r"第(.*)章", name)[0]
        # item['num'] = self.change2num(chapter)
        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        # list_sorted = sorted(self.content_list, key=lambda x: x['num'])
        list_sorted = sorted(self.content_list,key=lambda x: x['name'])
        for item in list_sorted:
            self.file.write("---------------------------------- %s--------------\n" % (item['name']))
            # self.file.write(''.join(item['content']).replace('\xa0', '') + "\n")
            self.file.write(item['content'])
        self.file.close()

    # 章节数字转换
    def change2num(self, name):
        m = 0
        mc = 1
        rev_name = name[::-1]
        for t_str in rev_name:
            if t_str in self.num_enum:
                m += self.num_enum[t_str] * mc
            if t_str in self.multi_cov:
                mc = self.multi_cov[t_str]
        # 第十二章，第十章特例
        if name[0] == '十':
            m += 10
        return m


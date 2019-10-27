# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class NovelPipeline(object):
    def __init__(self):
        self.num_enum = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2, '千': '', '百': '', '十': '',
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
        }
        self.multi_cov = {'百': '', '十': ''}

        self.content_list = []

    def open_spider(self, spider):
        # self.file = open('yuanzun.txt', 'w',encoding='gb18030')
        pass

    def process_item(self, item, spider):
        chapter = re.findall(r"第(.*)章", item['name'])[0]
        item['num'] = self.convNum(chapter)
        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        self.file = open(self.content_list[0]['novelName'] + '.txt', 'w', encoding='gb18030')
        list_sorted = sorted(self.content_list, key=lambda x: x['num'])
        for item in list_sorted:
            # print(item['name'])
            # self.file.write("\n\n%s\n" % (item['name']))
            self.file.write("\n\n%s---%s\n" % (item['num'],item['name']))
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

    def convNum(self, name):
        listnum = list(name)
        print('---------------')
        print(name)
        num =[]
        for i in listnum:
            if i in self.num_enum.keys():
                num.append(self.num_enum[i])
            # if i in self.num_enum.values():
            #     num.append(i)

        print(num)
        return ''.join('%s' %id for id in num)

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

if __name__ == '__main__':
    num_enum = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2, '千': '', '百': '', '十': '',
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    name = '阳间篇 第1022章 雷震子'
    listnum = list(name)
    print( num_enum.values())
    num = []
    for i in listnum:
        if i in num_enum.keys():
            num.append(num_enum[i])
        if i in num_enum.values():
            num.append(i)

    print(num)
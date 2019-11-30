# -*- coding: utf-8 -*-
import scrapy
import mySettings
"""
    获取一级学科目录并存储到文件 mySettings.FCSI_File 
    格式:{ 代码 : 名称 }
"""


class SubjectsSpider(scrapy.Spider):
    name = 'subjects'

    def start_requests(self):
        url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            list = eval(response.text)
            firstClassSubjectIndex = {item['dm']: item['mc'] for item in list}
            with open(mySettings.FCSI_File, 'w', encoding='utf-8') as f:
                f.write(str(firstClassSubjectIndex))
        except Exception as e:
            print(e)

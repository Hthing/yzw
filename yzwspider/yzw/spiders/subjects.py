# -*- coding: utf-8 -*-
import scrapy
import traceback
import os

"""
    获取一级学科目录并存储到文件 mySettings.FCSI_File 
    格式:{ 代码 : 名称 }
"""


class SubjectsSpider(scrapy.Spider):
    name = 'subjects'
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    custom_settings = {
        'ITEM_PIPELINES': None,
    }

    def start_requests(self):
        url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            list = eval(response.text)
            firstClassSubjectIndex = {item['dm']: item['mc'] for item in list}
            path = os.path.join(self.PROJECT_ROOT, self.settings.get('FCSI_FILE'))
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(firstClassSubjectIndex))
            self.logger.info("一级学科目录抓取完成.")
        except Exception as e:
            self.logger.error(traceback.format_exc())

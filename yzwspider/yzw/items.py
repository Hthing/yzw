# -*- coding: utf-8 -*-
import scrapy


class YzwItem(scrapy.Item):
    id = scrapy.Field()
    招生单位 = scrapy.Field()
    院校特性 = scrapy.Field()
    院系所 = scrapy.Field()
    专业  = scrapy.Field()
    研究方向 = scrapy.Field()
    学习方式 = scrapy.Field()
    拟招生人数 = scrapy.Field()
    备注 = scrapy.Field()
    业务课一 = scrapy.Field()
    业务课二 = scrapy.Field()
    外语 = scrapy.Field()
    政治 = scrapy.Field()
    所在地 = scrapy.Field()
    指导老师 = scrapy.Field()
    专业代码 = scrapy.Field()
    门类 = scrapy.Field()
    一级学科 = scrapy.Field()

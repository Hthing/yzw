# -*- coding: utf-8 -*-
import pymysql
import configparser
import xlwt
import re

import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YzwPipeline(object):

    def open_spider(self,spider):
        self.conf = configparser.ConfigParser()
        self.conf.read('yzw/spiders/schools.ini','utf8')
        if self.conf.get('MySQL','MySQL') == 'True':
            self.d = pymysql.connect(host=self.conf.get('MySQL','host'),
                                     user=self.conf.get('MySQL','user'),
                                     password=self.conf.get('MySQL','password'),
                                     db=self.conf.get('MySQL','database'),
                                     port=self.conf.getint('MySQL','port'),
                                     charset='utf8')
        else:
            self.wbk = xlwt.Workbook()
            self.sheet = self.wbk.add_sheet('Sheet1')
            self.row = 1
            self.sheet.col(0).width = 8000
            self.sheet.col(1).width = 3000
            self.sheet.col(2).width = 10000
            self.sheet.col(3).width = 7000
            self.sheet.col(4).width = 10000
            self.sheet.col(5).width = 7000
            self.sheet.col(6).width = 3000
            self.sheet.col(7).width = 11000
            self.sheet.col(8).width = 4000
            self.sheet.col(9).width = 7000
            self.sheet.col(10).width = 2000
            self.sheet.col(11).width = 2000
            self.sheet.col(12).width = 2000
            self.sheet.col(13).width = 6000
            self.list = ['招生单位', '院校特性', '院系所', '专业', '研究方向', '拟招生人数', '业务课一', '业务课二', '外语', '政治', '所在地','专业代码','门类','一级学科']
            style =  self.excelTitleStyle()

            for i in range(0, 14):
                self.sheet.write(0, i, self.list[i], style)

    def close_spider(self,spider):
        try:
            if self.conf.get('MySQL','MySQL') == 'True':
                self.d.close()
                os.system("shutdown -s -t 0")
            else:
                self.wbk.save(self.conf.get('config','filename')+'.xls')
        except:
            pass


    def process_item(self,item,spider):
        try:

            if self.conf.get('MySQL','MySQL') == 'True':
                self.process_mysql(item)
            else:
                self.process_excel(item)
        except:
            pass
        return item
    def process_mysql(self,item):

        cursor = self.d.cursor()
        sql = "insert into " + self.conf.get('MySQL',
                                             'table') + " VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(
            item['招生单位'], item['院校特性'], item['院系所'], item['专业'], item['研究方向'], item['拟招生人数'], item['业务课一'],
            item['业务课二'], item['外语'], item['政治'], item['所在地'],item['专业代码'],item['门类'],item['一级学科'])

        ret = cursor.execute(sql)
        return ret
    def process_excel(self,item):
        flag = False if (self.row % 2 == 0) else True
        style = xlwt.XFStyle()
        if flag:
            style = self.excelStyle()
        else:
            style = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment = alignment
        for i in range(0,14):
            ret = self.sheet.write(self.row,i,item[self.list[i]],style)
        self.row += 1

    def excelStyle(self):
        style = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 42
        style.pattern = pattern
        borders = xlwt.Borders()
        borders.top = 1
        borders.bottom = 1
        borders.top_colour = 17
        borders.bottom_colour = 17
        style.borders = borders
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alignment

        return style
    def excelTitleStyle(self):
        style = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 17
        style.pattern = pattern
        fnt = xlwt.Font()
        fnt.name = u'黑体'
        fnt.height = 0X00D9
        fnt.colour_index = 1
        fnt.bold = True
        style.font = fnt
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alignment

        return style
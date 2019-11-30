# -*- coding: utf-8 -*-
import pymysql
import xlwt
import mySettings as st
import logging
import os
import sys
from twisted.enterprise import adbapi


class YzwPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=st.host,
            port=st.port,
            db=st.database,
            user=st.user,
            passwd=st.password,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        db_connect_pool = adbapi.ConnectionPool('pymysql', **params)
        obj = cls(db_connect_pool)
        return obj

    def open_spider(self, spider):
        if st.MySQL == 'True':
            pass
        else:
            self.newExcelFile()

    def close_spider(self, spider):
        try:
            if st.MySQL == 'True':
                self.db.close()
                if st.auto_shutdown == 'True':
                    if sys.platform.startswith('linux'):
                        os.system("shutdown 1")
                    elif sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
                        os.system("shutdown -s -t 60")
                    elif sys.platform.startswith('darwin'):
                        os.system("sudo shutdown -h +1")
            else:
                self.wbk.save(st.filename + '.xls')
        except Exception as e:
            logging.error(e)

    def process_item(self, item, spider):
        try:
            if st.MySQL == 'True':
                self.process_mysql(item)
            else:
                self.process_excel(item)
        except Exception as e:
            logging.error(e)
        return item

    def process_mysql(self, item):
        result = self.dbpool.runInteraction(self.insert, item)
        # 给result绑定一个回调函数，用于监听错误信息
        result.addErrback(self.error)

    def insert(self, cursor, item):
        insert_sql = "insert into {0} VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}')" \
                .format(st.table, item['招生单位'], item['院校特性'], item['院系所'], item['专业'], item['研究方向'], item['拟招生人数'],
                        item['业务课一'], item['业务课二'], item['外语'], item['政治'], item['所在地'], item['专业代码'], item['门类'],
                        item['一级学科'])
        cursor.execute(insert_sql)

    def error(self, reason):
        logging.error("insert to database err: -------------\n" + str(reason))

    def process_excel(self, item):
        flag = False if (self.row % 2 == 0) else True
        style = xlwt.XFStyle()
        if flag:
            style = self.getExcelStyle()
        else:
            style = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment = alignment
        for i in range(0, 14):
            ret = self.sheet.write(self.row, i, item[self.list[i]], style)
        self.row += 1

    def getExcelStyle(self):
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

    def getExcelTitleStyle(self):
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

    def newExcelFile(self):
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
        self.list = ['招生单位', '院校特性', '院系所', '专业', '研究方向', '拟招生人数', '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '门类',
                     '一级学科']
        style = self.getExcelTitleStyle()
        for i in range(0, 14):
            self.sheet.write(0, i, self.list[i], style)

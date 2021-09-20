# -*- coding: utf-8 -*-
import pymysql
import xlwt
import logging
import os
from twisted.enterprise import adbapi
import traceback
from yzwspider.yzw.items import YzwItem

logger = logging.getLogger("YzwPipeline")


class YzwPipeline(object):
    def __init__(self, pool, settings):
        self.dbpool = pool
        self.settings = settings
        self.excelstyle = self.getExcelStyle()
        excel_path = os.getcwd() if settings.get("EXCEL_FILE_PATH") == '.' else settings.get("EXCEL_FILE_PATH")
        excel_file = settings.get("EXCEL_FILE_NAME") + '.xls'
        self.excelFile = os.path.join(excel_path, excel_file)

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=settings.get("HOST"),
            port=settings.get("PORT"),
            db=settings.get("DATABASE"),
            user=settings.get("USER"),
            passwd=settings.get("PASSWORD"),
            charset=settings.get("CHARSET"),
            cursorclass=pymysql.cursors.DictCursor
        )
        db_connect_pool = None
        if settings.get("MYSQL"):
            YzwPipeline.__test_mysql_settings(**params)
            db_connect_pool = adbapi.ConnectionPool('pymysql', **params)
        obj = cls(db_connect_pool, settings)
        return obj

    def _create_table(self, txn):
        try:
            sql = "DROP TABLE IF EXISTS `{0}`".format(self.settings.get("TABLE"))
            re = txn.execute(sql)
            sql = self.settings.get("CREATE_TEBLE_SQL").format(self.settings.get("TABLE"))
            re = txn.execute(sql)
            logger.info("创建表:'%s'成功." % self.settings.get('TABLE'))
        except Exception as e:
            logger.critical(traceback.format_exc())

    def open_spider(self, spider):
        if self.dbpool:
            obj = self.dbpool.runInteraction(self._create_table)
        else:
            self.newExcelFile()

    def close_spider(self, spider):
        try:
            if self.dbpool:
                self.dbpool.close()
                logger.info("数据已存储于数据库" + self.settings.get("DATABASE") + "， 表：" + self.settings.get("TABLE"))
            else:
                self.wbk.save(self.excelFile)
                logger.info("excel文件已存储于 " + self.excelFile)
        except Exception as e:
            logger.error(traceback.format_exc())

    def process_item(self, item, spider):
        try:
            if self.dbpool:
                self.process_mysql(item)
            else:
                self.process_excel(item)
        except Exception as e:
            logger.critical(traceback.format_exc())

    def process_mysql(self, item):
        result = self.dbpool.runInteraction(self.insert, item)
        # 给result绑定一个回调函数，用于监听错误信息
        result.addErrback(self.error, item)

    def insert(self, cursor, item):
        insert_sql = self.__make_sql(item)
        cursor.execute(insert_sql)

    def error(self, reason, item):
        # 跳过主键重复error
        if reason.value.args[0] != 1062:
            logger.error(
                "insert to database err: ---------\n" + reason.getErrorMessage() + f"sql=\n{self.__make_sql(item)}")

    def process_excel(self, item):
        flag = False if (self.row & 1 == 0) else True
        style = xlwt.XFStyle()
        if flag:
            style = self.excelstyle
        else:
            style = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment = alignment
        for i in range(0, YzwItem.fields.__len__()):
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
        self.sheet.col(0).width = 3000
        self.sheet.col(1).width = 8000
        self.sheet.col(2).width = 3000
        self.sheet.col(3).width = 10000
        self.sheet.col(4).width = 7000
        self.sheet.col(5).width = 10000
        self.sheet.col(6).width = 7000
        self.sheet.col(7).width = 3000
        self.sheet.col(8).width = 5000
        self.sheet.col(9).width = 11000
        self.sheet.col(10).width = 4000
        self.sheet.col(11).width = 7000
        self.sheet.col(12).width = 2000
        self.sheet.col(13).width = 2000
        self.sheet.col(14).width = 2000
        self.sheet.col(15).width = 2000
        self.sheet.col(16).width = 6000
        self.sheet.col(17).width = 10000
        self.list = ['id', '招生单位', '院校特性', '院系所', '专业', '研究方向', '学习方式', '拟招生人数'
            , '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '指导老师', '门类', '一级学科', '备注']
        style = self.getExcelTitleStyle()
        for i in range(0, YzwItem.fields.__len__()):
            self.sheet.write(0, i, self.list[i], style)

    @staticmethod
    def __test_mysql_settings(**params):
        try:
            db = pymysql.connect(**params)
            db.close()
        except Exception as e:
            logger.critical(str(e))
            os._exit(1)

    def __make_sql(self, item):
        sql = f"""insert into `{self.settings.get('TABLE')}` 
            (`id`, `招生单位`, `院校特性`, `院系所`, `专业`,`研究方向`,`学习方式`, `拟招生人数`, `备注`, `业务课一`, `业务课二`, `外语`, `政治`, `所在地`, `专业代码`,`指导老师`, `门类`, `一级学科` )
             VALUES ('{item['id']}','{item['招生单位']}','{item['院校特性']}','{item['院系所']}','{item['专业']}','{item['研究方向']}',
             '{item['学习方式']}','{item['拟招生人数']}','{item['备注']}','{item['业务课一']}','{item['业务课二']}','{item['外语']}',
             '{item['政治']}','{item['所在地']}', '{item['专业代码']}', '{item['指导老师']}','{item['门类']}','{item['一级学科']}')"""
        # 处理转义字符
        sql = sql.replace("\\'", "\\\\'")
        return sql

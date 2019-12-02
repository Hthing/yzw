#!/usr/bin/python
import argparse
import os
import yzwspider.yzw.start as s
from yzwspider.yzw.settings import PROVINCE_LISE

kwargs = {}


def excel():
    kwargs['MYSQL'] = False
    kwargs['EXCEL_FILE_PATH'] = args.o
    pass


def mysql():
    kwargs['MYSQL'] = True
    kwargs['HOST'] = args.host
    kwargs['USER'] = args.u
    kwargs['PASSWORD'] = args.p
    kwargs['PORT'] = args.port
    kwargs['DATABASE'] = args.db
    kwargs['TABLE'] = args.table



project_root_path = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser()
parser.add_argument('-ssdm', help='省市代码(默认11)', choices=PROVINCE_LISE, metavar='省市代码', default='11')
parser.add_argument('-mldm', help="门类代码(默认01)", choices=[str(i).zfill(2) for i in range(1,14)], metavar='门类代码', default='01')
parser.add_argument('-yjxk', help='一级学科代码(默认0101)', metavar='一级学科代码', default='0101')
parser.add_argument('-log', help='保存日志文件', action='store_true')

# 子命令 mysql  or  excel
subparser = parser.add_subparsers( metavar='输出目标', required=True)
parser_mysql = subparser.add_parser("mysql", help="输出到mysql")
parser_excel = subparser.add_parser("excel", help="输出到excel")

# mysql配置
parser_mysql.add_argument('-host', help='主机地址(localhost)',  metavar='主机地址' , default='localhost')
parser_mysql.add_argument('-port', help='端口(3306)', metavar='端口号', type=int, default=3306)
parser_mysql.add_argument('-u', help='用户名(root)', metavar='用户名', default='root')
parser_mysql.add_argument('-p', help='密码(默认空)', metavar='密码', default='')
parser_mysql.add_argument('-db', help='数据库(yanzhao)', metavar='数据库名', default='yanzhao')
parser_mysql.add_argument('-table', help='数据表(major)', metavar='数据表名', default='major')
parser_mysql.set_defaults(func=mysql)


# excel配置
parser_excel.add_argument('-o', help='输出路径(默认输出至当前目录)', metavar='输出路径', default=os.getcwd())
parser_excel.set_defaults(func=excel)

args = parser.parse_args()
args.func()
kwargs['SSDM'] = args.ssdm
kwargs['MLDM'] = args.mldm
kwargs['YJXKDM'] = args.yjxk
if not args.log: kwargs['LOG_FILE'] = None

s.startup(kwargs)

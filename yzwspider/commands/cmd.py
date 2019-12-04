# -*- coding: utf-8 -*-

import argparse
import os
from yzwspider.yzw.settings import PROVINCE_LISE
import yzwspider.yzw.start as start


def run():
    args = args_parse()
    start.startup(get_settings(args))


def excel_settings(args):
    dict = {}
    dict['MYSQL'] = False
    dict['EXCEL_FILE_PATH'] = args.o
    if args.all is True:
        print("爬取全部信息时请使用mysql")
        exit(0)
    return dict


def mysql_settings(args):
    dict = {}
    dict['MYSQL'] = True
    dict['HOST'] = args.host
    dict['USER'] = args.u
    dict['PASSWORD'] = args.p
    dict['PORT'] = args.port
    dict['DATABASE'] = args.db
    dict['TABLE'] = args.table
    return dict


def general_settings(args):
    dict = {}
    dict['SSDM'] = args.ssdm if args.all is False else ''
    dict['MLDM'] = args.mldm if args.all is False else ''
    dict['YJXKDM'] = args.yjxk if args.all is False else ''
    if not args.log:
        dict['LOG_FILE'] = None
    else:
        print("日志文件将输出至当前目录.")
    return dict


def get_settings(args):
    settings = {}
    settings.update(args.func(args))
    settings.update(general_settings(args))
    return settings


def args_parse():
    usage = """yzwspider [-h] [-ssdm] [-mldm] [-yjxk] [--all] [--log] 输出目标 [其他参数]
              \t例, yzwspider -ssdm 11 -yjxk 0812 excel -o 文件输出路径
              \t    yzwspider -ssdm 11 -yjxk 0812 mysql -p 你的密码 -db 数据库 -table 数据表
              \t    具体参数以及默认值请使用 yzwspider 输出目标 -h 查看
              """
    parser = argparse.ArgumentParser(prog='yzwspider', usage=usage)
    parser.add_argument('-ssdm', help='省市代码(默认11)', choices=PROVINCE_LISE, metavar='省市代码', default='11')
    parser.add_argument('-mldm', help="门类代码(默认01)", choices=[str(i).zfill(2) for i in range(1,14)], metavar='门类代码', default='01')
    parser.add_argument('-yjxk', help='一级学科代码(默认0101)', metavar='一级学科代码', default='0101')
    parser.add_argument('--all', help='爬取全国所有专业并输出到mysql',  action='store_true')
    parser.add_argument('--log', help='保存日志文件', action='store_true')
    sub_parser = parser.add_subparsers(metavar='输出目标', required=True)
    sub_parse(sub_parser)
    args = parser.parse_args()
    return args


def sub_parse(subparser):
    mysql_parse(subparser)
    excel_parse(subparser)


def excel_parse(subparser):
    parser_excel = subparser.add_parser("excel", help="输出到excel")
    parser_excel.add_argument('-o', help='输出路径(默认输出至当前目录)', metavar='输出路径', default=os.getcwd())
    parser_excel.set_defaults(func=excel_settings)


def mysql_parse(subparser):
    parser_mysql = subparser.add_parser("mysql", help="输出到mysql")
    parser_mysql.add_argument('-host', help='主机地址(localhost)', metavar='主机地址', default='localhost')
    parser_mysql.add_argument('-port', help='端口(3306)', metavar='端口号', type=int, default=3306)
    parser_mysql.add_argument('-u', help='用户名(root)', metavar='用户名', default='root')
    parser_mysql.add_argument('-p', help='密码(默认空)', metavar='密码', default='')
    parser_mysql.add_argument('-db', help='数据库(yanzhao)', metavar='数据库名', default='yanzhao')
    parser_mysql.add_argument('-table', help='数据表(major)', metavar='数据表名', default='major')
    parser_mysql.set_defaults(func=mysql_settings)

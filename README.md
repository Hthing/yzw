# yzw
scrapy爬取研招网专业信息

含有考试范围、专业等。
可输出到Excel或MySQL

## 依赖库：  
xlwt  
pymysql  
scrapy

## 运行环境：
python3

## 数据格式：
```
    CREATE TABLE `major` (
  `招生单位` varchar(40) NOT NULL,
  `院校特性` varchar(10) DEFAULT NULL,
  `院系所` varchar(40) DEFAULT NULL,
  `专业` varchar(40) DEFAULT NULL,
  `研究方向` varchar(40) DEFAULT NULL,
  `拟招生人数` varchar(40) DEFAULT NULL,
  `业务课一` varchar(40) DEFAULT NULL,
  `业务课二` varchar(40) DEFAULT NULL,
  `外语` varchar(40) DEFAULT NULL,
  `政治` varchar(40) DEFAULT NULL,
  `所在地` varchar(30) DEFAULT NULL,
  `专业代码` varchar(10) DEFAULT NULL,
  `门类` varchar(20) DEFAULT NULL,
  `一级学科` varchar(40) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8
```
## 使用时修改yzw/spiders/schools.ini


省市代码门类代码等可在http://yz.chsi.com.cn/zsml/queryAction.do 查得

如果写入数据库 将[MySQL]下的MySQL改为True

其他情况默认输出为xls格式
```
[config]
#省市代码 默认11（北京）可为空
ssdm = 11

#门类代码 默认08 （工学）可为空
mldm = 08

#一级学科代码 可为空
yjxkdm = 0812

#若为True 将在使用MySQL情况下完成爬取任务一分钟后自动关机 默认为True ，输出为xls文件时不执行
auto_shutdown = True

#专业名称  可为空
zymc =
[MySQL]
#MySQL = True
MySQL = False
host = localhost
user = root
password = 123456
port = 3306
#数据库数据表 需自行创建
database = yanzhao
table = major
```

## 运行方法：
1. 装好第三方库
2. 根据yzw.sql创建数据表（可选）
3. 修改 schools.ini 文件
3. 进入根目录执行 ```scrapy crawl schools```

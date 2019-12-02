# yzw
scrapy爬取研招网专业信息(末尾有度盘全部数据)

含有考试范围、专业等，可输出到Excel或MySQL。

数据大概这个样子，获得数据之后我们就能方便地进行筛选了。

![图1](https://github.com/Hthing/yzw/blob/master/img/excel.png) 

## 依赖库：  
xlwt  、pymysql  、scrapy

使用下条语句进行安装依赖。

```
pip install xlwt pymysql scrapy
```



## 运行环境：
python3

## 数据格式：

建表sql已存于根目录yzw.sql中。

```mysql
CREATE TABLE `major` (
  `id` char(21) PRIMARY KEY, # id 为爬取页面的id参数+考试范围序号
  `招生单位` varchar(40) NOT NULL,
  `院校特性` varchar(10) DEFAULT NULL,
  `院系所` varchar(40) DEFAULT NULL,
  `专业` varchar(40) DEFAULT NULL,
  `研究方向` TINYTEXT DEFAULT NULL,
  `学习方式` varchar(30) DEFAULT NULL,
  `拟招生人数` varchar(40) DEFAULT NULL,
  `业务课一` varchar(40) DEFAULT NULL,
  `业务课二` varchar(40) DEFAULT NULL,
  `外语` varchar(40) DEFAULT NULL,
  `政治` varchar(40) DEFAULT NULL,
  `所在地` varchar(30) DEFAULT NULL,
  `指导老师` TINYTEXT DEFAULT NULL,
  `专业代码` varchar(10) DEFAULT NULL,
  `门类` varchar(20) DEFAULT NULL,
  `一级学科` varchar(40) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8
```



## 使用方法

### 1. 修改配置

> 使用时修改/schools.ini
>
>
> 省市代码门类代码等可在https://yz.chsi.com.cn/zsml/queryAction.do 查得
>
> 如果写入数据库 将[MySQL]下的MySQL改为True，并修改相应属性
>
> 其他情况默认输出为xls格式
>
> PS. 前4个代码均为空时，共有20W条数据左右，i5笔记本用时1小时左右

```ini
# schools.ini
[config]
#省市代码  可为空
ssdm = 11

#门类代码  可为空
mldm =01

#一级学科代码 可为空
yjxkdm = 0101

#专业名称（精确搜索）  可为空
zymc =

# Excel文件名称
filename = 研招网专业信息

#若为True 将在完成爬取任务一分钟后自动关机
auto_shutdown = False

[MySQL]
# 输出至MySQL， 若为False输出到Excel
MySQL = False
host = localhost
user = root
password = 123456
port = 3306
#数据库数据表 需自行创建
database = yanzhao
table = major
```

> 日志级别以及输出文件在/yzw/settings.py配置
>
> 注释掉LOG_FILE即输出至控制台

```
	settings.py
# 日志级别与输出路径
LOG_LEVEL = 'INFO'
#LOG_FILE = 'log.txt'
```

### 2. 运行

 1. 安装好第三方库。

 2. 根据yzw.sql创建数据表（若输出至Excel则不用）

 3. 修改schools.ini文件

 4. 在项目根目录执行

    ```
    python ./yzw/start.py
    ```

附上最终数据

链接：https://pan.baidu.com/s/1T-ejrTdqMTodA1T2DWU9Dg 
提取码：xt3e

## 爬取页面

​	爬取的页面如下，另外每行数据的id由页面的id以及考试范围顺序组成

​	![图2](https://github.com/Hthing/yzw/blob/master/img/page.png)


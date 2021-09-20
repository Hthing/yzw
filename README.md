# yzw
scrapy爬取研招网研究生考试专业信息

含有考试范围、专业等，可输出到Excel或MySQL。

**[发布页](https://github.com/Hthing/yzw/releases)有爬取好的数据，可用excel或mysql直接查看**

数据大概这个样子，获得数据之后我们就能方便地进行筛选了。

![图1](https://github.com/Hthing/yzw/blob/master/img/excel.png) 

## 安装：  

可直接使用pip自主安装

```
pip install --upgrade yzwspider
python -m yzwspider
```

或者clone到本地使用
```
git clone https://github.com/Hthing/yzw.git
cd yzw
pip install -r requirements.txt
python -m yzwspider
```



## 运行环境：
python3.7以上


## 使用方法

**需提前建立数据库**

省市代码，学科门类，一级学科代码（学科类别） 可在研招网查得。 例，计算机科学与技术：0812

https://yz.chsi.com.cn/zsml/queryAction.do

```
python -m yzwspider [-h] [-ssdm] [-mldm] [-yjxk] [--all] [--log] 输出目标 [其他参数]
```

yzwspider参数： （括号内为默认值）

> **-ssdm**： 省市代码(11)  支持中文名 即北京、上海等, 0表示全国
>
> **-mldm：** 门类代码(01)  支持中文名： 理学、工学等
>
> **-yjxk:**  一级学科代码(0101)
>
> **--all：**爬取全部专业信息并只可输出到mysql
>
> **--log：** 保存日志文件至当前目录
>
> 命令 "excel" 参数：
>
> > **-o：** .xls文件输出路径， 默认为当前目录
>
> 命令 "mysql" 参数：
>
> > **-host：**主机地址(localhost)
> >
> > **-port：**端口号(3306)
> >
> > **-u：**	用户名(root)
> >
> > **-p：**	密码('')
> >
> > **-db：**   数据库名(yanzhao)
> >
> > **-table：**数据表名（major）

例如，我们想获取北京市(11)的计算机科学与技术专业(0812)并输出为excel文件

```
 python -m yzwspider -ssdm 11 -yjxk 0812 excel
```

上条语句可将"-ssdm 11"替换为"-ssdm 北京"同样生效。

最终将会得到如下的信息

```
2019-12-04 15:13:57 [scrapy.core.engine] INFO: Closing spider (finished)
2019-12-04 15:13:57 [YzwPipeline] INFO: excel文件已存储于 /home/研招网专业信息.xls
2019-12-04 15:13:57 [yzwspider.yzw.collector] INFO: 数据抓取完成, 共计 691 条数据，
                    程序开始时间 2019-12-04 15:13:44 , 结束时间 2019-12-04 15:13:57, 耗时 0 分钟
2019-12-04 15:13:57 [scrapy.core.engine] INFO: Spider closed (finished)
```

若输出至mysql（默认参数可以不填）

```
python -m yzwspider -ssdm 11 -yjxk 0812 mysql -u root -p **** -host ******* -table test
```

爬取全国某专业
```
python -m yzwspider  -ssdm 0 -yjxk 0812 mysql -u *** -p ***
```

输出信息类似于excel.  如果想保存日志则加上--log即可







## 爬取页面

​	爬取的页面如下，另外每行数据的id由页面的id以及考试范围顺序组成

​	![图2](https://github.com/Hthing/yzw/blob/master/img/page.png)


# -*- coding: utf-8 -*-
import scrapy
import re
import configparser

class SchoolsSpider(scrapy.Spider):
    name = 'schools'
    provinceList = ['11','12','13','14','15','21','22','23','31','32','33','34','35','36','37',
                   '41','42','43','44','45','46','50','51','52','53','54','61','62','63','64','65','71','81','82']
    dict = {'35': '福建', '21': '辽宁', '51': '四川', '34': '安徽', '63': '青海', '42': '湖北', '64': '宁夏', '33': '浙江', '46': '海南',
     '82': '台湾', '61': '陕西', '37': '山东', '41': '河南', '13': '河北', '45': '广西', '54': '西藏', '14': '山西', '81': '澳门',
     '36': '江西', '52': '贵州', '50': '重庆', '44': '广东', '32': '江苏', '53': '云南', '71': '香港', '11': '北京', '31': '上海',
     '23': '黑龙江', '62': '甘肃', '22': '吉林', '65': '新疆', '43': '湖南', '15': '内蒙古', '12': '天津'}
    list_985 = ["北京大学", "清华大学", "中国科学技术大学", "南京大学", "复旦大学", "上海交通大学", "西安交通大学", "浙江大学", "哈尔滨工业大学", "北京理工大学", "南开大学", "天津大学", "东南大学", "武汉大学", "华中科技大学", "吉林大学", "厦门大学", "山东大学", "中国海洋大学", "湖南大学", "中南大学", "大连理工大学", "北京航空航天大学", "重庆大学", "四川大学", "电子科技大学", "中山大学", "华南理工大学", "兰州大学", "西北工业大学", "东北大学", "同济大学", "北京师范大学", "中国人民大学", "中国农业大学", "国防科技大学", "中央民族大学", "华东师范大学", "西北农林科技大学"]
    list_211 = ["北京大学", "中国人民大学", "清华大学", "北京交通大学", "北京工业大学", "北京航空航天大学", "北京理工大学", "北京科技大学", "北京化工大学", "北京邮电大学", "中国农业大学", "北京林业大学", "北京中医药大学", "北京师范大学", "北京外国语大学", "中国传媒大学", "中央财经大学", "对外经济贸易大学", "北京体育大学", "中央音乐学院", "中央民族大学", "中国政法大学", "华北电力大学", "华北电力大学(保定)", "南开大学", "天津大学", "天津医科大学", "河北工业大学", "太原理工大学", "内蒙古大学", "辽宁大学", "大连理工大学", "东北大学", "大连海事大学", "吉林大学", "延边大学", "东北师范大学", "哈尔滨工业大学", "哈尔滨工程大学", "东北农业大学", "东北林业大学", "复旦大学", "同济大学", "上海交通大学", "华东理工大学", "东华大学", "华东师范大学", "上海外国语大学", "上海财经大学", "上海大学", "第二军医大学", "南京大学", "苏州大学", "东南大学", "南京航空航天大学", "南京理工大学", "中国矿业大学", "中国矿业大学(北京)", "河海大学", "江南大学", "南京农业大学", "中国药科大学", "南京师范大学", "浙江大学", "安徽大学", "中国科学技术大学", "合肥工业大学", "厦门大学", "福州大学", "南昌大学", "山东大学", "中国海洋大学", "中国石油大学", "中国石油大学(华东)", "中国石油大学(北京)",  "郑州大学", "武汉大学", "华中科技大学", "中国地质大学","中国地质大学(北京)", "中国地质大学(武汉)", "武汉理工大学", "华中农业大学", "华中师范大学", "中南财经政法大学", "湖南大学", "中南大学", "湖南师范大学", "国防科学技术大学", "中山大学", "暨南大学", "华南理工大学", "华南师范大学", "广西大学", "海南大学", "四川大学", "西南交通大学", "电子科技大学", "四川农业大学", "西南财经大学", "重庆大学", "西南大学", "贵州大学", "云南大学", "西藏大学", "西北大学", "西安交通大学", "西北工业大学", "西安电子科技大学", "长安大学", "西北农林科技大学", "陕西师范大学", "第四军医大学", "兰州大学", "青海大学", "宁夏大学", "新疆大学", "石河子大学"]
    list_not_selfLine = ["国防科技大学", "中央民族大学", "华东师范大学", "西北农林科技大学"]

    conf = configparser.ConfigParser()
    conf.read('yzw/spiders/schools.ini','utf8')
    ssdm = conf.get('config','ssdm')
    mldm = conf.get('config','mldm')
    yjxkdm = conf.get('config','yjxkdm')
    zymc = conf.get('config','zymc')
    allowed_domains = ['chsi.com.cn']
    subjectIndex = {'06': '历史学', '12': '管理学', '07': '理学', '03': '法学', '08': '工学', '13': '艺术学', '10': '医学', '11': '军事学','05': '文学', '04': '教育学', '01': '哲学', '09': '农学', '02': '经济学'}
    f = open("firstClassSubjectIndex.txt", 'r',encoding='utf-8')
    firstClassSubjectIndex = eval(f.read())
    f.close()
    if ssdm == '' :
        start_urls = []
        for i in provinceList:
            start_urls.append('http://yz.chsi.com.cn/zsml/queryAction.do?ssdm='+i+
                          '&dwmc=&mldm='+mldm+'&mlmc=&yjxkdm='+yjxkdm+'&xxfs=&zymc='+zymc+'&pageno=1')
    else:
        start_urls = ['http://yz.chsi.com.cn/zsml/queryAction.do?ssdm='+ssdm+
                          '&dwmc=&mldm='+mldm+'&mlmc=&yjxkdm='+yjxkdm+'&xxfs=&zymc='+zymc+'&pageno=1']

    def parse(self,response):

        for tr in response.xpath('//tbody/tr'):
            try:
                schName = tr.xpath('.//a[re:test(@href,"/zsml/querySchAction.do?")]/text()').extract()[0][7:]
                flag = ''
                if schName in self.list_211:
                    flag = '211'
                    if schName in self.list_985:
                        flag = '985'
                        if schName not in self.list_not_selfLine:
                            flag = '985自划线院校'
                url = re.sub(r'queryAction','querySchAction',response.url)
                url = re.sub(r'dwmc=','dwmc='+schName,url)
                yield scrapy.Request(url,meta={'flag':flag},callback=self.parse_school)
            except Exception as e:
                self.logger.error(e)
                continue

        page = response.xpath('//div[re:test(@class,"zsml-page-box")]/ul/li').css('a::attr(onclick)').extract()
        page = page[len(page) - 1]
        flag = response.xpath('//li[re:test(@class,"lip unable ")]').css('li::attr(class)').extract()
        if flag == [] or flag == ['lip unable lip-first']:
            try:
                nextPage = re.findall(r'\(.*?\)',page)[0][1:-1]
                url = re.sub(r'pageno=\d*','pageno='+nextPage ,response.url)
                yield scrapy.Request(url,callback=self.parse)
            except Exception as e:
                self.logger.error(e)
                pass

    def parse_school(self,response):
        majorInfo = response.css('table').css('tr')
        n = len(majorInfo)
        for i in range(1,n):
            try:
                str = majorInfo[i].css('td::text')[2].extract()
                majorCode = re.findall(r'\(.*?\)',str)[0][1:-1]
                url = 'http://yz.chsi.com.cn' + majorInfo[i].css('td')[7].css('a::attr(href)')[0].extract()
                yield scrapy.Request(url,meta={'url':response.url,
                                               'flag':response.meta['flag'],
                                               'majorCode':majorCode},
                                     callback=self.parse_major)
            except Exception as e:
                self.logger.error(e)
                continue

        page = response.xpath('//div[re:test(@class,"zsml-page-box")]/ul/li').css('a::attr(onclick)').extract()
        page = page[len(page)-1]
        flag = response.xpath('//li[re:test(@class,"lip unable ")]').css('li::attr(class)').extract()
        if flag == [] or flag == ['lip unable lip-first']:
            try:
                nextPage = re.findall(r'\(.*?\)',page)[0][1:-1]
                url = re.sub(r'pageno=\d*','pageno='+nextPage ,response.url)
                yield scrapy.Request(url,meta={'flag':response.meta['flag']},callback=self.parse_school)
            except Exception as e:
                self.logger.error(e)
                pass


    def parse_major(self,response):
        majorDict = {}
        province = re.findall('ssdm=\d+', response.meta['url'])[0][5:]
        majorInfo = response.css('table')[0].css('tr')
        testRange = response.xpath('//tbody[re:test(@class,"zsml-res-items")]')
        for test in testRange:
            majorDict['招生单位'] = majorInfo[0].css('td::text')[1].extract()
            majorDict['院系所'] = majorInfo[1].css('td::text')[1].extract()
            majorDict['专业'] = majorInfo[2].css('td::text')[1].extract()
            majorDict['研究方向'] = majorInfo[3].css('td::text')[1].extract()
            majorDict['拟招生人数'] = majorInfo[4].css('td::text')[1].extract()
            majorDict['政治'] = re.sub(r'\s','',test.css('td::text')[0].extract())
            majorDict['外语'] = re.sub(r'\s','',test.css('td::text')[2].extract())
            majorDict['业务课一'] = re.sub(r'\s','',test.css('td::text')[3].extract())
            majorDict['业务课二'] = re.sub(r'\s','',test.css('td::text')[4].extract())
            majorDict['所在地'] = self.dict[province]
            majorDict['院校特性'] = response.meta['flag']
            majorDict['专业代码'] = response.meta['majorCode']
            majorDict['门类'] = self.subjectIndex[response.meta['majorCode'][:2]]
            majorDict['一级学科'] = self.firstClassSubjectIndex[response.meta['majorCode'][:4]]
            self.logger.info(majorDict)
            yield majorDict

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
                flag = tr.xpath('.//span/text()').extract()
                if flag:
                    flag = flag[0]
                else:
                    flag = ''
                schName = tr.xpath('.//a[re:test(@href,"/zsml/querySchAction.do?")]/text()').extract()[0][7:]
                url = re.sub(r'queryAction','querySchAction',response.url)
                url = re.sub(r'dwmc=','dwmc='+schName,url)
                yield scrapy.Request(url,meta={'flag':flag},callback=self.parse_school)
            except:
                continue

        page = response.xpath('//div[re:test(@class,"zsml-page-box")]/ul/li').css('a::attr(onclick)').extract()
        page = page[len(page) - 1]
        flag = response.xpath('//li[re:test(@class,"lip unable ")]').css('li::attr(class)').extract()
        if flag == [] or flag == ['lip unable lip-first']:
            try:
                nextPage = re.findall(r'\(.*?\)',page)[0][1:-1]
                url = re.sub(r'pageno=\d*','pageno='+nextPage ,response.url)
                yield scrapy.Request(url,callback=self.parse)
            except:
                pass

    def parse_school(self,response):
        majorInfo = response.css('table').css('tr')
        n = len(majorInfo)
        for i in range(1,n):
            try:
                str = majorInfo[i].css('td::text')[1].extract()
                majorCode = re.findall(r'\(.*?\)',str)[0][1:-1]
                url = 'http://yz.chsi.com.cn' + majorInfo[i].css('td')[6].css('a::attr(href)')[0].extract()
                yield scrapy.Request(url,meta={'url':response.url,
                                               'flag':response.meta['flag'],
                                               'majorCode':majorCode},
                                     callback=self.parse_major)
            except:
                continue

        page = response.xpath('//div[re:test(@class,"zsml-page-box")]/ul/li').css('a::attr(onclick)').extract()
        page = page[len(page)-1]
        flag = response.xpath('//li[re:test(@class,"lip unable ")]').css('li::attr(class)').extract()
        if flag == [] or flag == ['lip unable lip-first']:
            try:
                nextPage = re.findall(r'\(.*?\)',page)[0][1:-1]
                url = re.sub(r'pageno=\d*','pageno='+nextPage ,response.url)
                yield scrapy.Request(url,meta={'flag':response.meta['flag']},callback=self.parse_school)
            except:
                pass


    def parse_major(self,response):
        majorDict = {}
        province = re.findall('ssdm=\d+', response.meta['url'])[0][5:]
        majorInfo = response.css('table')[0]
        testRange = response.xpath('//tbody[re:test(@class,"zsml-res-items")]')
        for test in testRange:
            majorDict['招生单位'] = majorInfo.css('tr')[0].css('td::text')[1].extract()
            majorDict['院系所'] = majorInfo.css('tr')[1].css('td::text')[1].extract()
            majorDict['专业'] = majorInfo.css('tr')[2].css('td::text')[1].extract()
            majorDict['研究方向'] = majorInfo.css('tr')[3].css('td::text')[1].extract()
            majorDict['拟招生人数'] = majorInfo.css('tr')[4].css('td::text')[1].extract()
            majorDict['政治'] = re.sub(r'\s','',test.css('td::text')[0].extract())
            majorDict['外语'] = re.sub(r'\s','',test.css('td::text')[2].extract())
            majorDict['业务课一'] = re.sub(r'\s','',test.css('td::text')[3].extract())
            majorDict['业务课二'] = re.sub(r'\s','',test.css('td::text')[4].extract())
            majorDict['所在地'] = self.dict[province]
            majorDict['院校特性'] = response.meta['flag']
            majorDict['专业代码'] = response.meta['majorCode']
            majorDict['门类'] = self.subjectIndex[response.meta['majorCode'][:2]]
            majorDict['一级学科'] = self.firstClassSubjectIndex[response.meta['majorCode'][:4]]
            yield majorDict

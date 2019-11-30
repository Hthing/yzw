# -*- coding: utf-8 -*-
import scrapy
import re
import mySettings as st
import traceback
from items import YzwItem



class SchoolsSpider(scrapy.Spider):
    name = 'schools'
    allowed_domains = ['chsi.com.cn']
    start_urls = []
    firstClassSubjectIndex = {}

    def start_requests(self):
        with open(st.FCSI_File, 'r', encoding='utf-8') as f:
            self.firstClassSubjectIndex = eval(f.read())
        gen = self.__ssdm_yjxk(st.ssdm, st.yjxkdm)
        for ssdm, yjxkdm in gen:
            url =  'https://yz.chsi.com.cn/zsml/queryAction.do?ssdm={}&dwmc=&mldm={}&mlmc=&yjxkdm={}&xxfs=&zymc={}&pageno=1'\
                .format(ssdm, st.mldm, yjxkdm, st.zymc)
            yield scrapy.Request(url, meta={'ssdm':ssdm}, callback=self.parse)

    # 爬取学校目录
    def parse(self, response):
        for tr in response.xpath('//tbody/tr'):
            try:
                schName = tr.xpath('.//a[re:test(@href,"/zsml/querySchAction.do?")]/text()').extract()[0][7:]
                schFeature = self.__getSchoolFeature(schName)
                url = re.sub(r'queryAction', 'querySchAction', response.url)
                url = re.sub(r'dwmc=', 'dwmc=' + schName, url)
                yield scrapy.Request(url, meta={'ssdm':response.meta['ssdm']}, callback=self.parse_school)
            except Exception as e:
                self.logger.error(traceback.format_exc(e))
                continue
        # 翻页
        url = self.__nextPageUrl(response)
        if url:
            yield scrapy.Request(url, meta={'ssdm':response.meta['ssdm']}, callback=self.parse)

    # 爬取学校页面专业信息
    def parse_school(self, response):
        majorInfo = response.css('table').css('tr')
        n = len(majorInfo)
        for i in range(1, n):
            try:
                str = majorInfo[i].css('td::text')[2].extract()
                majorCode = re.findall(r'\(.*?\)', str)[0][1:-1]
                url = 'https://yz.chsi.com.cn' + majorInfo[i].css('td')[7].css('a::attr(href)')[0].extract()
                yield scrapy.Request(url, meta={'ssdm':response.meta['ssdm']}, callback=self.parse_major)
            except Exception as e:
                self.logger.error(traceback.format_exc(e))
                continue
        # 翻页
        url = self.__nextPageUrl(response)
        if url:
            yield scrapy.Request(url, meta={'ssdm':response.meta['ssdm']}, callback=self.parse_school)

    # 爬取专业信息
    def parse_major(self, response):
        try:
            majorDict = {}
            province = response.meta['ssdm']
            majorInfo = response.css('table')[0].css('tr')
            examRange = response.xpath('//tbody[re:test(@class,"zsml-res-items")]')
            for num in range(0,len(examRange)):
                body = examRange[num]
                majorDict['id'] = response.url[-19:] + str(num+1).zfill(2)
                majorDict['招生单位'] = majorInfo[0].css('td::text')[1].extract()[7:]
                majorDict['院校特性'] = self.__getSchoolFeature(majorDict['招生单位'])
                majorDict['院系所'] = majorInfo[1].css('td::text')[1].extract()[5:]
                majorDict['专业'] = majorInfo[2].css('td::text')[1].extract()
                majorDict['研究方向'] = majorInfo[3].css('td::text')[1].extract()
                majorDict['学习方式'] = majorInfo[2].css('td::text')[3].extract()
                majorDict['拟招生人数'] = majorInfo[4].css('td::text')[1].extract()
                majorDict['政治'] = re.sub(r'\s', '', body.css('td::text')[0].extract())
                majorDict['外语'] = re.sub(r'\s', '', body.css('td::text')[2].extract())
                majorDict['业务课一'] = re.sub(r'\s', '', body.css('td::text')[3].extract())
                majorDict['业务课二'] = re.sub(r'\s', '', body.css('td::text')[4].extract())
                majorDict['所在地'] = st.dict[province]
                majorDict['指导老师'] = majorInfo[3].xpath('td')[3].xpath('text()').extract()
                majorDict['指导老师'] = majorDict['指导老师'][0] if majorDict['指导老师'] else ''
                majorDict['专业代码'] = majorDict['专业'][1:7]
                majorDict['门类'] = st.subjectIndex[majorDict['专业代码'][:2]]
                majorDict['一级学科'] = self.firstClassSubjectIndex[majorDict['专业代码'][:4]]
                self.logger.info(majorDict)
                yield majorDict
        except Exception as e:
            self.logger.error(traceback.format_exc(e))

    # 生成省市代码， 一级学科代码
    def __ssdm_yjxk(self, ssdm, yjxkdm):
        if yjxkdm == '' and ssdm == '':
            for province in st.provinceList:
                for key in self.firstClassSubjectIndex.keys():
                    if str(key).startswith(st.mldm): yield province, key
        elif yjxkdm == '':
            for key in self.firstClassSubjectIndex.keys():
                if str(key).startswith(st.mldm): yield ssdm, key
        elif ssdm == '':
            for province in st.provinceList: yield province, yjxkdm
        else:
            yield ssdm, yjxkdm

    # 判断学校性质
    def __getSchoolFeature(self, schName):
        feature = ''
        if schName in st.list_211:
            feature = '211'
            if schName in st.list_985:
                feature = '985'
        return feature

    # 获取下一页url
    def __nextPageUrl(self, response):
        url = ''
        page = response.xpath('//div[re:test(@class,"zsml-page-box")]/ul/li').css('a::attr(onclick)').extract()
        page = page[len(page) - 1]
        pageButtonLabel = response.xpath('//li[re:test(@class,"lip unable ")]').css('li::attr(class)').extract()
        # 非最后一页
        if pageButtonLabel == [] or pageButtonLabel == ['lip unable lip-first']:
            try:
                nextPage = re.findall(r'\(.*?\)', page)[0][1:-1]
                url = re.sub(r'pageno=\d*', 'pageno=' + nextPage, response.url)
            except Exception as e:
                self.logger.error(traceback.format_exc(e))
        return url


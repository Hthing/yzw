# -*- coding: utf-8 -*-
import scrapy
import re
import os
import traceback
from yzwspider.yzw.items import YzwItem


class SchoolsSpider(scrapy.Spider):
    name = 'schools'
    allowed_domains = ['chsi.com.cn']
    start_urls = []
    firstClassSubjectIndex = {}
    st = {}
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    custom_settings = {
        'STATS_CLASS': 'yzwspider.yzw.collector.YzwCollector',
    }

    def start_requests(self):
        self.st = {i : self.settings.attributes[i].value for i in self.settings.attributes.keys() }
        path = os.path.join(self.PROJECT_ROOT, self.settings.get('FCSI_FILE'))
        with open(path, 'r', encoding='utf-8') as f:
            self.firstClassSubjectIndex = eval(f.read())
        gen = self.__ssdm_yjxk(self.settings.get('SSDM'), self.settings.get('YJXKDM'))
        for ssdm, yjxkdm in gen:
            url =  'https://yz.chsi.com.cn/zsml/queryAction.do?ssdm={}&dwmc=&mldm={}&mlmc=&yjxkdm={}&pageno=1'\
                .format(ssdm, self.settings.get('MLDM'), yjxkdm)
            yield scrapy.Request(url, meta={'ssdm':ssdm}, callback=self.parse)

    # 爬取学校目录
    def parse(self, response):
        for tr in response.xpath('//tbody/tr[not(@class="noResult")]'):
            try:
                school = tr.xpath('.//a[re:test(@href,"/zsml/querySchAction.do?")]/text()').get()
                schName = school[7:]
                url = re.sub(r'queryAction', 'querySchAction', response.url)
                url = re.sub(r'dwmc=', 'dwmc=' + schName, url)
                yield scrapy.Request(url, meta={'ssdm':response.meta['ssdm']}, callback=self.parse_school)
            except Exception as e:
                self.logger.error(f"爬取学校目录错误. url={response.url}")
                continue
        # 翻页
        url = self.__next_page_url(response)
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
                self.logger.error(f"爬取学校页面错误. url={response.url}")
                continue
        # 翻页
        url = self.__next_page_url(response)
        if url:
            yield scrapy.Request(url, meta={'ssdm':response.meta['ssdm']}, callback=self.parse_school)

    # 爬取专业信息
    def parse_major(self, response):
        try:
            item = YzwItem()
            province = response.meta['ssdm']
            majorInfo = response.css('table')[0].css('tr')
            examRange = response.xpath('//tbody[re:test(@class,"zsml-res-items")]')
            for num in range(0,len(examRange)):
                body = examRange[num]
                item['id'] = response.url[-19:] + str(num+1).zfill(3)
                item['招生单位'] = majorInfo[0].css('td::text')[1].extract()[7:]
                item['院校特性'] = self.__getSchoolFeature(item['招生单位'])
                item['院系所'] = majorInfo[1].css('td::text')[1].extract()[5:]
                item['专业'] = majorInfo[1].css('td::text')[3].extract()
                item['学习方式'] = majorInfo[2].css('td::text')[1].extract()
                item['研究方向'] = majorInfo[2].css('td::text')[3].extract()
                item['指导老师'] = majorInfo[3].css('td.zsml-summary')[0].css('::text').get()
                item['指导老师'] = item['指导老师'] if item['指导老师'] else ''
                item['拟招生人数'] = majorInfo[3].css('td.zsml-summary')[1].css('::text').get()
                comments = majorInfo[4].css('.zsml-bz::text')
                item['备注'] = comments[1].get() if len(comments) > 1 else ""
                item['政治'] = re.sub(r'\s', '', body.css('td::text')[0].extract())
                item['外语'] = re.sub(r'\s', '', body.css('td::text')[2].extract())
                item['业务课一'] = re.sub(r'\s', '', body.css('td::text')[3].extract())
                item['业务课二'] = re.sub(r'\s', '', body.css('td::text')[4].extract())
                item['所在地'] = self.settings.get('PROVINCE_DICT')[province]
                item['专业代码'] = item['专业'][1:7]
                item['门类'] = self.settings.get('SUBJECT_INDEX')[item['专业代码'][:2]]
                item['一级学科'] = self.firstClassSubjectIndex[item['专业代码'][:4]]
                self.logger.info(item)
                yield item
        except Exception as e:
            self.logger.error(f"爬取专业信息错误. url={response.url}")

    # 生成省市代码， 一级学科代码
    def __ssdm_yjxk(self, ssdm, yjxkdm):
        if yjxkdm == '' and ssdm == '':
            for province in self.settings.get('PROVINCE_LISE'):
                for key in self.firstClassSubjectIndex.keys():
                    if str(key).startswith(self.settings.get('MLDM')): yield province, key
        elif yjxkdm == '':
            for key in self.firstClassSubjectIndex.keys():
                if str(key).startswith(self.settings.get('MLDM')): yield ssdm, key
        elif ssdm == '':
            for province in self.settings.get('PROVINCE_LISE'): yield province, yjxkdm
        else:
            yield ssdm, yjxkdm

    # 判断学校性质
    def __getSchoolFeature(self, schName):
        return self.settings.get('SCHOOL_FEATURE').get(schName, "")

    # 获取下一页url
    def __next_page_url(self, response):
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
                self.logger.error(traceback.format_exc())
        return url


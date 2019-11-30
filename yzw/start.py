#!/usr/bin/python
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from spiders import subjects
from spiders import schools
from scrapy.utils.log import configure_logging

configure_logging()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(subjects.SubjectsSpider)
    yield runner.crawl(schools.SchoolsSpider)
    reactor.stop()

crawl()
reactor.run()

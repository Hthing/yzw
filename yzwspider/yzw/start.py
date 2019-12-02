#!/usr/bin/python
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from yzwspider.yzw.spiders import schools, subjects
from scrapy.utils.log import configure_logging
from twisted.python import log
import logging


def startup():
    configure_logging()
    runner = CrawlerRunner(get_project_settings())


    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(subjects.SubjectsSpider)
        yield runner.crawl(schools.SchoolsSpider)
        reactor.stop()

    logging.basicConfig(level=logging.INFO, filemode='w', filename='log.txt')
    observer = log.PythonLoggingObserver()
    observer.start()
    crawl()
    reactor.run()

if __name__ == '__main__':
    startup()
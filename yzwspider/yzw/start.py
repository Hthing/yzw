#!/usr/bin/python
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from yzwspider.yzw.spiders import schools, subjects
from scrapy.utils.log import configure_logging
import os

def startup(my_settings={}):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'yzwspider.yzw.settings')
    settings = get_project_settings()
    for key, value in my_settings.items():
        settings.attributes[key].value = value
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(subjects.SubjectsSpider)
        yield runner.crawl(schools.SchoolsSpider)
        reactor.stop()

    crawl()
    reactor.run()


if __name__ == '__main__':
    startup()

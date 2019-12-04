# -*- coding: utf-8 -*-
from scrapy.statscollectors import MemoryStatsCollector
import logging
import pprint

logger = logging.getLogger(__name__)


class YzwCollector(MemoryStatsCollector):

    def __init__(self, crawler):
        super(YzwCollector, self).__init__(crawler)

    def close_spider(self, spider, reason):
        if self._dump:
            start_time = self._stats['start_time']
            finish_time = self._stats['finish_time']
            if self._stats['finish_reason'] == 'finished':
                logger.info("""数据抓取完成, 共计 {0} 条数据，
                    程序开始时间 {1} , 结束时间 {2}, 耗时 {3} 分钟"""
                            .format(self._stats['item_scraped_count'],
                                start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                finish_time.strftime('%Y-%m-%d %H:%M:%S'),
                                int((finish_time - start_time).seconds / 60))
                            )
            else:
                logger.info("异常终止:\n" + pprint.pformat(self._stats),
                        extra={'spider': spider})
        self._persist_stats(self._stats, spider)

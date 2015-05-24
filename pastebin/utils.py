from scrapy import log
from scrapy import logformatter

class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': log.DEBUG,
            'format': logformatter.DROPPEDFMT,
            'exception': exception,
            'item': item,
        }
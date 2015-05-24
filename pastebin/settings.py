# -*- coding: utf-8 -*-

# Scrapy settings for pastebin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
BOT_NAME = 'pastebin'

SPIDER_MODULES = ['pastebin.spiders']
NEWSPIDER_MODULE = 'pastebin.spiders'

LOG_LEVEL = 'INFO'

# less verbose logger
LOG_FORMATTER = 'pastebin.utils.PoliteLogFormatter'

ITEM_PIPELINES = {
    'pastebin.pipelines.FilterPipeline': 300,
    'pastebin.pipelines.TextToFilePipeline': 400,
}
FILES_STORE = 'pastes'

FEED_FORMAT = 'csv'

# for pastebin.pipelines.FilterPipeline
REGEXES = [r'scrapy', r'arch\s+linux']

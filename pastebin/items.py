# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

class Paste(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    creation_date = scrapy.Field()
    syntax = scrapy.Field()
    text = scrapy.Field()
    matches = scrapy.Field()

    # for file pipeline
    file_path = scrapy.Field()

class PasteLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = Paste

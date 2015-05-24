# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.utils.url import urljoin_rfc

from pastebin.items import PasteLoader


class BasicSpider(scrapy.Spider):
    name = 'pastebin_latest'
    allowed_domains = ['pastebin.com']
    start_urls = (
        'http://pastebin.com/archive',
    )

    def __init__(self, limit=None):
        self.last_paste = ''
        self.limit = int(limit) if limit else None

        # get url of the last processed paste
        try:
            with open('last_paste') as f:
                self.last_paste = f.read().strip()
        except:
            self.last_paste = ''

    def parse(self, response):
        # retrieve urls of pastes on page
        rel_urls = response.css('.maintable td:first-child a').xpath('@href').extract()
        pastes_urls = [urljoin_rfc(response.url, url) for url in rel_urls]

        # limit urls if specified
        if self.limit:
            pastes_urls = pastes_urls[:self.limit]

        # cut off processed pastes
        try:
            pastes_urls = pastes_urls[:pastes_urls.index(self.last_paste)]
        except ValueError:
            pass

        # save url of the last paste
        if pastes_urls:
            with open('last_paste', 'w') as f:
                f.write(pastes_urls[0])

        self.log('Acquired new pastes: %s' % len(pastes_urls), scrapy.log.INFO)

        for url in pastes_urls:
            yield scrapy.http.Request(url, self.parse_paste_page)

    def parse_paste_page(self, response):
        l = PasteLoader(response=response);

        l.add_value('url', response.url)
        l.add_css('text', 'textarea#paste_code::text')
        l.add_xpath('text', 'string(//*[@id="selectable"]/div)')
        l.add_css('title', '.paste_box_line1 h1::text')
        l.add_css('syntax', '.paste_box_line2 a::text')
        l.add_css('creation_date', '.paste_box_line2 span::attr(title)')

        return l.load_item()

# -*- coding: utf-8 -*-
import os
import re
from urllib2 import urlopen
from datetime import datetime

import scrapy
from scrapy.exceptions import DropItem
from twisted.web import client

import pastebin.settings as s

class FilePipeline():
    '''downloads file specified in the file_url field and places it inside FILES_STORE directory'''

    def __init__(self):
        if os.path.exists(s.FILES_STORE):
            if not os.path.isdir(s.FILES_STORE):
                raise Exception('FILES_STORE is not a directory')
        else:
            os.mkdir(s.FILES_STORE)

    def process_item(self, item, spider):
        fname = self.get_filename(item, spider)
        fpath = os.path.join(s.FILES_STORE, fname)

        item['file_path'] = fpath

        d = client.downloadPage(item['file_url'], fpath)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)

        return d

        # urllib2 method
        # try:
        #     with open(fpath, 'w') as f:
        #         f.write(urlopen(item['file_url']).read())
        # except Exception as e:
        #     self._handle_error(e, item, spider)

        # return item

    def get_filename(self, item, spider):
        fname = item['file_url'].split('/')
        while not fname[-1]:
            fname.pop()
        return fname[-1]

    def _handle_error(self, failure, item, spider):
        item['file_path'] = 'Error occurred: %s' % failure
        spider.log('Fail to download %s:\n    %s' % (item['file_url'], failure), scrapy.log.WARNING)

class FileFilterPipeline():
    '''
    filters items based on the content of the acquired file specified in the file_path field
    fills "matches" field
    removes unmatched files
    '''

    def __init__(self):
        self.compiled = [re.compile(expr, re.I) for expr in s.REGEXES]

    def process_item(self, item, spider):
        if os.path.exists(item['file_path']):
            with open(item['file_path']) as f:
                raw_paste = f.read();

            item['matches'] = []

            for expr in self.compiled:
                if expr.search(raw_paste):
                    item['matches'].append(expr.pattern)

            if not item['matches']:
                os.remove(item['file_path'])
                raise DropItem('No matches')
            else:
                spider.log('Match: %s' % item['matches'], scrapy.log.INFO)

        return item

class TextToFilePipeline(FilePipeline):
    '''
    saves content of the "text" field to a file
    removes "text" field
    '''

    def process_item(self, item, spider):
        fname = self.get_filename(item, spider)
        fpath = os.path.join(s.FILES_STORE, fname)

        item['file_path'] = fpath

        try:
            with open(fpath, 'w') as f:
                f.write(item['text'].encode('UTF-8'))
        except Exception as e:
            spider.log('Fail to save text:\n    %s' % e, scrapy.log.WARNING)

        item.pop('text')

        return item

    def get_filename(self, item, spider):
        fname = item['url'].split('/')
        while not fname[-1]:
            fname.pop()
        return fname[-1]

class FilterPipeline():
    '''
    filters items based on the content of the "text" field
    fills "matches" field
    '''

    def __init__(self):
        self.compiled = [re.compile(expr, re.I) for expr in s.REGEXES]

    def process_item(self, item, spider):
        if not item['text']:
            return item

        item['matches'] = []

        for expr in self.compiled:
            if expr.search(item['text']):
                item['matches'].append(expr.pattern)

        if not item['matches']:
            raise DropItem('No matches')
        else:
            spider.log('Match: %s' % item['matches'], scrapy.log.INFO)

        return item

from os import name
from bs4.element import Tag
import re
import inspect
import json
import requests
from bs4 import BeautifulSoup
from contextlib import suppress

class Operation:
    """
    """

    def __init__(self):
        self.name = ''
        self.direct_url = ''
        self.related_url = ''
        self.extracted_meaning = ''
        self.aliases = []
        self.tags = []
        self.short_desc_url = ''
        self.short_desc = ''
        self.full_desc = ''

    def to_json(self):
        raw_attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        clean_attributes = [
            a for a in raw_attributes if not(a[0].startswith('_') or a[0].endswith('__'))
        ]

        return {attr[0]: attr[1] for attr in clean_attributes}


    def find_link(self):
        pass


    def enrich(self):
        if self.short_desc_url:
            short = json.loads(requests.get(self.short_desc_url).text)
            self.short_desc = short.get('extract')

        if self.direct_url:
            try:
                self.full_desc = self.get_text_from_html(self.direct_url)
            except ConnectionAbortedError:
                self.full_desc = 'ERROR_LOADING_PAGE'
            except Exception as ex:
                raise ex

    def get_text_from_html(self, url):
        full = requests.get(self.direct_url)
        soup = BeautifulSoup(full.text, 'html.parser')
        found_text = ''
        if 'wikipedia' in url:
            doc = soup.find_all('div', {'class': 'mw-parser-output'})
            if doc:
                found_text = doc[0].text
        
        return found_text


    def __normalize(self):
        name_rgx = '\(.+\)'
        roman_rgx = '[IVXLCDM]+$'
        self.name = re.sub(re.compile(name_rgx), '', self.name)
        #self.name = re.sub(re.compile(roman_rgx), '', self.name)
        self.name = self.name.strip()

        if self.direct_url:
            self.direct_url = 'https://pt.wikipedia.org' + self.direct_url 
            if '&action' in self.direct_url: 
                self.direct_url = self.direct_url.split('&action')[0]
            if '?title' in self.direct_url:
                self.direct_url = self.direct_url.replace('w/index.php?title=', 'wiki/')

            self.short_desc_url = 'https://pt.wikipedia.org/api/rest_v1/page/summary' + self.direct_url.split('/wiki')[1]

        self.aliases = [
            re.sub(r'^\s?ou\s', '', a).split('(')[0].replace(',', '').strip() for a in self.aliases
        ]
        self.aliases = list(set([a for a in self.aliases if a]))


    def mount_from_bs4(self, bs4_tag, reference_tags):
        for c in bs4_tag.contents:
            if isinstance(c, str) and not self.name:
                self.name = c
            elif isinstance(c, str) and self.name:
                self.aliases.append(c)
            else:
                if 'href' in c.attrs:
                    self.direct_url = c.attrs['href']
                    if isinstance(c.next, str):
                        self.name = c.next
                    else:
                        self.name = c.attrs['title']
                elif c.name == 'sup':
                    self.related_url = c.next['href'].replace('#', '')
            
            if c.parent.parent.parent.name == 'li':
                self.aliases.append(c.parent.parent.parent.contents[0].next)          

        if self.related_url:
            with suppress(KeyError):
                self.related_url = reference_tags[self.related_url]

        self.__normalize()
        return self
        



        
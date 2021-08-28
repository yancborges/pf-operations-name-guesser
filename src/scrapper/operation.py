from os import name
from bs4.element import Tag
import re
import inspect

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


    def to_json(self):
        raw_attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        clean_attributes = [
            a for a in raw_attributes if not(a[0].startswith('_') or a[0].endswith('__'))
        ]

        return {attr[0]: attr[1] for attr in clean_attributes}


    def __normalize(self):
        name_rgx = '\(.+\)'
        roman_rgx = '[IVXLCDM]+$'
        self.name = re.sub(re.compile(name_rgx), '', self.name)
        #self.name = re.sub(re.compile(roman_rgx), '', self.name)
        self.name = self.name.strip()

        self.aliases = [
            re.sub(r'^\s?ou\s', '', a).split('(')[0].replace(',', '').strip() for a in self.aliases
        ]
        self.aliases = list(set([a for a in self.aliases if a]))


    def mount_from_bs4(self, bs4_tag):
        for c in bs4_tag.contents:
            if isinstance(c, str) and not self.name:
                self.name = c
            elif isinstance(c, str) and self.name:
                self.aliases.append(c)
            else:
                if 'href' in c.attrs:
                    self.direct_url = c.attrs['href']
                    self.name = c.attrs['title']
                elif c.name == 'sup':
                    self.related_url = c.next['href']
            
            if c.parent.parent.parent.name == 'li':
                self.aliases.append(c.parent.parent.parent.contents[0].next)          

        self.__normalize()
        return self
        



        
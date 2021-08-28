from os import name
from bs4.element import Tag
import re

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


    def __normalize(self):
        name_rgx = '\([\w\s\d]+\)'
        roman_rgx = '[IVXLCDM]+$'
        self.name = re.sub(re.compile(name_rgx), self.name, '')
        self.name = re.sub(re.compile(roman_rgx), self.name, '')


    def mount_from_bs4(self, bs4_tag):
        for c in bs4_tag.contents:
            if isinstance(c, str):
                self.name = c
            else:
                if 'href' in c.attrs:
                    self.name = c.next
                    self.direct_url = c.attrs['href']
                else:
                    self.name = c.parent.contents[0].next
                    if c.name == 'sup':
                        self.related_url = c.next['href']

        self.__normalize()
        



        
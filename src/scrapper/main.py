from bs4 import BeautifulSoup
import bs4
import requests
from operation import Operation
import pandas as pd


def mount_references(bs4_source):
    refs = bs4_source.find_all('cite')
    j_refs = {}
    for item in refs:
        _id = item.parent.parent.attrs['id']
        _link = None
        for c in item.contents:
            if c.name == 'a':
                _link = c.attrs['href']
                break
        j_refs[_id] = _link
    
    return j_refs


def scrap_page():
    """
    """

    url = 'https://pt.wikipedia.org/wiki/Lista_de_opera%C3%A7%C3%B5es_da_Pol%C3%ADcia_Federal_do_Brasil#cite_note-245'
    raw_content =  BeautifulSoup(requests.get(url).text, 'html.parser')
    operations = []
    items = raw_content.find_all('li')
    references = mount_references(raw_content)

    # Keeping only the resources i've mapped
    items = [
        i for i in items 
            if not i.attrs 
            and (
                (
                    'style' in i.parent.parent.attrs 
                    and i.parent.parent.attrs['style'].startswith('-moz-column-count')
                )
                or
                (
                    'class' in i.parent.parent.attrs
                    and i.parent.parent.attrs['class'] == ['mw-parser-output']
                )
                or
                (
                    i.parent.name == 'ul'
                    and i.parent.parent.name == 'li'
                )
            )
            and not (
                'class' in i.parent.attrs
                and i.parent.attrs['class'] == 'references'
            )
    ]
    for i in items:
        operations.append(
            Operation().mount_from_bs4(i, references)
        )

    return operations

operations = scrap_page()
json_operations = operations
for o in operations:
    o.enrich()
pd.DataFrame(json_operations).to_csv('pf_operations.csv', sep=',')


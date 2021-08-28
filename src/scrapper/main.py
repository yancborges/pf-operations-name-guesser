from bs4 import BeautifulSoup
import requests
from operation import Operation
import pandas as pd

def scrap_page():
    """
    """

    url = 'https://pt.wikipedia.org/wiki/Lista_de_opera%C3%A7%C3%B5es_da_Pol%C3%ADcia_Federal_do_Brasil#cite_note-245'
    raw_content =  BeautifulSoup(requests.get(url).text, 'html.parser')
    operations = []
    items = raw_content.find_all('li')

    # Ignoring elements with any HTML attribute set
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
            Operation().mount_from_bs4(i)
        )

    return operations

operations = [i.to_json() for i in scrap_page()]
pd.DataFrame(operations).to_csv('pf_operations.csv', sep=',')

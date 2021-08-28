from bs4 import BeautifulSoup
import requests
from operation import Operation

def scrap_page():
    """
    """

    url = 'https://pt.wikipedia.org/wiki/Lista_de_opera%C3%A7%C3%B5es_da_Pol%C3%ADcia_Federal_do_Brasil#cite_note-245'
    raw_content =  BeautifulSoup(requests.get(url).text, 'html.parser')
    operations = []
    items = raw_content.find_all('li')

    # Ignoring elements with any HTML attribute set
    items = [i for i in items if not i.attrs]
    for i in items:
        operations.append(
            Operation().mount_from_bs4(i)
        )

scrap_page()
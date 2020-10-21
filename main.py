import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://en.wikipedia.org'
start_page = {"page": f"{base_url}/wiki/Small"}


def fix_links(not_full_url):
    not_full_url = dict(not_full_url)
    for i in range(len(not_full_url)):
        if not_full_url[list(not_full_url.keys())[i]] and not (
                'https' in not_full_url[list(not_full_url.keys())[i]] or 'http' in not_full_url[
            list(not_full_url.keys())[i]]):
            not_full_url[list(not_full_url.keys())[i]] = base_url + not_full_url[
                list(not_full_url.keys())[i]]
    return not_full_url


def parse_wiki(wiki_pages, num):
    wiki_pages = dict(wiki_pages)

    page = requests.get(list(wiki_pages.values())[num])
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup is not None:
        for link in soup.findAll('a'):
            if len(wiki_pages) < 1000:
                wiki_pages[link.text] = link.get('href')
            else:
                break
    wiki_pages = fix_links(wiki_pages)
    if len(wiki_pages) < 1000:
        return parse_wiki(wiki_pages, num + 1)
    else:
        return to_json(dict(wiki_pages))


def to_json(dictionary):
    json.dump(dictionary, open("result.json", "w"))
    print(f'Parsed! Amount of links: {len(dictionary)}')


parse_wiki(start_page, 0)

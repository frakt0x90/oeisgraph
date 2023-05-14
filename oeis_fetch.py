#NOTE: This is not actually async. It's just sync with extra work.
# I might try to fix it but we'll see.

import requests
import asyncio
from bs4 import BeautifulSoup
from tinydb import TinyDB
from typing import Set, List, Dict
from re import match, findall
from oeisutil import int_to_oeis_seq


async def get_seq_page(seq_id: str) -> str:
    resp = requests.get(f'https://oeis.org/{seq_id}')
    if resp.status_code == 200:
        print(f'got {seq_id}')
        return BeautifulSoup(resp.content)
    raise(ValueError(f'{seq_id} not found'))

async def gather_data(oeis_id) -> Dict[str, List[str]]:
    parsed_html = await get_seq_page(oeis_id)
    links = get_links(parsed_html)
    keywords = get_keywords(parsed_html)
    return {oeis_id: {'links': links, 'keywords': keywords}}

async def insert_data(db: TinyDB, oeis_id: str) -> None:
    persistence_obj = await gather_data(oeis_id)
    db.insert(persistence_obj)
    print(f'{oeis_id} done')

def get_links(parsed_html: BeautifulSoup) -> Set[str]:
    links = []
    for link in parsed_html.find_all('a'):
        address = link.get('href')
        if match(r'/A\d{6}$', address):
            links.append(address[1:])
    return list(set(links))

def get_keywords(parsed_html: BeautifulSoup) -> List[str]:
    return [element.text for element in parsed_html.find("p", class_="Seq SeqK").find_all('span')]

def get_last_entry(seq_db: TinyDB) -> int:
    data = seq_db.all()
    latest_oeis = max([list(dic.keys())[0] for dic in data])
    return int(latest_oeis[1:])

async def collect_entries():
    db = TinyDB('sequences.json')
    SEQ_START = get_last_entry(db) + 1
    SEQ_END = 361525  #as of 2023-03-25

    for seq_id in range(SEQ_START, SEQ_END + 1):
        oeis_id = int_to_oeis_seq(seq_id)
        retries = 0
        try:
            await insert_data(db, oeis_id)
        except ValueError:
            print(f'{oeis_id} failed')
            retries += 1
            if retries >= 5:
                break
            continue
        retries = 0
    
asyncio.run(collect_entries())

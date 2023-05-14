import concurrent.futures
import requests as r


MAX_THREADS = 4
urls = ["http://scrapingbee.com/blog", "http://reddit.com/","http://www.bankier.pl/","http://www.onet.pl"]

def scrape(url):
    print(f"calling: {url}")
    res = r.get(url)
    print(f"Done: {res.status_code}")
    return res

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    res = executor.map(scrape, urls)
    for r in res:
        print(r.status_code)
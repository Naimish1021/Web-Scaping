from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

for i in range(1,23):
    req = Request(f'https://near-me.store/sitemap_{str(i)}.xml', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'xml')
    for j in soup.find_all('loc'):
        with open('titles.txt','a') as f:
            title = j.text.replace('https://near-me.store/en/','').replace('-',' ').capitalize()
            print(title)
            f.write(title+'\n')

    print(len(soup.find_all('loc')))
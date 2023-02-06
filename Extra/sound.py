import mysql.connector as mysql
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os

mydb = mysql.connect(host="php.cpgava.org", user="sound", passwd="password", db="sound")
mycursor = mydb.cursor()

base_site = 'https://www.myinstants.com'
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
r = Request(base_site,headers=headers) 
soup = BeautifulSoup(urlopen(r).read(), 'html.parser')

tags =[]
cats = []
for cat in soup.find_all('ul',class_='dropdown-menu')[0].find_all('li'):
    cats.append(cat.text)
    tags.append(cat.find('a').get('href'))

def sound_saver(buttons,i):
    query = 'INSERT INTO `sound`(`title`, `path`, `cat`) VALUES (%s,%s,%s)'
    print(f'{i} - saving sounds')
    for button in buttons:
        link = button.get('onclick').replace("play('",'').replace("')",'')
        name = link.split('/')[-1]
        path = f'sound/{i}/{name}'
        title = button.get('title').replace('Play','').replace('sound','')
        req = Request(f'{base_site}{link}', headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        with open(path,'wb') as f:
            f.write(webpage)
        mycursor.execute(query,(title,path,i))
        mydb.commit()
    return None

def next_page(link,cat,tag):
    print(f'{cat} - {tag} {link}')
    req = Request(f'{base_site}{tag}{link}', headers=headers)
    
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    buttons = soup.find_all('button',class_='small-button')
    sound_saver(buttons,cat)
    
    try:
        next_link = soup.find_all('a',text='Next page')[0].get('href')
        if not next_link.endswith('#'):
            print(f'{next_link}')
            next_link = next_link[:-1].replace(' ','%20')
            return next_page(next_link,cat,tag)
        return None
    except AttributeError:
        return None

for i,j in zip(cats,tags):
    directory = f'sound/{i}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    req = Request(f'{base_site}{j}', headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    buttons = soup.find_all('button',class_='small-button')
    next_page_url = soup.find('a',text='Next page').get('href').replace(' ','%20')
    sound_saver(buttons,i)
    # next_page(next_page_url,i,j)

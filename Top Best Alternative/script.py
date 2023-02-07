
import sys

from bs4 import BeautifulSoup
import requests
import csv
import re

from threading import Thread

import contextlib


from time import sleep
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless") 
options.add_argument('--no-sandbox') 
options.add_argument('disable-infobars')
options.add_argument('--disable-gpu')
options.add_argument("--disable-extensions")
options.add_argument("--log-level=3")
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chromedriver_autoinstaller.install()  


base_url = 'https://www.topbestalternatives.com'


def save_image_from_url(url,type):
	if url.startswith('/'):
		url = base_url + url
	r = requests.get(url)
	if r.status_code == 200:
		path = f'media/{type}/' + url.split('/')[-1]
		with open(path, 'wb') as f:
			f.write(r.content)
			return path
	return ' '

def save(url):
	global KEYS_COUNT,MAX_KEY_COUNT,Expired_key,base_url

	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')
	
	content = soup.find('div',attrs={'class':'product-header'})
	product_link = soup.find_all('div',attrs={'class':'product-links'})
	name=content.find('h2').text

	count = int(soup.find('title').text.split(' ')[0])
	
	if count>50 or count!= len(soup.find_all('section',class_='section app')):
		try:
			driver = webdriver.Chrome(options=options)
			driver.get(url)
			for _ in range(count//50):
				sleep(5)
				driver.execute_script("document.getElementsByClassName('btn-load-more')[0].click()")
				sleep(10)
			soup = BeautifulSoup(driver.page_source,'html.parser')
			driver.close()
		except:
			pass	


	desc = content.find('div',attrs={'class':'product-description'}).text.replace('? Read More','')
	license = '-'
	with contextlib.suppress(Exception):
		license = content.find('div',attrs={'class':'license'}).text
	
	logo = '-'
	with contextlib.suppress(Exception):
		logo = save_image_from_url(content.find('div',attrs={ 'class':'logo'}).find('img')['src'],'logo')

	link = '-'
	with contextlib.suppress(Exception):
		link = product_link[1].find('a',attrs={'class':'btn-website'})['href']

	f_link = '-'
	with contextlib.suppress(Exception):
		f_link = product_link[1].find('a',attrs={'class':'btn-facebook'})['href']

	t_link = '-'
	with contextlib.suppress(Exception):
		t_link = product_link[1].find('a',attrs={'class':'btn-twitter'})['href']

	i_link = '-'
	with contextlib.suppress(Exception):
		i_link = product_link[1].find('a',attrs={'class':'btn-instagram'})['href']

	p_link = '-'
	with contextlib.suppress(Exception):
		p_link = product_link[1].find('a',attrs={'class':'btn-pinterest'})['href']

	g_link = '-'
	with contextlib.suppress(Exception):
		g_link = product_link[1].find('a',attrs={'class':'btn-github'})['href']

	y_link = '-'
	with contextlib.suppress(Exception):
		y_link = product_link[1].find('a',attrs={'class':'btn-youtube'})['href']

	r_link = '-'
	with contextlib.suppress(Exception):
		r_link = product_link[1].find('a',attrs={'class':'btn-reddit'})['href']
	
	categorys = '-'
	with contextlib.suppress(Exception):
		categorys =','.join([i.text for i in  product_link[0].find_all('a')])

	images = '-'
	with contextlib.suppress(Exception):
		images =','.join([save_image_from_url(i['src'],'ss') for i in soup.find('div',attrs={'class':'gallery-content'}).find_all('img')])
		
	alts = '-'
	with contextlib.suppress(Exception):
		alts=','.join([re.sub(r'\#\d+\s','',j.text) for j in soup.find_all('h3')])

	return [name,logo,categorys,license,desc,link,f_link,t_link,i_link,p_link,y_link,r_link,g_link,alts,images]
		
	
head = ['name','logo','cats','license','desc','link','f_link','t_link','i_link','p_link','y_link','r_lin','g_link','alternatives','images']
with open('urls.csv','r') as urls_file:
	reader = csv.reader(urls_file,delimiter=',')
	url_page = list(reader)
	
with open('data.csv','w',newline='',encoding='utf-8') as f:
	writer = csv.writer(f)
	writer.writerow(head)
	for i in url_page:
		try:			
			writer.writerow(save(i[0]))
			print(f'{i[0]} saved')
		except Exception as e:
			print(e)
			print(f'{i[0]} failed')


			

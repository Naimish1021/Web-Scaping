from turtle import title
import openai 
import random
import time
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from threading import Thread
import re

KEYS = ['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',
				'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']
User_Agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
			'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			]
# as much  as key declare here 

	 
def gpt3(stext, key=random.choice(KEYS)):
		openai.api_key = key  
		response = openai.Completion.create(
				engine="text-davinci-002",
				prompt=stext,
				temperature=0.8,
				max_tokens=3020,
				top_p=1,
				frequency_penalty=0,
				presence_penalty=0

		)
		time.sleep(1)
		return response.choices[0].text


def get_soup(url):
	
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
	webpage = urlopen(req).read()
	page_soup = soup(webpage, "html.parser")
	data =  page_soup.find_all('table')[5].find_all('tr')[1].find_all('td')[1] 
	title = data.find('h1').text
	return title, get_content(child=data)

def get_p_generated(text):
	content = ''
	for t in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.replace('\n','')):
		if t.replace(' ','') != '':
			# query = f'Rephrase this in own word{t}'
			# response = gpt3(query)
			# response =  response.replace('\n',' ')
			content = f'{content} { t}'
	return content

def get_p(i):
	content = ''
	if i.text.replace(' ','') != '':
		content = ' <p>'
		# for j in i.contents:
		# 	if j.name =='b':
		# 		content = f'{content} <{j.name}> {get_p_generated(j.text)} </{j.name}>'
		content = f'{content}  {get_p_generated(i.text)} '
		content = f'{content} </p>'
	return content

def get_list(ul):
	content = ''
   
	for j in ul.contents:
		if j.text!='\n' and j.text.replace(' ','').replace('\n','') != '':
			if j.name == 'li' :
				
				if len(j.text) >= 50:
					content = f'{content}<li>{get_p_generated(j.text)}</li>'
				else:
					content = f'{content}<li>{j.text}</li>'
					
			elif j.name in ['ul','ol']:
				content = f'{content} <{j.name}> {get_list(j)} </{j.name}>'
			else:
				content = f'{content} {j}' 
			
	return content

def get_content(child=None):
		
	content=''
	
	for i in child.contents:
		if i.name is not None:
			# print(i.name)
			if i.name in ['h2','h3']  :
				content = f'{content}<{i.name}>{i.text}</{i.name}>'           

			elif i.name == 'p' and  len(i.text) > 5: 
				content = f'{content}{get_p(i=i)}'
				
			elif i.name in ['ol','ul'] :                  
				content = f'{content} <{i.name}> {get_list(i)} </{i.name}>'

	return content

def bill(url,j):
	# try:
		j,i = get_soup(url)
		with open('needhelppaying_data.csv', 'a',newline='\n',encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow([j,i])
		return 0
	# except:
	# 	with open('needhelppaying_not_saved_data.csv', 'a',newline='\n',encoding='utf-8') as f:
	# 		writer = csv.writer(f)
	# 		writer.writerow([j,url])
# please change file name according to your use
try:
	try:
		with open('needhelppaying_data.csv','r') as f: #this is checking for already file having saved url or not
			reader = csv.reader(f)
			entry = len(list(reader))
	except Exception:
		entry = 0

	if entry == 0:	
		with open('needhelppaying_data.csv', 'a',newline='\n',encoding='utf-8') as f: #this is checking for already file having saved url or not
			writer = csv.writer(f)
			writer.writerow(['title','content'])

	# this is file of urls
	with open('needhelppaying.csv','r') as f: 
		reader = csv.reader(f)
		urls = list(reader)

	no_of_thead = 10 # now change thread from here
	urls_list = []
	for i in range(entry,len(urls)-(len(urls)%no_of_thead),no_of_thead):   
		ls = [j[0] for j in urls[i:i+no_of_thead]] 
		urls_list.append(ls)
	
	for j,i in enumerate( urls_list):
		thread = [Thread(target=bill, args=(url,j)) for url in i]
		
		for i in thread:
			i.start()
		for i in thread:
			i.join()
		
		print(f'{(j+1)*no_of_thead} complated')
	
	
except KeyboardInterrupt:
	exit()

except Exception as e:
	print(e)
	# 245,https://www.needhelppayingbills.com/html/bartow_county_assistance_progr.html

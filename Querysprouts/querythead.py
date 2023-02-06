from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import csv
import openai
import time
from threading import Thread
import random

KEYS = ['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','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' ] #add your  openai keys here 

def gpt3(stext):
	openai.api_key = random.choice(KEYS) #'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'
	response = openai.Completion.create(
		engine="text-davinci-002",
		prompt=stext,
				temperature=0.8,
				max_tokens=3020,
				top_p=1,
				frequency_penalty=0,
				presence_penalty=0

	)
	time.sleep(0.5 )
	return response.choices[0].text



def scraping(url):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
		req = Request(url , headers=headers)

		webpage = urlopen(req).read()
		page_soup = soup(webpage, "html.parser")
		title = page_soup.find('h1').text
		cat = page_soup.find('article').attrs['class'][7].replace('category-','')
		div = page_soup.find( 'div',{'class':'entry-content'})

		content = ''
		for i in div.contents:

			if i.name in ['h2','h3']:
				content = f'{content}<{i.name}>{i.text}</{i.name}>'

			elif i.name == 'p':

				if i.text != '':
					
					if i.contents[0].name is None or i.contents[0].name == 'span':

						# when we use gpt3 api uncomment this
						# query = f'Rephrase this in own word {i.text}'
						# response = gpt3(query)
						# content = f'{content}<p>{response}</p>'

						# when we don't use gpt3 api uncomment this
						content = f'{content}<p>{i.text}</p>'
						
					# when paragraph has strong tag
					elif i.contents[0].name == 'strong':
						# query = f'Rephrase this in own word {i.text}'
						# response = gpt3(query)
						# content = f'{content}<p><strong>{response}</strong></p>'

						content = f'{content}<p><strong>{i.text}</strong></p>'


			if i.name == 'ul':
				ul = '<ul>'
				for i in i.contents:
					if i.name == 'li':
						# if len(i.text) >= 50:
						# 	query = f'Rephrase this in own word {i.text}'
						# 	response = gpt3(query)
						# 	ul = f'{ul}<li>{response}</li>'
						# else:
						ul = f'{ul}<li>{i.text}</li>'

				ul = f'{ul}</ul>'
				content=content+ul

		ls = [title,content.strip(),cat]
		with open('querysprouts.csv', 'a',newline='',encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(ls)
		return 1

	# when we get rate limit error
	except openai.error.RateLimitError as e:

		print(e,'\nsleeping')
		time.sleep(30)
		return scraping(url)

	except Exception as e:
		print(e)
		return 0


try:
	try:
		with open('querysprouts.csv','r') as f:
			reader = csv.reader(f)
			entry = len(list(reader))
	except Exception:
		entry = 0

	if entry == 0:	
		with open('querysprouts.csv', 'a',newline='',encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(['title','content','category'])

	with open('querysproutsitemap.csv','r') as f:
		reader = csv.reader(f)
		urls = list(reader)

	
	urls_list = []
	for i in range(entry,len(urls),2):
		ls = [j[0] for j in urls[i:i+2]]
		urls_list.append(ls)
	
	for j,i in enumerate( urls_list):
		thread = [Thread(target=scraping, args=(url,)) for url in i]
		
		for i in thread:
			i.start()
		for i in thread:
			i.join()
		
		print(f'{(j+1)*2} complated')
	
except KeyboardInterrupt:
	exit()

except Exception as e:
	print(e)
	
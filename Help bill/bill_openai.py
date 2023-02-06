import openai 
import random
import time
import csv
from bs4 import BeautifulSoup 
import re

KEYS = ['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','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','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',
		'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']

MAX_KEY_COUNT = len(KEYS)
KEYS_COUNT = 0

def gpt3(stext, key_count):
	global KEYS_COUNT,MAX_KEY_COUNT
	try:
		openai.api_key = KEYS[key_count]  
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
	
	except openai.error.RateLimitError as e:
		print(e,'and current key :',KEYS[key_count])	
		time.sleep(5)	
		KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
		return gpt3(stext, KEYS_COUNT)

def get_p_generated(text):
	content = ''
	global KEYS_COUNT,MAX_KEY_COUNT
	for t in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.replace('\n','')):
		if t.replace(' ','') != '':
			query = f'Rephrase this in own word{t}'
			response = gpt3(query, KEYS_COUNT)
			if response is not None:
				response =  response.replace('\n',' ')
			content = f'{content} {response}'
			KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
	return content

def get_list(ul):
	content = ''
   
	for j in ul.contents:
		if j.text!='\n' and j.text.replace(' ','').replace('\n','') != '':
			if j.name == 'li' :
				
				if len(j.text) >= 50:
					content = f'{content}<li>{get_p_generated(j.text).strip()}</li>'
				else:
					content = f'{content}<li>{j.text.strip()}</li>'
					
			elif j.name in ['ul','ol']:
				content = f'{content} <{j.name}> {get_list(j)} </{j.name}>'
			else:
				content = f'{content} {j}' 
			
	return content

def get_content(child=None):
		
	content=''
	
	for i in child.contents:
		if i.name is not None:
			if i.name in ['h2','h3']  :
				content = f'{content}<{i.name}>{i.text.strip()}</{i.name}>'           

			elif i.name == 'p' and  len(i.text) > 5: 
				content = f'{content}<p>{get_p_generated(i.text).strip()}</p>'
				
			elif i.name in ['ol','ul'] :                  
				content = f'{content} <{i.name}> {get_list(i)} </{i.name}>'

	return content

try:
	try:
		#this is checking for already saved data2
		with open('G:/Scrapping/Web Scraping/Help bill/needhelppaying_data_openai.csv','r') as f: 
			reader = csv.reader(f)
			list_titles = [i[0] for i in list(reader)[1:]]
			
	except Exception:
		list_titles = []
	
	count = len(list_titles)
	if count == 0:	
		with open('G:/Scrapping/Web Scraping/Help bill/needhelppaying_data_openai.csv', 'a',newline='\n',encoding='utf-8') as f: #this is checking for already file having saved url or not
			writer = csv.writer(f)
			writer.writerow(['title','content'])
	
	#this file is scraped data file
	with open('G:/Scrapping/Web Scraping/Help bill/needhelppaying_data_scraped1.csv','r') as f: 
		reader = csv.reader(f)
		data = list(reader)[1:]
		for i in data:
			if i[1] not in list_titles:
				soup = BeautifulSoup(i[2], 'html.parser')
				content = get_content(soup)
				
				# this file for saving generated data
				with open('G:/Scrapping/Web Scraping/Help bill/needhelppaying_data_openai.csv', 'a',newline='\n',encoding='utf-8') as f: 
					writer = csv.writer(f)
					writer.writerow([i[1],content])
				list_titles.append(i[1])
				print(f'{count} completed')
				count += 1
			# this file for incase of check which urls are already saved
			with open('G:/Scrapping/Web Scraping/Help bill/needhelppaying_saved_url.csv', 'a',newline='\n',encoding='utf-8') as f:
				writer = csv.writer(f)
				writer.writerow([i[0],i[1]])
				
except KeyboardInterrupt:
	exit()

except Exception as e:
	print(e)
import contextlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
import time



def get_data(search,driver,limit=5):
    
    driver.get('https://www.google.com')
    driver.implicitly_wait(10)

    print(f"Fetching data for {search}")


    q= driver.find_element(By.NAME, "q")
    q.send_keys(search + Keys.ENTER)
    driver.implicitly_wait(10)
    saved_count = 1
    counter = 1
    qno = 1
    data = []


    while saved_count <= limit:
        qq = aa = ""

        # checking for question
        try:
            question = driver.find_element(By.CSS_SELECTOR,f'div[jsname="N760b"] > div:nth-child({counter}) > div:nth-child(2)')
            qq = question.text
            print(qq)
        except NoSuchElementException:
            counter += 1
            continue

        time.sleep(1)

        # checking for answer
        question.click()

        answer = ""
        with contextlib.suppress(NoSuchElementException):
            answer = question.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div > div > span:nth-child(1) > span')

        #  if answer is not present
        if not answer:
            print('different format')
            aa = ""

        else:
            # just to check if answer is present
            print(qno, qq)
            aa = answer.text
            print(aa)
            print('-------------------------------------')
            
            qno += 1

            row = [qq, aa]
            data.append(row)
            saved_count += 1

        counter += 1

    driver.close()

    #  after complation of all data saving it to csv file
    path = search.strip().replace(' ','_') +'_qa.csv'
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Answer'])
        writer.writerows(data)
    
    


path ='chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability('browserless:token', '64302a88-dcc8-4635-ae83-f546beeae345')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')

searches = [
    'python',
    'java',
    'c++',
]



for search in searches:
    driver = webdriver.Chrome(path,options=chrome_options)
    get_data(search,driver)
    

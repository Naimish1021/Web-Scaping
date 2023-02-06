from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import pyrebase

config = {
  "apiKey": "AIzaSyCKMmt51qUjHVpWoz-JCBJMJpdR-LMkznE",
    "authDomain": "my-data-9edc9.firebaseapp.com",
    "databaseURL": "https://my-data-9edc9-default-rtdb.firebaseio.com",
    "projectId": "my-data-9edc9",
    "storageBucket": "my-data-9edc9.appspot.com",
    "messagingSenderId": "511134635681",
   " appId": "1:511134635681:web:b30ff0e8111a135a3742e0",
   " measurementId": "G-7ZF29YBL2R",
  "database_url": "https://my-data-9edc9.firebaseio.com",
 }


db = pyrebase.initialize_app(config)
db = db.database()
citys = db.child('cities').get()
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

places = db.child('places').get()
skip = 0
total_count = 0
if places.val() is not None:
    skip = len(places.val())
    last_city_id = list(places.val())[-1]['city_id']
    skip = len(db.child('places').order_by_child('city_id').equal_to(last_city_id).get().val())
    total_count = len(db.child('places').get().val())
start = last_city_id+1 if skip == 20 else 1
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
s = Service("G:\Scrapping\Selenium Projects\chromedriver.exe") #change path to chromedriver.exe
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--enable-webgl-developer-extensions")
chrome_options.add_argument("--enable-webgl-draft-extensions")

driver = webdriver.Chrome(service=s,options=chrome_options)

for city in citys[start:]:
    state = db.child('states').child(city.val()['state_id']).get().val()['state_name']
    print('state :' ,state)
    print('city : ',city.val()['city_name'])
    search = f" landscaping  in {city.val()['city_name']},{state}" # change search to your search

    driver.get('https://www.google.com')
    driver.implicitly_wait(2)
    driver.find_element(By.NAME,"q").send_keys(search + Keys.ENTER)
    more = driver.find_element(By.TAG_NAME,"g-more-link")
    more_btn = more.find_element(By.TAG_NAME,"a")
    more_btn.click()
    time.sleep(10)
    counter = 0

    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, 'div#search a[class="vwVdIc wzN8Ac rllt__link a-no-hover-decoration"')

        if len(elements) > skip > 0:
            elements = elements[skip+1:]
            counter = skip
            skip = 0
        for element in elements:
            data_cid = element.get_attribute('data-cid')
            element.click()
            # print('item click... 5 seconds...')
            time.sleep(2)

            #title
            title = driver.find_element(By.CSS_SELECTOR,'h2[data-attrid="title"]')

            # print('title: ', title.text)
            #address
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:address"] span:nth-child(2)')
                if len(temp_obj.text) > 0:
                    address = temp_obj.text
                    pincode = address.split(',')[-2]
            except NoSuchElementException:
                address ="NA"
                pincode = "NA"
            # print ('address: ',address)


            #website
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[class="kp-header"] div > div > div:nth-child(2) > div > a')
                website = temp_obj.get_attribute('href') if temp_obj.text == 'Website' else "NA"
            except NoSuchElementException:
                website ="NA"

            # print('website:', website)

            #phone
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/collection/knowledge_panels/has_phone:phone"] span:nth-child(2) > span > a > span')
                if len(temp_obj.text) > 0:
                    phone = temp_obj.text
            except NoSuchElementException:
                phone ="NA"

            # print('phone:', phone)

            #rating
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'g-review-stars span')
                if len(temp_obj.get_attribute('aria-label')) > 0:
                    rating = temp_obj.get_attribute('aria-label')
            except NoSuchElementException:
                rating ="NA"

            # print('rating:',rating)

            #total review
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'a[data-async-trigger="reviewDialog"] span')
                if len(temp_obj.text) > 0:
                    reviews = temp_obj.text
            except NoSuchElementException:
                reviews ="NA"
            # print('reviews:', reviews)

            #image
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:media"] > div > a > div')

                if len(temp_obj.get_attribute('style')) > 0:
                    image = temp_obj.get_attribute('style')
                    if 'background' in image:
                        image = image.replace('background-image: url("','')
                        image = image.replace('"','')
                        image = image.replace(');','')
            except NoSuchElementException:
                image ="NA"
            # print('image:', image)

            #category
            category="NA"
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/local:lu attribute list"] > div > div > span')
                if len(temp_obj.text) > 0:
                    category = temp_obj.text
            except NoSuchElementException:
                try:
                    temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/local:one line summary"] > div > span')
                    if len(temp_obj.text) > 0:
                        category = temp_obj.text
                except NoSuchElementException:
                    pass




            # social profiles
            profiles=""
            for s_count in range (1, 6):
                try:
                    temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/common/topic:social media presence"] div:nth-child(2) > div:nth-child(' + str(s_count) + ') > div > g-link > a')
                    if len(temp_obj.get_attribute('href')) > 0:
                        profiles_str = temp_obj.get_attribute('href')
                except NoSuchElementException:
                    profiles_str = "NA"
                    break
                profiles += f"{profiles_str}<br/>"
            # print('profiles: ', profiles)


            #description
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-long-text]')
                if len(temp_obj.get_attribute('data-long-text')) > 0:
                    description = temp_obj.get_attribute('data-long-text')
            except NoSuchElementException:
                '''
                try:
                    temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/local:merchant_description"] > c-wiz > div > div:nth-child(2)')
                    if len(temp_obj.get_attribute('innerHTML')) > 0:
                        description = temp_obj.get_attribute('innerHTML')
                except NoSuchElementException:
                    description ="NA"
                '''
                description="NA"


            keys = ["place_name", "address", "pincode", "website", "phone", "rating", "reviews", "image", "category", "profiles","description", "city_id"]
            val = [title.text, address, pincode, website, phone, rating, reviews, image, category, profiles, description, city.key()]
            #timing
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:hours"] > div > div > div:nth-child(2) > div > table')
                if len(temp_obj.get_attribute('innerHTML')) > 0:
                    timing = temp_obj.find_elements(By.TAG_NAME,'td')
                    if len(timing) == 14:
                        for i in range(0,len(timing),2):

                            keys.append(timing[i].get_attribute('innerHTML').lower()) 
                            val.append(timing[i+1].get_attribute('innerHTML'))
                    # timing = "<table>"+timing.replace(' class="SKNSIb"','')+"</table>"
            except NoSuchElementException:
                for i in range(7):
                    keys.append(f"timing_{i}")
                    val.append('NA')

            db.child('places').child(str(total_count)).set(dict(zip(keys, val)))
            time.sleep(3)
            counter += 1 
            total_count += 1
            print(f'{total_count} places extracted')
            if counter == 20:
                break

                    #print(counter, data_cid, title.text, address, website, phone,rating,reviews,image,category,timing,description,profiles)
                    # row = [data_cid, title.text, address, website, phone,rating,reviews,image,category,timing,description,profiles]
                    # data.append(row)

        if counter == 20:
                break
        try:
            page_button = driver.find_element(By.ID, 'pnnext')
            page_button.click()
            print('page click... 10 seconds...')
            time.sleep(10)
        except NoSuchElementException:
            break



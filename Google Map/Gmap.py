from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import mysql.connector as mysql


mydb = mysql.connect(host="localhost", user="root", passwd="", db="housing")
mycursor = mydb.cursor()

# getting last city id
mycursor.execute("SELECT max(city_id) FROM places")
max_id = mycursor.fetchone()[0]

# gettting how many places saved from current city
if max_id is not None:
    mycursor.execute("SELECT count(place_id) FROM places WHERE city_id = %s", (max_id,))
    skip = mycursor.fetchone()[0]
    mycursor.execute("SELECT max(place_id) FROM places")
    total_count = mycursor.fetchone()[0]
else:
    skip = 0
    total_count = 0
if max_id is None:
    mycursor.execute("SELECT * FROM city")
elif skip == 20:
    mycursor.execute(f"SELECT * FROM city WHERE city_id > {str(max_id)}")
else:
    mycursor.execute(f"SELECT * FROM city WHERE city_id > {str(max_id-1)}")

citys = mycursor.fetchall()
# search = "landscaping in dallas"
# pages = 2

# header = ["data_cid", "title", "address", "website", "phone", "rating","reviews","image","category","timing","description","profiles"]
# data = []

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


options =webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--enable-webgl-developer-extensions")
options.add_argument("--enable-webgl-draft-extensions")

s = Service("chromedriver.exe")
driver = webdriver.Chrome(service=s,options=options)




def get_data(counter):
    while True:
        global skip, total_count
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
            address = 'NA'
            pincode = 'NA'
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:address"] span:nth-child(2)')
                if len(temp_obj.text) > 0:
                    address = temp_obj.text
                    pincode = address.split(',')[-2]
                    
            except NoSuchElementException:
                pass
            # print ('address: ',address)


            #website
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[class="kp-header"] div > div > div:nth-child(2) > div > a')
                website = temp_obj.get_attribute('href') if temp_obj.text == 'Website' else "NA"
            except NoSuchElementException:
                website ="NA"

            # print('website:', website)

            #phone
            phone ="NA"
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/collection/knowledge_panels/has_phone:phone"] span:nth-child(2) > span > a > span')
                if len(temp_obj.text) > 0:
                    phone = temp_obj.text
            except NoSuchElementException:
               pass

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
            reviews ="NA"
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'a[data-async-trigger="reviewDialog"] span')
                if len(temp_obj.text) > 0:
                    reviews = temp_obj.text
            except NoSuchElementException:
                pass
            # print('reviews:', reviews)

            #image
            image ="NA"
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:media"] > div > a > div')

                if len(temp_obj.get_attribute('style')) > 0:
                    image = temp_obj.get_attribute('style')
                    if 'background' in image:
                        image = image.replace('background-image: url("','')
                        image = image.replace('"','')
                        image = image.replace(');','')
            except NoSuchElementException:
                pass
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
            description="NA"
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
                pass 


            row_q ="INSERT INTO `places`( `name`, `address`, `pincode`, `website`, `phone`, `rating`, `reviews`, `image`, `category`, `profiles`,`description`, `city_id`"
            val = [title.text, address, pincode, website, phone, rating, reviews, image, category, profiles, description, city[0]]
            #timing
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:hours"] > div > div > div:nth-child(2) > div > table')
                if len(temp_obj.get_attribute('innerHTML')) > 0:
                    timing = temp_obj.find_elements(By.TAG_NAME,'td')
                    if len(timing) == 14:
                        for i in range(0,len(timing),2):

                            row_q += f",`{timing[i].get_attribute('innerHTML').lower()}`"
                            val.append(timing[i+1].get_attribute('innerHTML'))

                    else:
                        for i in range(7):
                            row_q += f",`{days[i]}`"
                            val.append('NA')
                    # timing = "<table>"+timing.replace(' class="SKNSIb"','')+"</table>"
            except NoSuchElementException:
                for i in range(7):
                    row_q += f",`{days[i]}`"
                    val.append('NA')


            row_q += ")VALUES( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            try:
                mycursor.execute(row_q,tuple(val))
                mydb.commit()
            except Exception as e:
                print(e)
                mydb.rollback()

            counter += 1 
            total_count += 1
            print(f'{total_count} places extracted')
            if counter == 20:
                return None

                    #print(counter, data_cid, title.text, address, website, phone,rating,reviews,image,category,timing,description,profiles)
                    # row = [data_cid, title.text, address, website, phone,rating,reviews,image,category,timing,description,profiles]
                    # data.append(row)

        if counter == 20:
                return None
        try:
            page_button = driver.find_element(By.ID, 'pnnext')
            page_button.click()
            print('page click... 10 seconds...')
            time.sleep(10)
        except NoSuchElementException:
            break
    
    return None

for city in citys:

    mycursor.execute("SELECT state_name FROM state WHERE state_id = %s", (city[2],))
    state = mycursor.fetchone()
    print('state :' ,state[0])
    print('city : ',city[1])
    search = f" landscaping  in {city[1]},{state[0]}" # change search to your search
    counter = skip
    try :
        driver.get('https://www.google.com')
        driver.implicitly_wait(2)
        driver.find_element(By.NAME,"q").send_keys(search + Keys.ENTER)
        more = driver.find_element(By.TAG_NAME,"g-more-link")
        more_btn = more.find_element(By.TAG_NAME,"a")
        more_btn.click()
        time.sleep(10)
           
   
        get_data(counter)
    except Exception as e:
        
        time.sleep(10)
        driver.get('https://www.google.com')
        driver.implicitly_wait(2)
        driver.find_element(By.NAME,"q").send_keys(search + Keys.ENTER)
        more = driver.find_element(By.TAG_NAME,"g-more-link")
        more_btn = more.find_element(By.TAG_NAME,"a")
        more_btn.click()
        time.sleep(10)
           
        get_data(counter)


# with open('gmap.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#         writer.writerows(data)
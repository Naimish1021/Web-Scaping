import googlemaps #install with pip install googlemaps
import mysql.connector as mysql
from bs4 import BeautifulSoup
import time

mydb = mysql.connect(host="localhost", user="root", passwd="", db="housing")

mycursor = mydb.cursor()

search_type = 'abc' #restaurant, cafe, bar, hotel, lodging, museum, park, point_of_interest, zoo 
                            # change from here

# getting last city id
mycursor.execute("SELECT max(city_id) FROM places where type = %s",(search_type,))
max_id = mycursor.fetchone()[0]


if max_id is not None:
    mycursor.execute("SELECT count(place_id) FROM places WHERE city_id = %s and type = %s ", (max_id,search_type) )
    skip = mycursor.fetchone()[0]
    mycursor.execute("SELECT count(place_id) FROM places WHERE type = %s ", (search_type,) )
    total_count = mycursor.fetchone()[0]
else:
    skip = 0
    total_count = 0

if max_id is None:
    mycursor.execute("SELECT * FROM city")
elif skip >= 20:
    mycursor.execute(f"SELECT * FROM city WHERE city_id > {str(max_id)} ")
else:
    mycursor.execute(f"SELECT * FROM city WHERE city_id > {str(max_id-1)} ")

citys = mycursor.fetchall()


params = ['formatted_address','place_id','formatted_phone_number','rating','user_ratings_total','photos']
row_q ="INSERT INTO `places`( `name`, `address`, `pincode`, `gmap_id`, `phone`, `rating`, `reviews`, `photo`,`type`,  `city_id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
key="AIzaSyD5Sub1W-rrQ2UiObWU6lfdYHHHYPmp26E"

map_client = googlemaps.Client(key=key)


for city in citys:
    mycursor.execute("SELECT state_name FROM state WHERE state_id = %s", (city[2],))
    state = mycursor.fetchone()
    print('city : ',city[1])
    print('state :' ,state[0])   
    
    res = map_client.places(f"{search_type} in {city[1]} , {state[0]}", language='en')
    places = res.get("results")
    rows = []
    for i in places[skip:]:

        val = [i['name']]
        for tag in params:
            try:
                if tag == 'formatted_address':
                    val.append(i[tag])
                    val.append(i[tag].split(',')[-2])
                elif tag == 'photos':
                    
                    url =BeautifulSoup(i[tag][0]['html_attributions'][0], 'html.parser').find('a').attrs['href']
                    val.append(url)
                
                else:
                    val.append(i[tag])
            except:
                val.append("NA")

        val.extend([search_type,city[0]])
        rows.append(val)
    mycursor.execute(row_q, val)
    mydb.commit()
    time.sleep(0.1)
    total_count += 1
    print(f'{total_count} inserted')
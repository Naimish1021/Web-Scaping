import googlemaps
import mysql.connector as mysql
from bs4 import BeautifulSoup
import time

mydb = mysql.connect(host="localhost", user="root", passwd="", db="housing")

mycursor = mydb.cursor()


def get_data(search_type):
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
        mycursor.execute("SELECT city.city_id,city.city_name,state.state_name FROM city inner join state on city.state_id = state.state_id ")
    elif skip >= 20:
        mycursor.execute(f"SELECT city.city_id,city.city_name,state.state_name FROM city inner join state on city.state_id = state.state_id  WHERE city_id > {str(max_id)} ")
    else:
        mycursor.execute(f"SELECT city.city_id,city.city_name,state.state_name FROM city inner join state on city.state_id = state.state_id  WHERE city_id > {str(max_id-1)} ")

    citys = mycursor.fetchall()
    print(len(citys))
    
    params = ['formatted_address','place_id','formatted_phone_number','rating','user_ratings_total','photos']
    row_q ="INSERT INTO `places`( `name`, `address`, `pincode`, `gmap_id`, `phone`, `rating`, `reviews`, `photo`,`type`,  `city_id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    key="AIzaSyC_OybJl2aaTPrYPk0ANERfHFQotOb3a5k"

    map_client = googlemaps.Client(key=key)
    for city in citys:
        print('city : ',city[1])
        print('state :' ,city[2])
        print('search type : ',search_type)   
        # continue
        res = map_client.places(f"{search_type} in {city[1]} , {city[2]}", language='en')
        places = res.get("results")
        rows= []
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
        mycursor.executemany(row_q, rows)
        mydb.commit()
        total_count += 1
        time.sleep(3)
        print(f'{total_count+len(places)} inserted {search_type}')

with open('search_types.txt','r') as f:
    search_types = f.read().splitlines()
    for i in search_types:
        get_data(i)
        time.sleep(3)
        print(f'{i} inserted')
import requests
from bs4 import BeautifulSoup
import time
import csv

url = 'https://www.iplt20.com/auction'

req = requests.get(url)

soup = BeautifulSoup(req.content,'html.parser')


##########    Team Data     ######

data =[['Team Name','Funds Remaining','Overseas Players','Total Players']]

for i in soup.find('div',class_='auction-grid-view mt-3').find_all('div',class_="agv-main"):
    name = i.find(class_="agv-team-name").text
    remain_fund = i.find(class_='avg-fund-remaining').find(class_='fr-fund').text
    li = i.find_all('li')
    overseas_player = li[0].find(class_='fr-fund').text
    total_player = li[1].find(class_='fr-fund').text
    data.append([name,remain_fund,overseas_player,total_player])

with open('data.csv','w',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)

#########         Team And Player Data          #########

selection = soup.find(id="autab3-2022").find_all('section')
data  =[ ['Team Name','Player Name','Nationality','Type','Price Paid']]
for i in selection:
    team_name=i.find('h2').text
    tr = i.find('tbody').find_all('tr')

    for i in tr:
        td = i.find_all('td')
        p_name = td[0].text
        nationality = td[1].text
        p_type = td[2].text
        price = td[3].text
        data.append([team_name,p_name,nationality,p_type,price])

with open('team_data.csv','w',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)


#######        Most selling player by team      ########
top_buy = soup.find(id="top-buys")

data  =[ ['Team Name','Player Name','Type','Price']]

for i in top_buy.find('tbody').find_all('tr'):
   
    td = i.find_all('td')
    team_name = td[0].text.replace('\n','')
    p_name = td[1].text 
    p_type  = td[2].text
    price = td[3].text 
    data.append([team_name,p_name,p_type,price])

with open('top_sold.csv','w',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)

#####     Unsold Player Data      ######
unsold = soup.find(id="autab4-2022")
data  =[ ['Player Name','Nationality','Type','Base Price']]
for i in unsold.find('tbody').find_all('tr'):
    td = i.find_all('td')
    p_name = td[0].text.replace('\n','')
    nationality = td[1].text 
    p_type  = td[2].text
    price = td[3].text 

    data.append([p_name,nationality,p_type,price])

with open('unsold_player.csv','w',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)
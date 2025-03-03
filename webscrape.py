""" Very simple python webscraper """ 
import requests
from bs4 import BeautifulSoup
import pandas as pd


r = requests.get('https://www.mimuw.edu.pl/')

soup = BeautifulSoup(r.content, 'html.parser')

content = []

events = soup.select('div.info-item')

for event in events:
    content.append({"Tytuł": event.select_one('h3').text, "URL":event.a['href'] if event.select_one('a') and event.a.has_attr('href') else None, "Data": event.select_one('div.info-item-text-date').text})
    
df = pd.DataFrame.from_dict(content)

df.to_csv('events.csv', index = False)

random_events = df.sample(5)
print(random_events)

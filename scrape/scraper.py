import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader

headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5',
            'Referer': 'https://google.com',
            'DNT': '1'}

searchterm = 'dress'

def get_data(searchterm):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={searchterm}&_sacat=0'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
    for item in results:
        product = {
            'category': item.find('span', {'class': 'SECONDARY_INFO'}),
            'title': item.find('h3', {'class': 's-item__title'}).text,
            'price': item.find('span', {'class': 's-item__price'}),
            'image': item.find('img', {'class': 's-item__image-img'}),
            'item': item.find('a')       
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist, searchterm)

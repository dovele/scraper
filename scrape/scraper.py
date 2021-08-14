import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5',
            'Referer': 'https://google.com',
            'DNT': '1'}

def scrape_data(items_to_scrape, keywords):
  """
  Scrapes ebay website for a number of samples for each keyword
  
  :param items_to_scrape: integer of items to scrape for each keyword.
  :param keywords: list of keywords to scrape.
  :return: pandas dataframe with the following columns:
    Category (keyword), title, price, item url, image url.
    
  """

  data = {"category": [], "item_title": [], "item_price": [], "item_url": [], "item_image": []}
  for keyword in keywords:
    page_url = []
    for i in range(1,round((items_to_scrape/203) + 1)):
        page_url.append('https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + keyword + '&_sacat=0&_ipg=192&_pgn=' + str(i))
    # details of the info from the website
    for links in page_url:
      print(links)
      response = requests.get(links, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')

      
      for title in soup.find_all('h3', { 'class': 's-item__title' }):
        data["item_title"].append(title.text)
        data["category"].append(keyword)
      for price in soup.find_all('span', { 'class':"s-item__price" }):
        data["item_price"].append(price.text)
      for url_of_item in soup.find_all('a', { 'class': 's-item__link' }):
        data["item_url"].append(url_of_item.get('href'))
      for url_of_image in soup.find_all('img', { 'class': 's-item__image-img' }):
        data["item_image"].append(url_of_image['src'])
    page_url.clear()

  df = pd.DataFrame.from_dict(data, orient='index')
  return df.transpose()

# scrape_data(3000, ['dress', 'bikini', 'sunglasses'])  # Example

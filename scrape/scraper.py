import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
import random
from decimal import Decimal
import re
from database_operations import *


def scrape_keyword(number_of_items: int, keyword: str) -> pd.DataFrame:
    """
    Scrapes number_of_items products from etsy.com for a given keyword
    and returns a pandas dataframe
    :param number_of_items: Number of products to scrape (int)
    :param keyword: Keyword for which scrape products data (str)
    :return: pandas Dataframe
    """
    ua = UserAgent()

    items_count = 0
    titles_list = []
    prices_list = []
    ratings_list = []
    reviews_count_list = []
    item_urls_list = []
    images_url_list = []

    keyword_query = keyword.replace(" ", "+")

    while items_count < number_of_items:
        page_number = 1

        url = f'https://www.etsy.com/search?q={keyword_query}&page={page_number}'
        page = requests.get(url=url, headers={"User-Agent": ua.chrome})
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            for container in soup.select(".js-merch-stash-check-listing.v2-listing-card"):

                title = container.find("h3").text.strip().replace("'", "")
                titles_list.append(title)

                price = Decimal(container.find("span", class_="currency-value").text)
                prices_list.append(price)

                try:
                    rating = float(container.find("input").get('value'))
                except:
                    rating = 0
                    pass

                ratings_list.append(rating)

                try:
                    reviews_container = container.select(".text-body-smaller.text-gray-lighter")
                    reviews_count_string = reviews_container[1].text
                    reviews_count_without_parentheses = re.sub('[(,)]', '', reviews_count_string)
                    reviews_count = int(reviews_count_without_parentheses)
                except:
                    reviews_count = 0
                    pass

                reviews_count_list.append(reviews_count)

                item_url = container.find("a").get('href')
                item_urls_list.append(item_url)

                image_url = container.find("img").get('src')
                if not image_url:
                    image_url = container.find("img").get('data-src')
                images_url_list.append(image_url)

                items_count += 1

                if items_count == number_of_items:
                    break

        else:
            print('Page unreachable')
            break

        page_number += 1
        print('End of loop. Currently there are: ', str(items_count), ' items from: ', str(number_of_items))

        time.sleep(random.uniform(2, 4))

    data_dictionary = {'title': titles_list, 'price': prices_list, 'rating': ratings_list,
                       'reviews_count': reviews_count_list, 'item_url': item_urls_list,
                       'image_url': images_url_list}

    return pd.DataFrame(data_dictionary)


def scraper(keywords: 'list[str]', results_count: int):
    """
    Loops through every keyword in keywords_list and calls the scraping method,
    after dataframe is returned it calls the method to insert the data to the keywords_data table
    :param keywords: List of keywords to scrape (List[str])
    :param results_count: Number of products to scrape for each keyword (int)
    """
    for keyword in keywords:
        insert_keyword(keyword)
        df = scrape_keyword(results_count, keyword)
        keyword_id = get_last_keyword_id()
        insert_dataframe_to_keywords_data(df, keyword_id)
        time.sleep(random.uniform(3, 5))


# eBay scraper

This Ebay scraper was written for learning purposes.
Project contains two Python files: scraper.py and database.py

It scrapes this information - category, titles, prices, item urls, image urls.

## Usage
To scrape product information:
1) run "scraper.py"
3) put in the number of items ("items_to_scrape") and keywords ("keywords") you want to scrape into "scrape_data(items_to_scrape, keywords)", e.g.:


```
scrape_data(3000, ['dress', 'bikini', 'sunglasses'])
```

To insert tables into Heroku database:
1) run "database.py"
2) put in the datframe you scraped funtion into "create_insert_table(df)", e.g.:


```
create_insert_table(scrape_data(3000, ['dress', 'bikini', 'sunglasses']))
```

## License
> You can check out the full license here: https://opensource.org/licenses/MIT

This project is licensed under the terms of the MIT license.

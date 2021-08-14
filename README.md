# scraper

This Ebay scraper was written for learning purposes.
Project contains two Python files: scraper.py and database.py

It scrapes this information - category, titles, prices, item urls, image urls.

## Installation
```!pip install git+https://github.com/dovele/scraper
  from scraper import Scraper
  scraper = Scraper()
```
## Usage

To scrape, put in a keyword into 'searchterm =', for example 'search term = 'sunglasses''. The output will be a csv file. 
Successful scraping returns 'Saved to CSV'.

import config
import psycopg2 
from psycopg2 import connect

import psycopg2
import pandas as pd

def connect_database():
    """
    Connection to work with the remote database on Heroku platform.
    :return: connection
    """
    connection = psycopg2.connect(
      database="db",
      user="user",
      password="password",
      host="host",
      port="5432"
  )

    return connection


def create_insert_table(df):
    """
    Create tables and insert dataframe in database.
    :return: None
    """
    connection = connect_database()
    cur = connection.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id serial PRIMARY KEY,
            category VARCHAR(50)
        );
        ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS ebay (
        id serial PRIMARY KEY,
        item_title varchar(10000),
        item_price varchar(255),
        item_url varchar(10000),
        item_image varchar(10000),
        category varchar(255)
        );
        ''')

    #Get array of unique category names
    unique_categories = df['category'].str.split(',').explode().unique().tolist()
    cat = [i for i in range(1, len(unique_categories)+1)]
    # Insert unique category names to the categories table
    for i in cat:
        cur.execute(f"INSERT INTO categories (category) VALUES ('{i}');")

    # insert data df into ebay table
    for index, row in df.iterrows():
            cur.execute(
                "INSERT INTO ebay (item_title, item_price, item_url, item_image, category) values(%s, %s, %s, %s, %s)",
                (row.item_title, row.item_price, row.item_url, row.item_image, row.category),
            )

    connection.commit()

def join_and_export():
    """
    Execute query, fetch all the records and export it to CSV file.
    :return: CSV file.
    """
    connection = connect_database()
    cur = connection.cursor()

    cur.execute(
            "select categories.category, ebay.item_title, ebay.item_price, ebay.item_url, ebay.item_image from ebay LEFT JOIN categories on ebay.category = categories.category"
        )

    df = pd.DataFrame(cur.fetchall())
    df.to_csv('data.csv')
    
# create_insert_table(scrape_data(3000, ['dress', 'bikini', 'sunglasses'])) # Example

from create_connection import connect
import pandas as pd
from datetime import datetime
from psycopg2.extras import execute_values


def create_tables() -> None:
    """
    Connects to the database and creates tables if they don't exist
    for keywords (keywords) and its data (keywords_data)
    """

    connection = connect()
    cur = connection.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS keywords (
    id serial PRIMARY KEY,
    keyword VARCHAR ( 255 ) NOT NULL,
    query_timestamp TIMESTAMP 
    );
    CREATE TABLE IF NOT EXISTS keywords_data (
        id serial PRIMARY KEY,
        keyword_id INT,
        title VARCHAR (255),
        price DECIMAL,
        rating FLOAT,
        reviews_count INT,
        item_url TEXT,
        image_url TEXT,
        CONSTRAINT fk_keyword
            FOREIGN KEY(keyword_id) 
                REFERENCES keywords(id));''')

    print('Tables were created successfully')


def drop_tables() -> None:
    """
    Drops existing tables
    """
    connection = connect()
    cur = connection.cursor()
    cur.execute('''
    DROP TABLE IF EXISTS
        keywords,
        keywords_data;''')

    print('Tables were dropped successfully')


def export_data() -> None:
    """
    Selects and fetches all data from two tables about keywords
    and exports that data to csv file
    """
    connection = connect()
    curr = connection.cursor()
    curr.execute('''
    SELECT keyword, query_timestamp, title, price, rating, reviews_count, item_url, image_url
    FROM keywords
    INNER JOIN keywords_data ON keywords_data.keyword_id = keywords.id;''')
    rows = curr.fetchall()
    df = pd.DataFrame(rows, columns=[x[0] for x in curr.description])
    df.to_csv('data_export.csv', index=False)
    print('Data was exported successfully to data_export.csv')


def insert_keyword(keyword: str) -> None:
    """
    Inserts given keyword to the 'keywords' table
    :param keyword: keyword that will be scraped
    """
    connection = connect()
    curr = connection.cursor()
    dt = datetime.now()

    curr.execute(f"INSERT INTO keywords(keyword, query_timestamp) VALUES ('{keyword}', '{dt}');")


def insert_dataframe_to_keywords_data(df: pd.DataFrame, keyword_id: int) -> None:
    """
    Inserts given dataframe containing information about scraped data for a given keyword
    to the 'keywords_data' table
    :param df: Scraped dataframe with products data
    :param keyword_id: keyword's if for which the data was scraped
    """
    connection = connect()
    curr = connection.cursor()

    tuples = [(keyword_id, ) + tuple(x) for x in df.to_numpy()]
    cols_list = list(df.columns)
    cols_list.insert(0, 'keyword_id')
    cols = ','.join(cols_list)
    query = "INSERT INTO %s(%s) VALUES %%s" % ('keywords_data', cols)
    execute_values(curr, query, tuples)


def get_last_keyword_id() -> int:
    """
    Finds and returns the last keyword's id
    :return: last keyword's id (int)
    """
    connection = connect()
    curr = connection.cursor()
    curr.execute("SELECT MAX(id) FROM keywords;")
    return curr.fetchone()[0]

import sys
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors


DATABASE = ""
USER = ""
PASSWORD = ""
HOST = ""
PORT = ""


def show_psycopg2_exception(err):
    """
    Handles and parses psycopg2 exceptions.
    """
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occurred
    line_n = traceback.tb_lineno
    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


def connect(database: str = DATABASE, user: str = USER, password: str = PASSWORD, host: str = HOST, port: str = PORT):
    """
    The function will attempt to establish a connection with the database and return the connection if successful.
    If unsuccessful the error will be shown.
    Database information needs to be provided.
    """
    connection = None
    try:
        print("Establishing a connection with the database...")
        connection = psycopg2.connect(
            user=user,
            database=database,
            password=password,
            host=host,
            port=port
        )
        print("Connection successful!")
    except OperationalError as err:
        # passing exception to function
        show_psycopg2_exception(err)
        # set the connection to 'None' in case of error
        connection = None

    return connection


def copy_from_csv():
    """
    This function will upload the data from a csv file into a postgresql table.
    csv file and the table name need to be provided.
    If the function is unsuccessful the error will be shown.
    """
    connection = connect()
    string_execute = f"all_items.csv"
    with open("all_items.csv") as csv:
        if connection is not None:
            connection.autocommit = True
            cursor = connection.cursor()
            try:
                cursor.copy_from(csv, "all_items", sep=";")
                print("Data uploaded successfully")
                cursor.close()
                connection.close()
            except (Exception, psycopg2.DatabaseError) as err:
                show_psycopg2_exception(err)
                cursor.close()


def all_items_table():
    """
    The function will create a table for one category of items. The table has an ID, item title, price, item link,
     image link and type. The type column is used as a reference to the types table.
    """
    connection = connect()
    if connection is not None:
        connection.autocommit = True
        try:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS all_items")
            cursor.execute('''CREATE TABLE all_items (
            id SERIAL PRIMARY KEY,
            title varchar(100) DEFAULT 'brand unknown',
            price varchar(50),
            item_link text NOT NULL,
            image_link text NOT NULL,
            type varchar(100),
            CONSTRAINT item_type
                FOREIGN KEY (type)
                    REFERENCES types (type)
                    ON DELETE CASCADE
            );''')
            print(f"Table all_items created successfully")
            cursor.close()
            connection.close()

        except OperationalError as err:
            # pass exception to function
            show_psycopg2_exception(err)
            # set the connection to 'None' in case of error
            connection = None


def item_types_table(types: list):
    """
    This function when given a list of item types creates a table using those items. It has an ID column and the type.
    Is referenced in the type column of all items.
    """
    connection = connect()
    if connection is not None:
        connection.autocommit = True
        try:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS types")
            cursor.execute('''CREATE TABLE types (
            id SERIAL PRIMARY KEY,
            type varchar(100), 
            
            UNIQUE(type)
            );''')
            print("Table types created successfully")
            for i in types:
                string_execute = f'''
                INSERT INTO types (type) VALUES (\'{i}\');
                '''
                cursor.execute(string_execute)

            cursor.close()
            connection.close()

        except OperationalError as err:
            # pass exception to function
            show_psycopg2_exception(err)
            # set the connection to 'None' in case of error
            connection = None

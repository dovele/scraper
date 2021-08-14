import config
import psycopg2 
from psycopg2 import connect

connection = psycopg2.connect(
    database="d9peu2e501rl36",
    user="ixlplailywcloj",
    password="---",
    host="ec2-176-34-222-188.eu-west-1.compute.amazonaws.com",
    port="5432"
)

connection

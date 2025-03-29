import psycopg
from config.config import load_config

config_crate_baza = load_config()
baza = config_crate_baza.DBConfig.dbName
user = config_crate_baza.DBConfig.dbUser
password = config_crate_baza.DBConfig.dbPassword


connection = psycopg.connect(dbname=baza,
                                 user=user,
                                 password=password)
cursor = connection.cursor()
connection.autocommit = True
#sql = 'CREATE DATABASE MarketBot_ifw8e9238f0sd0j9eur029u3fj09we8jfsedf0s9ew0e9'
sql = 'CREATE DATABASE marketbot'
cursor.execute(sql)
connection.commit()
cursor.close()
connection.close()

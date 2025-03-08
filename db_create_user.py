from bot.config.config import load_config
import psycopg
config_crate_baza = load_config()
baza = config_crate_baza.DBConfig.dbName
user = config_crate_baza.DBConfig.dbUser
password = config_crate_baza.DBConfig.dbPassword


connection = psycopg.connect(dbname=baza,
                                 user=user,
                                 password=password)
connection.autocommit = True
cursor = connection.cursor()
sql = ("""
    CREATE TABLE users (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NULL,
        data_registration DATE NULL,
        blok_bot BOOLEAN NULL
    ); 
""")
cursor.execute(sql)
connection.commit()
cursor.close()
connection.close()

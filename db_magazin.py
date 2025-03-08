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
    CREATE TABLE magazin (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(50) NULL,
        url VARCHAR(50) NULL
    );
""")
cursor.execute(sql)
connection.commit()
cursor.close()
connection.close()

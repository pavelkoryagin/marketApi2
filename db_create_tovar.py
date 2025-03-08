import psycopg
from bot.config.config import load_config

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
    CREATE TABLE tovar (
        id BIGSERIAL PRIMARY KEY,
        fk_id_user BIGINT REFERENCES users(id) NULL,
        fk_id_magazin INTEGER REFERENCES magazin(id) NULL,
        url TEXT NULL,
        url_parsing TEXT NULL,
        artikul VARCHAR(50) NULL,
        zena INTEGER NULL,
        zena_new INTEGER NULL,
        data TIMESTAMP NULL
    )
""")
cursor.execute(sql)
connection.commit()
cursor.close()
connection.close()
#data TIMESTAMP WITH TIME ZONE NULL
import psycopg
from config.config import load_config

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
    CREATE TABLE podpiska (
        id BIGSERIAL PRIMARY KEY,
        fk_id_user BIGINT REFERENCES users(id) NULL,
        podpiska BOOLEAN NULL,
        data_podpiska TIMESTAMP NULL,
        tovarov INT NULL
    );
""")
cursor.execute(sql)
connection.commit()
cursor.close()
connection.close()

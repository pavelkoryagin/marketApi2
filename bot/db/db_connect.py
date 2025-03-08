import psycopg
import asyncio
from psycopg_pool import AsyncConnectionPool


def dbConnection(config):
    dbConnection = psycopg.Connection.connect(f"dbname={config.DBConfig.dbName} user={config.DBConfig.dbUser} password={config.DBConfig.dbPassword}", autocommit=True)
    #dbConnection = psycopg.connect(f"dbname={config.DBConfig.dbName} user={config.DBConfig.dbUser} password={config.DBConfig.dbPassword}")

    return dbConnection

async def adbConnection(config, logger):
    try:
        pool = AsyncConnectionPool(
            f"dbname={config.DBConfig.dbName} user={config.DBConfig.dbUser} password={config.DBConfig.dbPassword}"f"dbname={config.DBConfig.dbName} user={config.DBConfig.dbUser} password={config.DBConfig.dbPassword}",
            min_size=12, max_size=120, open=True)
        #В будущих версиях значение open будет заменено на false в конструкторк
        #https://www.psycopg.org/psycopg3/docs/api/pool.html#psycopg_pool.AsyncConnectionPool
        #await pool.wait()
        #await pool.open()
    except Exception as ex:
        logger.exception('Ошибка создания пула соединения. Error - adbConnection')
        #await pool.close()
    # await pool.open()
    # adbConnection = await psycopg.AsyncConnection.connect(f"dbname={config.DBConfig.dbName} user={config.DBConfig.dbUser} password={config.DBConfig.dbPassword}", autocommit=True)
    #
    # return adbConnection
    return pool
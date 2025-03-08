from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    adminId: list[int]

@dataclass
class Proxies:
    login: str
    password: str
    proxies: list[str]

@dataclass
class DBConfig:
    dbName: str
    dbUser: str
    dbPassword: str

@dataclass
class Config:
    tg_bot: TgBot
    proxies: Proxies
    DBConfig: DBConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN'), adminId=list(map(int, env.list('ADMIN_IDS')))),
        proxies=Proxies(login=env('PROXIESLOGIN'), password=env('PROXIESPAROL'), proxies=list(map(str, env.list('PROXIES')))),
        DBConfig=DBConfig(dbName=env('DBNAME'), dbUser=env('DBUSER'), dbPassword=env('DBPASSWORD'))
    )

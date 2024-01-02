from dataclasses import dataclass, field

from dotenv import load_dotenv
from os import getenv


load_dotenv()


@dataclass
class BotConfig:
    token: str = field(default=getenv('token'))
    

@dataclass
class DatabaseConfig:
    dbname: str = field(default=getenv('DBNAME'))
    user: str = field(default=getenv('USERDB'))
    password: str = field(default=getenv('PASSWORDDB'))
    
    @property
    def full_url(self):
        return f'postgresql+psycopg2://{self.user}:{self.password}@localhost/{self.dbname}'
    

Database = DatabaseConfig()
Bot = BotConfig()

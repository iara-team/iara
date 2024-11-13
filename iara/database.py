from sqlalchemy.engine import URL
from sqlmodel import SQLModel, create_engine

from .models import *

DATABASE_NAME = "iara"

# Infrastructure
DBMS_NAME = "postgresql"
DBMS_DRIVER = "psycopg2"

# Credentials
HOST = "localhost"
USERNAME = "username"
PASSWORD = "password"

url_kwargs = {
    "drivername": f"{DBMS_NAME}+{DBMS_DRIVER}",
    "username": USERNAME,
    "password": PASSWORD,
    "host": HOST,
    "database": DATABASE_NAME,
}

engine_kwargs = {
    "echo": True,
    "executemany_mode": "values_plus_batch",
    "insertmanyvalues_page_size": 10000,
    "executemany_batch_page_size": 2000,
}

# Writable Database
DATABASE_URL = URL.create(**url_kwargs)
engine = create_engine(DATABASE_URL, **engine_kwargs)

def init_db():
    SQLModel.metadata.create_all(engine)

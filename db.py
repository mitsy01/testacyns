import os

from sqlalchemy import String, Integer, MetaData, Table, Column, create_engine
from databases import Database
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_engine(SQLALCHEMY_URI, echo=True)
database = Database(SQLALCHEMY_URI)
metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer,primary_key=True),
    Column("name", String(50))
)


def create_db():
    metadata.create_all(bind=engine)
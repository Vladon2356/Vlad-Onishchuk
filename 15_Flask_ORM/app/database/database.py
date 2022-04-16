from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config as config
db_string = config.SQLALCHEMY_DATABASE_URL

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()

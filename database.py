from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## Dev engine - local SQLite DB
engine = create_engine('sqlite:///mp4.db')

## Prod Engine - MySQL - EC2 Instance
# Define your production engine here. 

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

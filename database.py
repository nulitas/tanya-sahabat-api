import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

database_url = f"mysql+pymysql://{username}:{password}@{url}:{port}/{db_name}"
if password is None or password == "":
    database_url = f"mysql+pymysql://{username}@{url}/{db_name}"

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

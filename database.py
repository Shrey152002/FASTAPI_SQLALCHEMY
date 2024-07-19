from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:shre_1588%40@localhost:3306/movieticketwebsite"


try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    logging.error(f"Error connecting to database: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
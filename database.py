from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_url = "mysql+pymysql://root:root@localhost/school_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def getDB():
    db=session()
    try:
        yield db

    finally:
        db.close()
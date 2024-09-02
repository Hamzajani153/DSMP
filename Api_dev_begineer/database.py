from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@localhost/<database>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Pk135430@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

#dependency
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


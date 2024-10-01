from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@localhost/<database>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Pk135430@localhost:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

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

while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",
                                password="Pk135430",cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as e:
        print("Database connection error")
        print(f"Error: {e}")
        time.sleep(5)
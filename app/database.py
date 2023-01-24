from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import maskpass

pwd = maskpass.askpass(prompt="Password:", mask="*")

#SQLALCHEMY_DATABASE_URL = 'postgresql://<postgress>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = (f"postgresql://postgres:{pwd}@localhost/fastapi")


engine = create_engine(SQLALCHEMY_DATABASE_URL) # establishes connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
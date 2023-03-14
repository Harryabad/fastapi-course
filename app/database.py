from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import maskpass

# Ask for user input to get the password securely
pwd = maskpass.askpass(prompt="Password:", mask="*")

# SQLALCHEMY_DATABASE_URL is the connection string to connect to the database.
# Replace <postgress> with your username and <password> with the password to access the database.
# Replace <ip-address/hostname> with the IP address or hostname of the machine hosting the database.
# Replace <database_name> with the name of the database you want to connect to.
SQLALCHEMY_DATABASE_URL = (f"postgresql://postgres:{pwd}@localhost/fastapi")

# Create an engine that connects to the database using the connection string.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker that will be used to create new database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models.
Base = declarative_base()

# This function returns a new database session every time it is called.
# The session is closed automatically when the function call is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

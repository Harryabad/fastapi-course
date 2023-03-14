# import the CryptContext class from passlib module
from passlib.context import CryptContext

# create an instance of CryptContext with the "bcrypt" scheme and the "auto" mode for handling deprecated schemes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# define a function that takes a password string and returns the hashed version using bcrypt
def hash(password: str):
    return pwd_context.hash(password)

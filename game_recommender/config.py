import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") # make using secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem" # store session data in server filesystem
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587 # or 465 for SSL
    MAIL_USE_TLS = True  # or False if using SSL
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
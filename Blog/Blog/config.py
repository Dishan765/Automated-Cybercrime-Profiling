import os

username = "root"
password = "12345"
database = "BlogDissert"
server = "localhost"


class Config:
    #SEND_FILE_MAX_AGE_DEFAULT = 0#to remove
    SECRET_KEY = 'l\x16\xc6\xd7\xc1\xd3\x17\xc9\xc0\xd1W\xa9kH\x01\xf0'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' 
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{server}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_POOL_RECYCLE=90

    SECURITY_PASSWORD_SALT = 'my_precious_two'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    #SET PASSWORD AND USERNAME AS AN ENVIRONMENT VARIABLE
    #export APP_MAIL_USERNAME="tom310359@gmail.com"
    #export APP_MAIL_PASSWORD="12345qwerty!"
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'tom310359@gmail.com'

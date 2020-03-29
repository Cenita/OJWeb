import  os
DEBUG = True
SECRET_KEY = b'\x02\xffb\x13\xc1\x9f8\x1a\xa5j\xdbu\x19\x88\xa0\xd0\xb8\xc4\x02\xed^\x93\xc4I'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'ojwebsite'
USERNAME = 'root'
PASSWORD = 'root'
DB_URL = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
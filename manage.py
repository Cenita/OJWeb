from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from app import app
from models import *

#创建一个管理者
manager = Manager(app)
#创建一个迁移程序
migrate = Migrate(app=app,db=db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
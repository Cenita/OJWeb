from app import *


#登录限制
def login_limit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('userid'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper

#已经登录
def loggined(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('userid'):
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
    return wrapper

#管理员登录限制
def admin_limit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('userid')=='admin':
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
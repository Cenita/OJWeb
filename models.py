from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    truename = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    createTime = db.Column(db.Integer,nullable=False)
    userType = db.relationship('UserType',backref=db.backref('users'))
    def getRecord(self):
        re = 0
        for i in self.acRecord:
            re+=i.score
        return re

class UserType(db.Model):
    __tablename__ = 'usertype'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    name = db.Column(db.String(5),nullable=True)

class Answer_Record(db.Model):
    __tablename__ = 'ac_record'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'))
    paper_id = db.Column(db.Integer,db.ForeignKey('paper.id',ondelete = 'CASCADE'))
    question_id = db.Column(db.Integer,db.ForeignKey('question.id',ondelete = 'CASCADE'))
    code = db.Column(db.Text)
    score = db.Column(db.Integer)
    act = db.Column(db.Integer)
    backinfo = db.Column(db.Text)
    status = db.Column(db.String(1),nullable=False)
    createTime = db.Column(db.Integer,nullable=False)

class paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    start_time = db.Column(db.Integer,nullable=False)
    end_time = db.Column(db.Integer,nullable=False)
    attr = db.Column(db.Text)
    paper_type = db.Column(db.String(2),nullable=False)
    question = db.Column(db.Text)
    status = db.Column(db.String(1),nullable=False)
    create_time = db.Column(db.Integer,nullable=False)

class question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PID = db.Column(db.String(30),unique=True)
    name = db.Column(db.String(50))
    content = db.Column(db.Text)
    input = db.Column(db.Text)
    output = db.Column(db.Text)
    example = db.Column(db.Text)
    tips = db.Column(db.Text)

class LuoGuAccount(db.Model):
    __tablename__='luogu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    token = db.Column(db.Text)
    cookies = db.Column(db.Text)
    update_time = db.Column(db.Integer,nullable=False)

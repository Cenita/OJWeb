from limit import *
import tools
import crawler
import demjson
import json
@app.route('/')
def index():
    type = request.args.get('type')
    content = {
        'webType':'index',
        'type':type,
        'list_content':[[0,'涛涛',500],[1,'敏敏',500]]
    }
    if type=='mouth':
        start,end = getTime.get_current_mouth()
    elif type=='all':
        start,end = getTime.get_current_mouth()
        start=0
    else:#星期
        start,end = getTime.get_current_week()
        content['type'] = 'week'
    #分组查询score，然后降序排列
    child = db.session.query(Answer_Record.user_id,func.sum(Answer_Record.act).label('score')).group_by(Answer_Record.user_id).subquery()
    score_list = db.session.query(User,child.c.score).outerjoin(child,User.id==child.c.user_id).all()
    print(score_list)
    #重新整理数据结构
    result_score_list = []
    index = 1
    #存在分数的用户
    for i in score_list:
        user,user_score = i
        user_type = user.userType[0].name
        user_name = user.truename
        if user_score and user_type[0]=='1':
            user_list = {
                "paiwei":"第 "+str(index)+" 名",
                "name":user_name,
                "score":user_score
            }
            result_score_list.append(user_list)
            index+=1
    #不存在分数的用户
    for i in score_list:
        user, user_score = i
        user_type = user.userType[0].name
        user_name = user.truename
        if not user_score and user_type[0]=='1':
            user_list = {
                "paiwei":"",
                "name":user_name,
                "score":0
            }
            result_score_list.append(user_list)
            index+=1
        # print(user.getRecord())
    print(result_score_list)
    content['list_content']=result_score_list
    return render_template('index.html',**content)


@app.route('/login/',methods=['GET','POST'])
@loggined
def login():
    if request.method=='GET':
        content = {
            'webType':'login'
        }
        return render_template('login.html',**content)
    else:
        #获取用户名和密码 并且找到是否存在该用户
        #若存在则登录
        #若不存在则返回
        return_json = {
            "status":200,
            "message":""
        }
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username==username).first()
        if not user:
            user = User.query.filter(User.email==username).first()
        if not user:
            user = User.query.filter(User.truename==username).first()

        if user:
            #密码是否存在
            if user.password==password:
                session['id']=user.id
                session['userid']=user.username
                session['username']=user.truename
                session.permanent = True
                return_json["message"] = url_for('index')
                return_json["status"]=400
                if user.username == 'admin':
                    return_json["message"]=url_for('back_index')
            else:
                return_json["message"] = "密码错误"
                pass
        else:
            return_json["message"] = "账号不存在"
            pass
        return json.dumps(return_json)


@app.route('/regist/',methods=['POST','GET'])
@loggined
def regist():
    content = {
        'webType': 'regist'
    }
    if request.method=='GET':
        return render_template('regist.html',**content)
    else:
        username = request.form.get('username')
        truename = request.form.get('truename')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('password_again')
        registPort = request.form.get('registPort')
        print(request.form)
        #如果两个密码不相等
        return_json = {
            "status": 200,
            "message": ""
        }
        if password2!=password1:
            return_json["message"]="两次密码不相等"
            return return_json
        user = User.query.filter(User.username==username).first()
        user2 = User.query.filter(User.email==email).first()
        user3 = User.query.filter(User.truename==truename).first()
        #查看这个用户是否存在
        if user:
            return_json["message"]="用户名已经存在"
            return json.dumps(return_json)
        if user2:
            return_json["message"] = "邮箱已存在"
            return json.dumps(return_json)
        if user3:
            return_json["message"] = "真实姓名已存在"
            return json.dumps(return_json)

        if registPort!="aaaa":
            return_json["message"] = "注册码错误"
            return json.dumps(return_json)

        try:
            user = User(username=username,truename=truename,email=email,password=password1,createTime=time.time())
            db.session.add(user)
            db.session.commit()
            usetype = UserType(user_id=user.id,name='1')
            db.session.add(usetype)
            db.session.commit()
            return_json['status']=400
            return_json["message"]=url_for('login')
        except Exception:
            return_json['status']=300
            return_json["message"]="服务器查询数据库错误"
        return json.dumps(return_json)

@app.route('/exit/',methods=['GET'])
def exit():
    session.clear()
    return redirect(url_for('login'))


@app.route('/exam/')
@login_limit
def exam():
    content = {
        'webType':'exam'
    }
    return render_template('exam.html',**content)

@app.route('/practice/')
@login_limit
def practice():
    content = {
        'webType':'practice'
    }
    this_time = int(time.time())
    can_do_paper = paper.query.filter(paper.paper_type=='1',paper.start_time<=this_time,paper.end_time>=this_time).all()
    time_out_paper = paper.query.filter(paper.paper_type=='1',paper.end_time<=this_time).all()
    ready_paper = paper.query.filter(paper.paper_type=='1',paper.start_time>=this_time).all()
    print(can_do_paper,time_out_paper,ready_paper)
    content['can_do_paper']=tools.deal_paper(can_do_paper)
    content['time_out_paper']=tools.deal_paper(time_out_paper)
    content['ready_paper']=tools.deal_paper(ready_paper)
    return render_template('practice.html',**content)

@app.route('/paper/<id>')
@login_limit
def check_paper(id):
    paper_this = paper.query.filter(paper.id==int(id)).all()
    paper_this = tools.deal_paper(paper_this)[0]
    qs_list = paper_this["question"].split(';')
    re_qs = []
    for index,qs in enumerate(qs_list):
        que = question.query.filter(question.PID==qs).first()
        re = {
            "index":index+1,
            "question":que,
            "score":Answer_Record.query.filter(Answer_Record.user_id==session['id'],Answer_Record.paper_id==id,Answer_Record.question_id==que.id).first(),
        }
        re_qs.append(re)
    re_qs = {
        'qs_num':len(qs_list),
        'qs':re_qs
    }
    paper_record = db.session.query(Answer_Record.act.label("act"),Answer_Record.user_id.label('user_id')).filter(Answer_Record.paper_id==id).subquery()
    user_record = db.session.query(User.id.label('id'),paper_record.c.act).outerjoin(paper_record,User.id==paper_record.c.user_id).subquery()
    record = db.session.query(user_record.c.id,func.sum(user_record.c.act)).group_by(user_record.c.id).all()
    users_record_list=[]
    for user_id,all_sum in record:
        if not all_sum:
            all_sum=0
        user = User.query.filter(User.id==user_id).first()
        if user.userType[0].name!='1':
            continue
        user_question_list = []
        for index,que_id in enumerate(qs_list):
            que_id = question.query.filter(question.PID==que_id).first().id
            rec = Answer_Record.query.filter(Answer_Record.user_id==user.id,Answer_Record.paper_id==id,Answer_Record.question_id==que_id).first()
            if rec:
                rec = rec.score
            else:
                rec = 0
            user_question_list.append([index+1,rec])
        users_record_list.append({
            "user":user.truename,
            "all_sum":all_sum,
            "question":user_question_list
        })
    return render_template("paper.html",paper=paper_this,questions=re_qs,user_record=users_record_list)

@app.route('/paper/<id>/<qs_id>',methods=['POST','GET'])
@login_limit
def check_quesiton(id,qs_id):
    if request.method=='GET':
        paper_this = paper.query.filter(paper.id == int(id)).all()
        paper_this = tools.deal_paper(paper_this)[0]
        qs = question.query.filter(question.id==qs_id).first()
        example = json.loads(qs.example)
        content = Answer_Record.query.filter(Answer_Record.user_id==session['id'],Answer_Record.paper_id==id,Answer_Record.question_id==qs_id).first()
        if content:
            content = content.code
        else:
            content = ""
        return render_template('question.html',paper=paper_this,question=qs,example=example,content=content)
    else:
        content = request.form.get('code')
        PID = question.query.filter(question.id == qs_id).first().PID
        ac = Answer_Record.query.filter(Answer_Record.user_id==session['id'],Answer_Record.paper_id==id,Answer_Record.question_id==qs_id).first()
        if ac:
            pass
        else:
            ac = Answer_Record(user_id=session['id'],paper_id=id,question_id=qs_id,score=0,act=0,status="0",createTime=int(time.time()),code=content)
            db.session.add(ac)
            db.session.commit()
        re_json = {
            "status":200,
            "content":""
        }
        status,re_content = crawler.luogo_oj_subject('1317349213@qq.com',PID,content,ac.id)
        if not status:
            re_json["content"]=re_content
        else:
            re_json["status"]=400
            re_json["content"]=url_for('record',id=ac.id)
        return json.dumps(re_json)

@app.route('/record/<id>',methods=['POST','GET'])
@login_limit
def record(id):
    rec = Answer_Record.query.filter(Answer_Record.id==id).first()
    pa = paper.query.filter(paper.id==rec.paper_id).first()
    que = question.query.filter(question.id==rec.question_id).first()
    rec_result = json.loads(rec.backinfo)
    print(rec_result)
    return render_template('record.html',paper=pa,record=rec,question=que,rec_result=rec_result)
from app import *
from limit import *
import crawler
import tools
import time
@app.route("/backstage/")
@admin_limit
def back_index():
    return render_template('backstage/index.html')

@app.route("/backstage/user/")
@admin_limit
def back_user():
    content = {
    }
    user = User.query.filter().all()
    user_list = []
    for i in user:
        user_type = i.userType[0].name
        createTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i.createTime))
        if user_type=='1':
            user_type='普通用户'
        elif user_type=='2':
            user_type='管理员'
        t_list = [i.username,i.truename,i.email,createTime,user_type]
        user_list.append(t_list)
    content['user_list']=user_list
    return render_template('backstage/userManage.html',**content)

@app.route("/backstage/delectUser/<id>")
@admin_limit
def back_delectUser(id):
    user = User.query.filter(User.username==id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('back_user'))

@app.route("/backstage/exam/")
@admin_limit
def back_exam():
    check_paper = paper.query.filter(paper.paper_type == '2').all()
    content = {}
    paper_list = []
    for i in check_paper:
        p = {}
        p['title'] = i.name
        p['start_time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(i.start_time))
        p['end_time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(i.end_time))
        p['quesition_num'] = len(i.question.split(';'))
        p['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.create_time))
        p['paper_id'] = i.id
        paper_list.append(p)
    content['paper_list'] = paper_list
    return render_template('backstage/paper_exam.html',**content)

@app.route("/backstage/practice/")
@admin_limit
def back_practice():
    check_paper = paper.query.filter(paper.paper_type == '1').all()
    content={}
    paper_list=[]
    for i in check_paper:
        p={}
        p['title']=i.name
        p['start_time']=time.strftime("%Y-%m-%d %H:%M",time.localtime(i.start_time))
        p['end_time']=time.strftime("%Y-%m-%d %H:%M",time.localtime(i.end_time))
        p['quesition_num']=len(i.question.split(';'))
        p['create_time']=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i.create_time))
        p['paper_id']=i.id
        paper_list.append(p)
    content['paper_list']=paper_list
    return render_template('backstage/paper_practice.html',**content)

@app.route("/backstage/edit/paper/<id>",methods=["POST","GET"])
@admin_limit
def back_edit_paper(id):
    if request.method=="GET":
        check_paper = paper.query.filter(paper.id==id).first()
        setpaper={
            "type":'practice',
            "title":check_paper.name,
            "id":check_paper.id,
            "attr":check_paper.attr,
            "paper_type":check_paper.paper_type,
            "question":check_paper.question,
            "start_time":time.strftime("%Y-%m-%d %H:%M",time.localtime(check_paper.start_time)),
            "end_time":time.strftime("%Y-%m-%d %H:%M",time.localtime(check_paper.end_time))
        }
        return render_template('backstage/add_paper.html',**setpaper)
    else:
        method = request.form.get('btn')
        args = request.form
        check_paper = paper.query.filter(paper.id == id).first()
        if method=='del':
            db.session.delete(check_paper)
            db.session.commit()
        else:
            print(request.form)
            check_paper.name=request.form.get('title')
            check_paper.attr=request.form.get('type')
            check_paper.paper_type=request.form.get('paper_type')
            check_paper.start_time=int(time.mktime(time.strptime(request.form.get('startTime'), '%Y-%m-%d %H:%M')))
            check_paper.end_time=int(time.mktime(time.strptime(request.form.get('endTime'), '%Y-%m-%d %H:%M')))
            question_string = tools.del_question(request.form.get('qu_list'))
            check_paper.question=question_string
            check_paper.status=request.form.get('status')
            db.session.commit()
        if request.form.get('paper_type')=='1':
            return redirect(url_for('back_practice'))
        else:
            return redirect(url_for('back_exam'))

@app.route("/backstage/add_paper/<type>",methods=['GET','POST'])
@admin_limit
def back_add_paper(type):
    if request.method=='GET':
        if type=='practice':
            paper_type='1'
        else:
            paper_type='2'
        return render_template('backstage/add_paper.html',type=type,paper_type=paper_type)
    else:
        start_time = request.form.get('startTime')
        end_time = request.form.get('endTime')
        start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M')))
        end_time = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M')))
        question_string = tools.del_question(request.form.get('qu_list'))
        content = {
            "name":request.form.get('title'),
            "start_time":start_time,
            "end_time":end_time,
            "paper_type":request.form.get('paper_type'),
            "attr":request.form.get('endTime'),
            "question":question_string,
            "status":request.form.get('status'),
            "create_time":int(time.time())
        }
        new_paper = paper(**content)
        db.session.add(new_paper)
        db.session.commit()
        if type=='practice':
            return redirect(url_for("back_practice"))
        else:
            return redirect(url_for("back_exam"))

@app.route("/backstage/question/")
@admin_limit
def back_question():
    questions = question.query.filter().all()
    return render_template('backstage/question.html',que=questions)
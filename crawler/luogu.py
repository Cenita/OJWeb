from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from requests.cookies import RequestsCookieJar
import json
from fake_useragent import UserAgent
from aip import AipOcr
import sys
sys.path.extend("../")
from app import *

def verify(image):
    APP_ID = '16948185'
    API_KEY = 'PDvBYGLhi2Og3aZnQihW6zqb'
    SECRET_KEY = 'McMmDdFg4HbaiW7Xql7xjsigXjn4HU6p'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = image
    option={}
    option['language_type']="ENG"
    content = client.basicGeneral(image)
    content = content.get('words_result',option)
    print(content)
    if content:
        return content[0]['words']
    else:
        return ""

def handle_content(content):
    content=content.replace('$','').replace('\\times','×').replace('\\le','<=')
    return content

def get_content(PID):
    try:
        html = urlopen('https://www.luogu.org/problem/'+str(PID)).read().decode('utf8')
        soup = BeautifulSoup(html, features='lxml')
        title = soup.h1.get_text()
        div_list = soup.article.find_all('div')
        content = handle_content(div_list[0].get_text())
        input = handle_content(div_list[1].get_text())
        output = handle_content(div_list[2].get_text())
        tips = handle_content(div_list[3].get_text())
        example = soup.article.find_all('pre')
        exam_list = []
        for i in range(int(len(example) / 2)):
            exam = {
                "input": example[i].code.get_text(),
                "out": example[i + 1].code.get_text(),
            }
            exam_list.append(exam)
        result = {
            "status":"OK",
            "title":title,
            "content":content,
            "input":input,
            "output":output,
            "example":exam_list,
            "tips":tips
        }
    except Exception:
        result = {
            "status":"ERROR"
        }
    return result

def Luogu_login(user,ss):
    password = user.password
    username = user.username
    if password:
        ua = UserAgent()
        head = {
            "User-Agent": ua.random,
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        respose = ss.get('https://www.luogu.org/api/verify/captcha', headers=head)
        login = ss.get("https://www.luogu.org/auth/login", headers=head)
        soup = BeautifulSoup(login.text, features='lxml')
        token = soup.find_all('meta', {'name': 'csrf-token'})[0]['content']
        img = respose.content
        head1 = head.copy()
        head1['referer'] = 'https://www.luogu.org/auth/login'
        head1['x-csrf-token'] = token
        head1['content-type'] = 'application/json;'
        while True:
            yzm = verify(img)
            print(yzm)
            if len(yzm) == 4:
                data = {"username": username, "password": password, "captcha": yzm}
                result = ss.post("https://www.luogu.org/api/auth/userPassLogin", json=data, headers=head1)
                result = json.loads(result.text)
                print(result)
                if result.get('locked') == False:
                    print("break")
                    break
                else:
                    respose = ss.get('https://www.luogu.org/api/verify/captcha', headers=head)
                    img = respose.content
            else:
                respose = ss.get('https://www.luogu.org/api/verify/captcha', headers=head)
                img = respose.content
    cookies = ss.cookies.get_dict()
    user.cookies = json.dumps(cookies)
    user.token = token
    user.update_time = int(time.time())
    db.session.commit()
    return cookies,token

def check_login(user,ss):
    ua = UserAgent()
    head = {
        "User-Agent": ua.random,
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    respose = ss.get("https://www.luogu.org/record/list?pid=P1150",headers = head)
    soup = BeautifulSoup(respose.text, features='lxml')
    if soup.title.get_text()=='登录 - 洛谷':
        Luogu_login(user,ss)
        return soup.find_all('meta', {'name': 'csrf-token'})[0]['content']
    else:
        return soup.find_all('meta', {'name': 'csrf-token'})[0]['content']

def luogo_oj_subject(username,PID,code,record_id):
    ss = requests.session()
    user = LuoGuAccount.query.filter(LuoGuAccount.username==username).first()
    if user.cookies:
        for name,value in json.loads(user.cookies).items():
            ss.cookies.set(name,value)
    token = check_login(user,ss)
    try:
        pass
    except Exception:
        return False,"爬虫检查登陆失败"
    ua = UserAgent()
    head = {
        "User-Agent": ua.random,
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "x-csrf-token":token,
        'referer':'https://www.luogu.org/auth/login'
    }
    data = {
        "verify": "",
        "enableO2": 0,
        "lang": 0,
        "code": code,
    }
    head['content-type']='application/x-www-form-urlencoded;'
    print(ss.post("https://www.luogu.org/api/problem/submit/P1001",data=data,headers=head).text)
    rid = json.loads(ss.post("https://www.luogu.org/api/problem/submit/P1001",data=data,headers=head).text).get('data')
    try:
        rid = rid.get('rid')
    except Exception:
        print(rid)
        return False,rid

    try:
        while True:
            time.sleep(0.5)
            result = json.loads(ss.post("https://www.luogu.org/record/{}?_contentOnly=1".format(rid),headers=head).text)
            result = result.get('currentData').get('record').get('detail')
            if result.get('compile'):
                if result.get('compile').get('success')==True:
                    if result.get('subtasks'):
                        break
                else:
                    break
        record = Answer_Record.query.filter(Answer_Record.id==record_id).first()
        if result.get('subtasks'):
            score = result.get('subtasks')[0].get('score')
            record.score = score
            record.act = score
        record.backinfo=json.dumps(result)
        record.status="1"
        db.session.commit()
    except Exception:
        return False,"爬虫提交答案失败"
    return True,"成功提交"





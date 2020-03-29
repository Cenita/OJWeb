import json
import sys
sys.path.extend('../')
import crawler
from app import *

def del_question(PID_STRING):
    pid_list = PID_STRING.split(';')
    current_item = []
    for pid in pid_list:
        q = question.query.filter(question.PID == pid).first()
        print(q)
        if q:
            current_item.append(pid)
            continue
        get_result = crawler.get_content(pid)
        if get_result['status']=='ERROR':
            continue
        current_item.append(pid)
        example = json.dumps(get_result['example'])
        q = question(PID=pid,name=get_result['title'],content=get_result['content'],
                     tips=get_result['tips'],input=get_result['input'],output=get_result['output'],
                     example=example
                     )
        db.session.add(q)
    return ";".join(current_item)


def deal_paper(text):
    paper_list=[]
    for i in text:
        pa = {
            "title": i.name,
            "id": i.id,
            "question":i.question,
            "question_num":len(i.question.split(';')),
            "start_time": time.strftime("%Y-%m-%d %H:%M", time.localtime(i.start_time)),
            "end_time": time.strftime("%Y-%m-%d %H:%M", time.localtime(i.end_time))
        }
        paper_list.append(pa)
    return paper_list
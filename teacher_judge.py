import requests
from bs4 import BeautifulSoup
from collections import defaultdict



def judge_item(teacher):
    print('judging teacher %s...' % teacher.string)
    course_id = list(teacher.parents)[2]['rwh_id']
    teacher_info = teacher['onclick'].split("'")   
    teacher_id = teacher_info[1]
    pjcs = teacher_info[3]
    form_data = {
        'rwh': course_id,
        'zgh': teacher_id,
        'pjcs': pjcs,
        'kcdm': '',
        'pageXnxq': ''
    }
    r = session.post("http://10.200.21.61:7001/ieas2.1/xspj/toAddPjjs", 
                     data=form_data)
    if r.status_code != 200:
        print('failed! Details:', r.status_code, teacher_id, course_id, pjcs)
        return
    s = BeautifulSoup(r.content, "html.parser")
    form = s.find('form', id='queryform')
    entries = form.find_all('input', type='hidden')
    form_data2 = defaultdict(list)
    for entry in entries:
        if not entry.has_attr('name'):
            continue
        form_data2[entry['name']].append(entry['value'])
    entries = form.find_all('input', id='zbdm')
    for i, entry in enumerate(entries):
        # option = entry.td.input
        option = entry.find_next_sibling('td').input
        if i == 0:
            option = option.find_next_sibling('input')
        form_data2[option['name']].append(option['value'])
    r2 = session.post('http://10.200.21.61:7001/ieas2.1/xspj/saveXspj',
                      data=form_data2)
    if r2.status_code != 200:
        print('failed! De2tails:', r2.status_code, form_data2)
        return
    print('success!')


def auto_judge():
        
    session = requests.Session()
    session.headers = {
        'Cookie': 'JSESSIONID=2f88b1mLwrV8Yx9SyDh1yLJQzQJzR1HF9qPCKPql63LMTXfgpnl5!-822511665'
    }
    res = session.get("http://10.200.21.61:7001/ieas2.1/xspj/Fxpj_fy", 
                       allow_redirects=False)
    if res.status_code != 200:
        print("can't load page")
        exit()
    
    soup = BeautifulSoup(res.content, 'html.parser')
    yellow_spans = soup.find_all('span', class_='yellow')
    teachers = []
    for span in yellow_spans:
        teachers += span.find_all('a')
    
    for teacher in teachers:
        # print(teacher.prettify())
        judge_item(teacher)

auto_judge()

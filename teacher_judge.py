import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import quote


session = requests.Session()
page_xnxq = ''

jiaowu_url = 'http://jwxt.buaa.edu.cn:8080/ieas2.1/'
# use '/login' instead of '/login/' to avoid redirects
login_url = 'https://sso.buaa.edu.cn/login?service=' \
            + quote(jiaowu_url, 'utf-8') + 'welcome'


def get_login_token() -> str:
    r = session.get(login_url)
    assert (r.status_code == 200)
    soup = BeautifulSoup(r.content, 'html.parser')
    lt = soup.find('input', {'name': 'execution'})['value']
    return lt


def login(username: str, password: str) -> bool:
    formdata = {
        'username': username,
        'password': password,
        'execution': get_login_token(),
        'type': 'username_password',
        '_eventId': 'submit',
        'submit': '登陆'
    }
    r2 = session.post(login_url, data=formdata, allow_redirects=True)
    soup = BeautifulSoup(r2.text, "html.parser")
    return not soup.find_all('div', class_='error_txt')


def assess_item(teacher: "beautifulSoup object"):
    print('evaluate teacher %s...' % teacher.string)
    course_id = list(teacher.parents)[2]['rwh_id']
    teacher_info = teacher['onclick'].split("'")
    teacher_id = teacher_info[1]
    pjcs = teacher_info[3]
    form_data = {
        'rwh': course_id,
        'zgh': teacher_id,
        'pjcs': pjcs,
        'kcdm': '',
        'pageXnxq': page_xnxq
    }
    r = session.post(jiaowu_url + "xspj/toAddPjjs",
                     data=form_data)
    assert (r.status_code == 200)
    s = BeautifulSoup(r.content, "html.parser")
    form = s.find('form', id='queryform')
    entries = form.find_all('input', type='hidden')
    form_data2 = defaultdict(list)
    for entry in entries:
        if entry.has_attr('name'):
            form_data2[entry['name']].append(entry['value'])
    entries = form.find_all('input', id='zbdm')
    for i, entry in enumerate(entries):
        option = entry.find_next_sibling('td').input
        if i == 0:
            option = option.find_next_sibling('input')
        form_data2[option['name']].append(option['value'])
    r2 = session.post(jiaowu_url + 'xspj/saveXspj',
                      data=form_data2)
    assert (r2.status_code == 200)
    print('success!')


def auto_evaluation():
    global page_xnxq
    r = session.get(jiaowu_url + 'xspj/Fxpj_fy',
                    allow_redirects=False)
    assert (r.status_code == 200)
    soup = BeautifulSoup(r.content, 'html.parser')
    yellow_spans = soup.find_all('span', class_='yellow')
    teachers = []
    page_xnxq = soup.find('select', id='xnxq').find('option', selected=True)['value']
    for span in yellow_spans:
        teachers += span.find_all('a')
    for teacher in teachers:
        assess_item(teacher)
    print("all job done!")


def auto_judge():
    print('《北航自动评教脚本》')
    print('请确保在校园网环境下或访问 https://vpn.buaa.edu.cn/ 下载客户端VPN')
    username = input('请输入统一认证登陆账号：')
    password = input('请输入统一认证登陆密码：')
    if login(username, password):
        auto_evaluation()
    else:
        print("账号或者密码错误(请确保连入校园网)")


auto_judge()

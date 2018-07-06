import requests
from bs4 import BeautifulSoup

headers = {
    'Cookie': 'JSESSIONID=2f88b1mLwrV8Yx9SyDh1yLJQzQJzR1HF9qPCKPql63LMTXfgpnl5!-822511665'
}
res = requests.get("http://10.200.21.61:7001/ieas2.1/xspj/Fxpj_fy",
    headers=headers, allow_redirects=False)
if res.status_code != 200:
    print("can't load page")
    exit()

soup = BeatifulSoup(res.content)

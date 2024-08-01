# 新版评教系统自动评教
# 使用selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import random
from time import sleep
from selenium.webdriver.chrome.options import Options
#
chrome_options = Options()
# chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
# chrome_options.add_argument(
#     'blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
# # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# chrome_options.add_argument('--headless')
chrome_options.add_experimental_option("detach", True)  # 使得浏览器不自动关闭

user_info = {
    'username': 'xxx',
    'password': 'xxx'
}


browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 5)

login_url = 'https://sso.buaa.edu.cn/login?service=https%3A%2F%2Fspoc.buaa.edu.cn%2Fpjxt%2Fcas'

browser.get(login_url)
wait.until(EC.frame_to_be_available_and_switch_to_it(
    browser.find_element(By.ID, 'loginIframe')))

browser.find_element(By.ID, 'unPassword').send_keys(user_info['username'])
browser.find_element(By.ID, 'pwPassword').send_keys(user_info['password'])
browser.find_element(By.XPATH,
                     '//*[@id="content-con"]/div[1]/div[7]/input').click()

evaluation_url = 'https://spoc.buaa.edu.cn/pjxt/authentication/main'

browser.get(evaluation_url)
wait.until(EC.frame_to_be_available_and_switch_to_it(
    browser.find_element(By.ID, 'mains_index_iframe')
))


browser.find_element(By.XPATH,
                     '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/ul/li/h3/a').click()
browser.implicitly_wait(5)
browser.switch_to.default_content()
browser.find_element(By.ID, 'mains_2078_01_link').click()

wait.until(EC.frame_to_be_available_and_switch_to_it(
    browser.find_element(By.ID, 'mains_2078_01_iframe')
))

browser.find_element(By.XPATH,
                     '//*[@id="app"]/div/div[2]/div[1]/div/div/div[1]/div[2]/table/tbody/tr/td[9]/div/div/button').click()
browser.implicitly_wait(5)

for outer_item in range(1, 5):
    try:
        element = browser.find_element(
            By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[1]/div[2]/table/tbody/tr[{outer_item}]/td[6]/div/div/button[1]')
        if element.text == '去评价':
            element.click()
            elements = browser.find_elements(
                By.CSS_SELECTOR, '.ivu-btn-primary')
            while len(elements) > 0:
                item = elements.pop(0)
                item.click()
                browser.implicitly_wait(5)
                arr = [1, 1, 2, 2, 3, 3]
                for i in range(1, 7):
                    index = random.randint(0, len(arr)-1)
                    choice = arr.pop(index)
                    browser.find_element(
                        By.XPATH, f'//*[@id="app"]/div/div/div[2]/div/div[1]/div/div[2]/div/div[{i}]/div/div/div[3]/div[2]/div/label[{choice}]/span[1]/input').click()
                browser.find_element(
                    By.XPATH, '//*[@id="app"]/div/div/div[3]/button[2]').click()
                wait.until(EC.presence_of_element_located((
                    By.CLASS_NAME, 'ivu-modal-content')))
                browser.find_element(
                    By.CSS_SELECTOR, 'body > div:nth-child(6) > div.ivu-modal-wrap > div > div > div > div > div.ivu-modal-confirm-footer > button.ivu-btn.ivu-btn-primary').click()
                wait.until(EC.presence_of_element_located((
                    By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button')))
                sleep(1)
                elements = browser.find_elements(
                    By.CSS_SELECTOR, '.ivu-btn-primary')
            browser.find_element(
                By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button').click()
    except Exception as e:
        print(e)
    finally:
        print(f'课程类型{outer_item}评教完成')


print('评教完成')

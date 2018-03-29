import time
import json
from selenium import webdriver
from users import ACCOUNT, PASSWORD

class GetCookies:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('http://weibo.com/login.php') # load the login page
        time.sleep(10)

    def run(self):
        try:
            self.driver.find_element_by_xpath('//div[@class="info_list username"]/div/input').send_keys(ACCOUNT) # ACCOUNT should be defined in users.py
            print('input username')
        except:
            print('username error!')
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('//div[@class="info_list password"]/div/input').send_keys(PASSWORD) # ACCOUNT should be defined in users.py
            print('input password')
        except:
            print('password error!')
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('//div[@class="info_list login_btn"]/a').click() # click the botton to login
            print('click to login')
        except:
            print('click error!')
        time.sleep(10) # wait to login
        cookies={"cookies":[]}
        for item in self.driver.get_cookies():
            cookies["cookies"].append({"name":item["name"], "value":item["value"]})
        cookies["cookies"]=list(cookies["cookies"])
        file = open('cookies.json', 'w', encoding='utf-8')
        json.dump(cookies, file, indent=4, sort_keys=False, ensure_ascii=False)
        file.close()
        self.driver.close()


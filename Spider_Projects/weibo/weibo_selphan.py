# -*- coding: utf-8 -*-

# Selenium & Phantomjs Version

import time
import collections
import getpass
from selenium import webdriver
import sys
sys.path.append('../template')
import mjson

driver = webdriver.Chrome()
#  driver = webdriver.PhantomJS()
driver.get('http://passport.weibo.com/')
origin_url = driver.current_url
username = driver.find_element_by_id('username')
password = driver.find_element_by_id('password')
sbtn = driver.find_element_by_class_name('smb_btn')
save_btn = driver.find_element_by_id('save_btn')
safe_login = driver.find_element_by_id('safe_login')

uname = input("Plese enter your sina weibo account name:")
pwd = getpass.getpass("Please enter your account password:")
username.send_keys(uname)  # send username
password.send_keys(pwd)  # send password
safe_login.click()  # uncheck safe login
time.sleep(1)
sbtn.submit()

time.sleep(5)  # wait for page load

if driver.current_url == origin_url:
    print("Error happens, log in fails")
else:
    print("Log in successfully")
    driver.get("http://weibo.com/2065392673/fans"
               "?from=100505&wvr=6&mod=headfans&current=fans#place")
    time.sleep(1)
    numbers = driver.find_elements_by_xpath('//em[@class="count"]')
    images = driver.find_elements_by_xpath('//dt[@class="mod_pic"]/a/img')
    name = []
    following = []
    follower = []
    weibo = []
    img = []

    for i in range(len(numbers)):
        number = numbers[i].text
        if i % 3 == 0:
            following.append(number)
        elif i % 3 == 1:
            follower.append(number)
        else:
            weibo.append(number)

    for image in images:
        name.append(image.get_attribute('alt'))
        img.append(image.get_attribute('src'))
    DIC = {}
    OUTPUT = 'output.json'
    for i in range(len(name)):
        content = collections.OrderedDict([("Name", name[i]),
                                           ("Following", following[i]),
                                           ("Follower", follower[i]),
                                           ("Weibo", weibo[i]),
                                           ("Image", img[i])])
        DIC[str(i)] = content
    ol = sorted(list(DIC.items()), key=lambda x: int(x[0]))  # ordered list
    ol = [s[1] for s in ol]
    my_file = mjson.RWfile(OUTPUT)
    my_file.write_in(ol)
driver.quit()

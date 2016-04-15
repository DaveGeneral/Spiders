# -*- coding: utf-8 -*-

# Cookie Version

import time
import collections
import getpass
import sys
sys.path.append('../template')
import mjson

if driver.current_url == origin_url:
    print("Error happens, log in fails")
else:
    print("Log in successfully")
    driver.get("http://weibo.com/2065392673/fans"
               "?from=100505&wvr=6&mod=headfans&current=fans#place")
    time.sleep(3)
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

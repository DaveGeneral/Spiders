#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import os
import shutil
import urllib.request

path = os.getcwd()
path = os.path.join(path, 'temp')
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

page_sum = 5
img_startnum = 1
url = "http://baozoumanhua.com/gif/month/page/"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                         'AppleWebKit/537.11'
                         '(KHTML,like Gecko)'
                         'Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,'
                     'application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

print("""
    ###############################

         BaoZou Gif Crawler
           Author: Ke Yi

    ###############################
""")

for count in range(page_sum):
    req = urllib.request.Request(
        url=url + str(count + 1),
        headers=headers
    )
    content = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(content, "lxml")
    img_content = soup.findAll('img', src=True, style="width:460px;")
    url_list = [img['src'] for img in img_content]
    print("\nFile number in page %s: %s" % (req.full_url, len(url_list)))
    for i in range(url_list.__len__()):
        try:
            imgurl = url_list[i]
            imgname = str(img_startnum).zfill(4)
            filename = path + os.sep + imgname + ".gif"
            img_startnum += 1
            print(filename)
            urllib.request.urlretrieve(imgurl, filename)
        except Exception as e:
            print("Forbidden error, step to next one.")

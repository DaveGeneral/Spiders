#  Env python3+

import os

import urllib.request

import bs4

path = os.getcwd()
path = os.path.join(path, 'baozou')
if not os.path.exists(path):
    os.mkdir(path)

page_sum = 10
url = "http://baozoumanhua.com/gif/month/page/"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


imgnum = 1

for count in range(page_sum):
    req = urllib.request.Request(
        url=url + str(count + 1),
        headers=headers
    )
    print(req.full_url)
    content = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(content, "html.parser")
    img_content = soup.findAll('img', src=True, style="width:460px;")
    url_list = [img['src'] for img in img_content]
    #  title_list = [img['alt'] for img in img_content]
    print(len(url_list))
    for i in range(url_list.__len__()):
        try:
            imgurl = url_list[i]
            imgname = str(imgnum).zfill(4)
            #  imgname = title_list[i] if title_list[i] !="" else str(imgnum).zfill(4)
            filename = path + os.sep + imgname + ".gif"
            imgnum += 1
            print(filename)
            urllib.request.urlretrieve(imgurl, filename)
        except Exception as e:
            print("Forbidden error, step to next one.")

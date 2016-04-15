# -*- coding: utf-8 -*-

# Cookie Version

import bs4
import collections
import requests
import sys
sys.path.append('../template')
import mparameter
import mjson


DIC = {}
UID = 2065392673
OUTPUT = 'output_cookie.json'
COOKIE = ""
with open("cookie.txt", 'r') as f:
    for line in f.readlines():
        COOKIE += line

print(COOKIE)


class WeiBoSpider(object):

    def __init__(self, uid):
        self.uid = uid

    def retrieve_page(self):
        url = "http://weibo.cn/%d/fans" % (self.uid)
        pm = mparameter.Parameter()
        headers = pm.get_headers()
        headers["Cookie"] = COOKIE
        soup = "Flag"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            status = response.status_code
            if status == 200:
                soup = bs4.BeautifulSoup(response.text, "lxml")
            else:
                print("%s error to reach the server %s" % (status, url))
        except Exception:
            print("Error happens! Please check your requests.")
        return soup

    def get_info(self, soup):
        tables = soup.find_all('td', attrs={'valign': 'top'})
        name = []
        uid = []
        img_url = []
        for i in range(len(tables)):
            temp = tables[i]
            if i % 2 == 0:
                img_url.append(temp.select('img')[0]['src'])
            else:
                name.append(temp.select("a")[0].string)
                s = temp.select("a")[1]['href']
                uid.append(s[s.find('=') + 1:s.find('&')])
        return [name, uid, img_url]

    def retrieve_content(self, soup):
        if soup != "FLAG":
            name, uid, img_url = self.get_info(soup)
            for i in range(len(name)):
                content = collections.OrderedDict([("Name", name[i]),
                                                   ("User_ID", uid[i]),
                                                   ("Image_Url", img_url[i])])
                DIC[str(i)] = content


def main():
    my_spider = WeiBoSpider(UID)
    soup = my_spider.retrieve_page()
    my_spider.retrieve_content(soup)
    ol = sorted(list(DIC.items()), key=lambda x: int(x[0]))  # ordered list
    ol = [s[1] for s in ol]
    my_file = mjson.RWfile(OUTPUT)
    my_file.write_in(ol)

if __name__ == '__main__':
    main()

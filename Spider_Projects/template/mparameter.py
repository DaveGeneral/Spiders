import time
import random


uafile = "../data/user_agents.txt"


class HEAD(object):

    def __init__(self):
        pass

    def get_UserAgent(self, uafile):
        uas = []
        with open(uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1:-1 - 1])
        random.shuffle(uas)
        return uas

    def get_header(self):
        uas = self.get_UserAgent(uafile)
        ua = random.choice(uas)
        headers = {'User-Agent': ua,
                   'Accept': 'text/html,application/xhtml+xml,'
                   'application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
        print(headers)
        time.sleep(3)

    def get_proxies(self):
        proxies = {'http': 'http://10.0.0.1:8080',
                   'https': 'http://10.0.0.1:4444'}
        return proxies
t = HEAD()
while True:
    t.get_header()

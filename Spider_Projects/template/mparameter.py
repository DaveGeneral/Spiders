import random


uafile = "../data/user_agents.txt"


class Parameter(object):

    def __init__(self):
        pass

    def get_useragent(self, uafile):
        n = random.randint(0, 888)
        f = open(uafile, 'r')
        for line in f.readlines()[n:n + 1]:
            f.close()
            return line.strip()[1:-1]

    def get_headers(self):
        ua = self.get_useragent(uafile)
        headers = {'User-Agent': ua,
                   'Accept': 'text/html,application/xhtml+xml,'
                   'application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'gzip,deflate',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
        return headers

    def get_proxies(self):
        proxies = {'http': 'http://10.0.0.1:8080',
                   'https': 'http://10.0.0.1:4444'}
        return proxies

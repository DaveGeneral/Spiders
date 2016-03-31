import bs4

import re

import requests

url = "https://movie.douban.com/top250?start=200&filter="
content = requests.get(url).text
soup = bs4.BeautifulSoup(content, "lxml")
quote = soup.select('.bd')[1:]
count = 0
for x in quote:
    if x.select('.inq'):
        m = x.select('.inq')
        n = x.findAll("p", {"class": ""})
        print(m[0].string)
        for y in n[0].stripped_strings:
            print(y)
        count += 1
print(count)
titles = soup.select('.hd')
for x in titles:
    temp = x.select('a span')
    name = ''.join(re.sub(r'\s+', ' ', s.string) for s in temp)
    print(name, len(name))
print(len(titles))

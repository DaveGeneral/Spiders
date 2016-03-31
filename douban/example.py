import bs4

import requests

url = "https://movie.douban.com/top250?start=225&filter="
content = requests.get(url).text
soup = bs4.BeautifulSoup(content, "lxml")
quote = soup.select('.bd')[1:]
print(quote[0])
count = 0
for x in quote:
    if x.select('.quote'):
        director = x.findAll("p", {"class": ""})
        print(director.string)
        count += 1

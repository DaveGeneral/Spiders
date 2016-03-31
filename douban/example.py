import bs4

import requests

url = "https://movie.douban.com/top250?start=225&filter="
content = requests.get(url).text
soup = bs4.BeautifulSoup(content, "lxml")
#  quote = soup.select('.bd')[1:]
#  count = 0
#  for x in quote:
#  if x.select('.inq'):
#  m = x.select('.inq')
#  n = x.findAll("p", {"class": ""})
#  #  n = x. select('string.')
#  print(m[0].string)
#  for y in n[0].stripped_strings:
#  print(y)
#  count += 1
#  print(count)
titles = soup.select('.hd')
#  print(titles)
for x in titles:
    temp = x.select('span')
    eng = temp[0].string
    local = temp[1].string
    alias = temp[2].string
    print(eng, local, alias)
print(len(titles))

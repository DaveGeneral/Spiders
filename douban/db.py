import MySQLdb

class DoubanDB(object):


    def __init__(self):
        pass


conn = MySQLdb.connect(host="localhost", user="spider",
                       passwd="pwd123456", port=3306,
                       db='Movie', charset="utf8")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Douban")
sql = """CREATE TABLE Douban(
         Rank INT NOT NULL,
         Name VARCHAR(100) NOT NULL,
         Rating FLOAT NOT NULL,
         Comment VARCHAR(100) NOT NULL,
         ImgUrl VARCHAR(100) NOT NULL)"""

cur.execute(sql)
sql = """INSERT INTO Douban(
Rank, Name, Rating, Comment, ImgUrl)
VALUES ("10", 'taowang', '8.6', '201424 人评价', "www.google.com");"""
try:
    cur.execute(sql)
    conn.commit()
except:
    # Rollback in case there is any error
    conn.rollback()

try:
    cur.execute("SELECT * FROM Douban;")
    lines = cur.fetchall()
    for row in lines:
        rank = row[0]
        name = row[1]
        rating = row[2]
        comment = row[3]
        imgurl = row[4]
        print(rank, name, rating, comment, imgurl)
except:
    print("Error: unable to fecth data")
cur.close()
conn.close()

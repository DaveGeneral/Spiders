import MySQLdb

conn = MySQLdb.connect(host="localhost", user="spider",
                       passwd="pwd123456", port=3306,
                       db='Movie', charset="utf8")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Top250")
sql = """CREATE TABLE Top250(
         Rank INT NOT NULL,
         Name VARCHAR(50) NOT NULL,
         Rating FLOAT NOT NULL,
         Comment INT NOT NULL,
         ImgUrl VARCHAR(100) NOT NULL)"""
cur.execute(sql)
cur.close()
conn.close()

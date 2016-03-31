import MySQLdb


class DoubanDB(object):

    def __init__(self):
        pass

    def table_create(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS Douban")
        sql = """CREATE TABLE Douban(
                 Rank INT NOT NULL,
                 Name VARCHAR(100) NOT NULL,
                 Rating FLOAT NOT NULL,
                 Comment VARCHAR(100) NOT NULL,
                 ImgUrl VARCHAR(100) NOT NULL)"""
        cursor.execute(sql)
        return

    def table_insert(self, conn, cursor):
        sql = """INSERT INTO Douban(
        Rank, Name, Rating, Comment, ImgUrl)
        VALUES ("10", 'taowang', '8.6', '201424 人评价', "www.google.com");"""
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()

    def table_select(self, cursor):
        try:
            cursor.execute("SELECT * FROM Douban;")
            lines = cursor.fetchall()
            for row in lines:
                rank = row[0]
                name = row[1]
                rating = row[2]
                comment = row[3]
                imgurl = row[4]
                print(rank, name, rating, comment, imgurl)
        except:
            print("Error: unable to fecth data")

    def start_db(self, datas):
        my_conn = MySQLdb.connect(host="localhost", user="spider",
                                  passwd="pwd123456", port=3306,
                                  db='Movie', charset="utf8")
        my_cursor = my_conn.cursor()
        self.table_create(my_cursor)
        self.table_insert(my_conn, my_cursor)
        self.table_select(my_cursor)
        my_cursor.close()
        conn.close()

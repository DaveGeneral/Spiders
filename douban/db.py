import MySQLdb

import warnings

warnings.filterwarnings("ignore")


class DoubanDB(object):

    def __init__(self):
        self.host = "localhost"
        self.user = "spider"
        self.password = "pwd123456"
        self.port = 3306
        self.db_name = "Movie"
        self.tb_name = "Douban"

    def tb_create(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS " + self.tb_name + ";")
        sql = (
            "CREATE TABLE " + self.tb_name +
            "(Rank VARCHAR(10) NOT NULL,"
            "Name VARCHAR(500) NOT NULL,"
            "Rating VARCHAR(10) NOT NULL,"
            "Review_Number VARCHAR(100) NOT NULL,"
            "Summary VARCHAR(500) NOT NULL,"
            "Comment VARCHAR(500),"
            "Address VARCHAR(500) NOT NULL,"
            "Image_URL VARCHAR(500) NOT NULL)"
        )
        cursor.execute(sql)
        return

    def tb_insert(self, conn, cursor):
        sql = (
            "INSERT INTO " + self.tb_name +
            "(Rank, Name, Rating, Review_Number, Summary, Comment, Address, Image_URL)"
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
            % ('444', 'taowang', '9.6', '201424 人评价', "sumar", "cmt", "add", "www.google.com")
        )
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()
        return

    def tb_retrieve(self, cursor):
        try:
            cursor.execute("SELECT * FROM " + self.tb_name + ";")
            lines = cursor.fetchall()
            for row in lines:
                print(row)
        except:
            print("Error: unable to fecth data")

        return

    def start_db(self, datas):
        my_conn = MySQLdb.connect(host=self.host, user=self.user,
                                  passwd=self.password, port=self.port,
                                  db=self.db_name, charset="utf8")
        my_cursor = my_conn.cursor()
        self.tb_create(my_cursor)
        self.tb_insert(my_conn, my_cursor)
        self.tb_retrieve(my_cursor)
        my_cursor.close()
        my_conn.close()


my_database = DoubanDB()
my_database.start_db(1)

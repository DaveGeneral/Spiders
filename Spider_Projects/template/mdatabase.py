import MySQLdb
import re
import warnings
import time


warnings.filterwarnings("ignore")


class DB(object):

    def __init__(self, db_name, tb_name):
        self.host = "localhost"
        self.user = "spider"
        self.password = "pwd123456"
        self.port = 3306
        self.db_name = db_name
        self.tb_name = tb_name
        self.tb_keys = []
        self.connection = MySQLdb.connect(host=self.host, user=self.user,
                                          passwd=self.password, port=self.port,
                                          db=self.db_name, charset="utf8")

    def tb_drop(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS " + self.tb_name + ";")
        return

    def tb_create(self, cursor):
        tb_keys = self.tb_keys
        sql = ("CREATE TABLE " + self.tb_name + " (" +
               " VARCHAR(1000), ".join(tuple(tb_keys)) +
               " VARCHAR(1000));"
               )
        cursor.execute(sql)
        return

    def tb_insert(self, conn, cursor, tb_values):
        #  solve single quote problem when inserting
        tb_keys = self.tb_keys
        tb_values = [re.sub(r"'", "''", x) for x in tb_values]
        sql = ("INSERT INTO " + self.tb_name + "(" +
               ", ".join([x for x in tb_keys]) + ") VALUES(" +
               ", ".join(["'" + x + "'" for x in tb_values]) + ");"
               )
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        return

    def tb_retrieve(self, cursor):
        try:
            cursor.execute("SELECT * FROM " + self.tb_name + ";")
            lines = cursor.fetchall()
            for row in lines:
                for i in range(len(row)):
                    print(self.tb_keys[i], row[i])
        except:
            print("Error: unable to fecth data")
        return

    def get_items(self, raw_datas):
        clean_keys = []
        clean_values = []
        for x in raw_datas.values():
            clean_keys = list(x.keys())
            clean_values.append(list(x.values()))
        return [clean_keys, clean_values]

    def start_db(self, datas):
        st = time.time()
        my_conn = self.connection
        my_cursor = my_conn.cursor()
        self.tb_keys, my_values = self.get_items(datas)
        self.tb_drop(my_cursor)
        self.tb_create(my_cursor)
        for x in my_values:
            self.tb_insert(my_conn, my_cursor, x)
        self.tb_retrieve(my_cursor)  # print results from mysql database
        my_cursor.close()
        my_conn.close()
        print("DB costs ", time.time()-st)

import MySQLdb
import re
import warnings


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
        self.tb_values = []
        self.conn = MySQLdb.connect(host=self.host, user=self.user,
                                    passwd=self.password, port=self.port,
                                    db=self.db_name, charset="utf8")
        print("Database Connection Setup...")

    def db_process(self, raw_datas):
        clean_keys = []
        clean_values = []
        for x in raw_datas.values():
            clean_keys = list(x.keys())
            clean_values.append(list(x.values()))
        self.tb_keys = clean_keys
        self.tb_values = clean_values

    def tb_drop(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS " + self.tb_name + ";")

    def tb_create(self, cursor):
        tb_keys = self.tb_keys
        sql = ("CREATE TABLE " + self.tb_name + " (" +
               ", ".join([x + " VARCHAR(1000)" for x in tb_keys]) + ");"
               )
        cursor.execute(sql)

    def db_insert(self, datas):
        print("Database Insertion Begins...")
        conn = self.conn
        cursor = conn.cursor()
        self.db_process(datas)
        self.tb_drop(cursor)  # drop existing table to erase data
        self.tb_create(cursor)
        for row in self.tb_values:
            #  solve single quote problem when inserting
            tb_values = [re.sub(r"'", "''", x) for x in row]
            sql = ("INSERT INTO " + self.tb_name + "(" +
                   ", ".join([x for x in self.tb_keys]) + ") VALUES(" +
                   ", ".join(["'" + x + "'" for x in tb_values]) + ");"
                   )
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
        print("Database Insertion Ends.")

    def db_retrieval(self):
        print("Database Retrieval Begins...")
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM " + self.tb_name + ";")
            lines = cursor.fetchall()
            for row in lines:
                for i in range(len(row)):
                    print(self.tb_keys[i], ":", row[i])
                print("")
        except:
            print("Error: Unable to fecth data")
        print("Database Retrieval Ends.")

    def db_close(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.close()
        conn.close()
        print("Database Connection Close.")

import MySQLdb
import re
import warnings


warnings.filterwarnings("ignore")


class DoubanDB(object):

    def __init__(self, db_name, tb_name):
        self.host = "localhost"
        self.user = "spider"
        self.password = "pwd123456"
        self.port = 3306
        self.db_name = db_name
        self.tb_name = tb_name
        self.connection = MySQLdb.connect(host=self.host, user=self.user,
                                          passwd=self.password, port=self.port,
                                          db=self.db_name, charset="utf8")

    def tb_drop(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS " + self.tb_name + ";")
        return

    def tb_create(self, cursor):
        sql = (
            "CREATE TABLE " + self.tb_name +
            "(Rank VARCHAR(10) NOT NULL,"
            "Name VARCHAR(500) NOT NULL,"
            "Rating VARCHAR(10) NOT NULL,"
            "Review_Number VARCHAR(100) NOT NULL,"
            "Summary VARCHAR(500) NOT NULL,"
            "Comment VARCHAR(500),"
            "Address VARCHAR(500) NOT NULL,"
            "Image_URL VARCHAR(500) NOT NULL);"
        )
        cursor.execute(sql)
        return

    def tb_insert(self, conn, cursor, raw):
        #  solve single quote problem when inserting
        clean = [re.sub(r"'", "''", x) for x in raw]
        print(clean)
        sql = (
            "INSERT INTO " + self.tb_name +
            "(Rank, Name, Rating, Review_Number, "
            "Summary, Comment, Address, Image_URL)"
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
            % (clean[0], clean[1], clean[2], clean[3],
                clean[4], clean[5], clean[6], clean[7])
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
                print(row)
        except:
            print("Error: unable to fecth data")
        return

    def get_items(self, dic):
        temp = []
        for x in dic.values():
            temp.append(x.values())
        return temp

    def start_db(self, datas):
        my_conn = self.connection
        my_cursor = my_conn.cursor()
        self.tb_drop(my_cursor)
        self.tb_create(my_cursor)
        datas = self.get_items(datas)
        print(type(datas))
        for x in datas:
            print(type(x))
            #  print(x)
            self.tb_insert(my_conn, my_cursor, x)
        #  print results from mysql database
        #  self.tb_retrieve(my_cursor)
        my_cursor.close()
        my_conn.close()

my_datas = {
    "1": {
        "Rank": "1",
        "Name": "肖申克的救赎 / The Shawshank Redemption / 月黑高飞(港) / 刺激1995(台)",
        "Rating": "9.6",
        "Review_Number": "685767人评价",
        "Summary": "导演: 弗兰克·德拉邦特 Frank Darabont",
        "Comment": "希望让人自由。",
        "Address": "https://movie.douban.com/subject/1292052/",
        "Image_URL": "https://img1.doubanio.com/view/movie",
    },
    "2": {
        "Rank": "2",
        "Name": "这个杀手不太冷 / Léon / 杀手莱昂 / 终极追杀令(台)",
        "Rating": "9.4",
        "Review_Number": "654870人评价",
        "Summary": "导演: 吕克·贝松 Luc Besson   主演: 让·雷诺",
        "Comment": "怪蜀黍和小萝莉不得不说的故事。",
        "Address": "https://movie.douban.com/subject/1295644/",
        "Image_URL": "https://img3.doubanio.com/view/movie_post",
    }}
#  my_datas = [['1', "Holo", '9.2', '10243人评价', "综述",
#  "评论", "www.google.com", "www.img.com"],
#  ['2', "Yes", "8.7", "23341人评价", "zongshu",
#  "pinglun", "www.github.com", "www.picture.com"]]
t = DoubanDB("Movie", "Douban")
t.start_db(my_datas)

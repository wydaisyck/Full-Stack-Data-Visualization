from pymongo import MongoClient
import pandas as pd


class MongoData():
    def __init__(self, server, port, user, passwd, db_name, table_name, charset='utf8'):
        self.server = server
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.db_name = db_name
        self.table_name = table_name

    def connect(self):
        print('开始连接数据库！')
        client = MongoClient(self.server, self.port)
        auth = client.admin
        auth.authenticate(self.user, self.passwd)
        db = client[self.db_name]
        return db

    def get_data(self, sql=None):
        db = self.connect()
        table = db[self.table_name]
        if sql is None:
            data = pd.DataFrame(list(table.find()))
        else:
            data = pd.DataFrame(list(table.find(eval(sql))))
        print('数据读取成功！')
        return data

    def process_data(self):
        df = self.get_data()
        df = df.sort_values(by=['date'])
        df['date'] = df['date'].apply(lambda x: int(x.replace('-', '')))
        df = df.fillna(0.)
        return df

















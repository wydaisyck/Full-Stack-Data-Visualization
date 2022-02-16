from app import app
from app.utils.connectdb import MongoData
from app.utils.get_table_result import getDatasInStore

if __name__ == "__main__":
    dh = MongoData(server="", port="", user='wangyidan', passwd='wangyidan321', db_name="zcs", table_name="factor_layering_return")
    pdata = dh.process_data()
    pdata.to_pickle('mongodata.pkl')
    print("数据存储成功！")
    app.run()

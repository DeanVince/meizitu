# coding=utf8
from pymysql import Connect

class MysqlUtil(object):
    def __init__(self):
        self.conn = Connect(host='39.96.63.98', port=3306, database='meizitu', user='test',
                       password='123456',
                       charset='utf8')
        self.cursor = self.conn.cursor()

    def execute(self,sql,params):
        self.cursor.execute(sql,params)
        self.conn.commit()
        return self.cursor

    def __delete__(self, instance):
        self.cursor.close()
        self.conn.close()

def main():

    params = []

    # params.append(input("请输入名字："))
    sql_util = MysqlUtil()
    sql = 'insert into test VALUES (0,%s)'
    sql = 'select * from test'
    cursor = sql_util.execute(sql,params)
    print(cursor.fetchall())

if __name__ == '__main__':
    main()


import requests
import urllib3
import json
from datetime import datetime
from datetime import timedelta
import time
import pymysql
urllib3.disable_warnings()

class GetDataFromMysql :
    def __init__(self, table_name):
        self.dbb = pymysql.connect(host='localhost',
                              user='root',
                              port=3306,
                              password='test112211',
                              db='test',
                              cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.dbb.cursor()
        self.table_name = table_name


    def get_data(self):
        try:
            self.cursor = self.dbb.cursor()
            sql = 'SELECT * from %s ORDER BY ID DESC LIMIT 20' % self.table_name

            self.cursor.execute(sql)
            self.dbb.commit()
            return self.cursor.fetchall()
        except:
            self.dbb.rollback()
            print('get_data 出现错误')
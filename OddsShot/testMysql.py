import pymysql
import time

db = pymysql.connect(host='localhost',
                              user='root',
                              port=3306,
                              password='test112211',
                              db='test',
                              cursorclass=pymysql.cursors.DictCursor)

while True:
    with db.cursor() as cursor:
        sql = "SELECT * from shaba ORDER BY ID DESC LIMIT 20"
        cursor.execute(sql)
        db.commit()
        print(cursor.fetchall())
    time.sleep(5)

cursor.close()
db.close()
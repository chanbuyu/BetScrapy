# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings


class ScrapyseleniumPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.host = settings.get('MYSQL_HOST', 'localhost')
        self.dbname = settings.get('MYSQL_DBNAME', 'scrapy')
        self.user = settings.get('MYSQL_USER', 'root')
        self.password = settings.get('MYSQL_PASSWORD', '')
        print('初始化数据库', self.host, self.dbname, self.user, self.password)

    def open_spider(self, spider):
        #print('正在调用open_spider.....')
        self.conn = pymysql.connect(host=self.host,
                                    db=self.dbname,
                                    port=3306,
                                    user=self.user,
                                    password=self.password,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        #print('正在调用process_item.....')
        sql = '''
            INSERT INTO bbsport (time, league, host, guest, bigsmall, bigodds, smallodds) VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        values = (item['time'], item['league'], item['host'], item['guest'], item['bigSmall'], item['bigOdds'], item['smallOdds'])
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            #print('插入数据库成功！！！！！！！！！！')
        except:
            self.conn.rollback()
            raise DropItem('Failed to insert item into database')
        return item



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import csv
import json
import mysql.connector
import psycopg2
from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

# class MongoDBUnitopPipeline:
#     def __init__(self):
#         self.client = pymongo.MongoClient('mongodb+srv://minhthien2705:Thien2705@minhthien.5bz9lq9.mongodb.net/?retryWrites=true&w=majority&appName=MinhThien')
#         self.db = self.client["unitop"]

#     def process_item(self, item, spider):
#         collection = self.db['UnitopAppCrawler']
#         try:
#             collection.insert_one(dict(item))
#             return item
#         except Exception as e:
#             raise DropItem(f"Error in Pipeline:{e}")

# class JsonDBUnitopPipeline:
#     def process_item(self, item, spider):
#         self.file = open('unitop.json','a',encoding='utf-8')
#         line = json.dumps(dict(item), ensure_ascii=False) + ','+'\n'
#         self.file.write(line)
#         self.file.close
#         return item

# class MySQLPipeline:

#     def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db):
#         self.mysql_host = mysql_host
#         self.mysql_user = mysql_user
#         self.mysql_password = mysql_password
#         self.mysql_db = mysql_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mysql_host=crawler.settings.get('MYSQL_HOST'),
#             mysql_user=crawler.settings.get('MYSQL_USER'),
#             mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
#             mysql_db=crawler.settings.get('MYSQL_DB')
#         )

#     def open_spider(self, spider):
#         self.conn = mysql.connector.connect(
#             host=self.mysql_host,
#             user=self.mysql_user,
#             password=self.mysql_password,
#             database=self.mysql_db
#         )
#         self.cursor = self.conn.cursor()

#     def close_spider(self, spider):
#         self.conn.close()
#     def process_item(self, item, spider):
#         # Cập nhật truy vấn INSERT để chứa tất cả các cột mới
#         query = "INSERT INTO course_data (coursename, lecturer, intro, course_description, votenumber, rating, newfee, oldfee, lessonnum, courseUrl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        
#         # Chuẩn bị các giá trị từ đối tượng item
#         values = (
#             item['coursename'],
#             item['lecturer'],
#             item['intro'],
#             item['describe'],
#             item['votenumber'],
#             item['rating'],
#             item['newfee'],
#             item['oldfee'],
#             item['lessonnum'],
#             item['courseUrl']
#         )
        
#         # Thực thi truy vấn INSERT với các giá trị đã chuẩn bị
#         self.cursor.execute(query, values)
        
#         # Lưu các thay đổi vào cơ sở dữ liệu
#         self.conn.commit()
        
#         return item

class CSVDBUnitopPipeline:
    def process_item(self, item, spider):
        with open('unitop_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['courseUrl','product_main','rating','in_stock','star','description','upc','product_type','price_exc','price_inc','tax','availability','nor']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

            # Kiểm tra nếu file CSV chưa có header thì ghi header
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(item)

        return item
# class PostgreSQLPipeline:
#     def open_spider(self, spider):
#         self.conn = psycopg2.connect(
#             dbname='unitop',
#             user='postgres',
#             password='12345',
#             host='localhost',
#             port='5432'
#         )
#         self.cur = self.conn.cursor()

#     def close_spider(self, spider):
#         self.cur.close()
#         self.conn.close()

#     def process_item(self, item, spider):
#         try:
#             query = "INSERT INTO course_data (coursename, lecturer, intro, course_description, votenumber, rating, newfee, oldfee, lessonnum, courseurl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#             values = (
#                 item['coursename'],
#                 item['lecturer'],
#                 item['intro'],
#                 item['describe'],
#                 item['votenumber'],
#                 item['rating'],
#                 item['newfee'],
#                 item['oldfee'],
#                 item['lessonnum'],
#                 item['courseUrl']
#             )
#             self.cur.execute(query, values)
#             self.conn.commit()
#         except Exception as e:
#             # Xử lý ngoại lệ ở đây, ví dụ:
#             print(f"Error: {e}")
#             self.conn.rollback()  # Hủy bỏ transaction nếu có lỗi
#         return item   
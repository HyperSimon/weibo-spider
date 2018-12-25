# coding=utf-8

from pymongo import MongoClient

# 数据库的连接
client = MongoClient('localhost', 27017)
db = client.panda
table_chengshi = db.chengshi

print len(table_chengshi.distinct('mblog.mid'))

print table_chengshi.find({'mblog.mid': '4300973306480688'}).count()

for i in table_chengshi.find({'mblog.mid': '4300973306480688'}, {'mblog.user.id': 1}):
    print i




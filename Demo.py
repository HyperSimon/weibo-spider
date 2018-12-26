# coding=utf-8
import random

from pymongo import MongoClient

import files

client = MongoClient('localhost', 27017)

# 连接所需数据库,test为数据库名
db = client.test
collection = db.test


def insertValue():
    collection.insert({"name": "wangzhen"})


def query():
    for item in collection.find():
        print(item)


def aa():
    name = 'wangzhen'
    print(name)


def save(filename, contents):
    fh = open(filename, 'w+')
    fh.write(contents)
    fh.close()


def read(filename):
    fh = open(filename, "r")
    content = fh.readline()
    return content


# save("sinceid.txt", "wangzhen")
# print read("sinceid.txt")

name = None
if name != 0:
    print("name not equal 0")

name = 0

commentId = 1111
url = "https://m.weibo.cn/comments/hotFlowChild?" \
      "cid=%s&" \
      "max_id=0&" \
      "max_id_type=0" % (str(commentId))

# a = [11, 11, 11]
# for index, i in enumerate(a):
#     print(i)
#
a = [{'value': 2, 'age': 3}, {'value': 3, 'age': 4}]

print(files.read('./property/account.txt').split(',')[0])

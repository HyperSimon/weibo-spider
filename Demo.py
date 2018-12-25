# coding=utf-8
import random

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# 连接所需数据库,test为数据库名
db = client.test
collection = db.test


def insertValue():
    collection.insert({"name": "wangzhen"})


def query():
    for item in collection.find():
        print item


def aa():
    name = 'wangzhen'
    print name


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
    print "name not equal 0"

name = 0
if name == None:
    print "name equal 0"

names = []
chinese = ['aa', 'bb', 'cc']
japanese = ['aa', 'bb', 'cc']
names.extend(chinese)
names.extend(japanese)
print names

print '%s 我叫白小飞 %s' % ('Python', 'Tab')

commentId = 1111
url = "https://m.weibo.cn/comments/hotFlowChild?" \
      "cid=%s&" \
      "max_id=0&" \
      "max_id_type=0" % (str(commentId))

print url

a = False
print a != False
a = []
print a != False
a = ['a', 'b']
print a != False

print random.randint(0, 1000) / 1000.0

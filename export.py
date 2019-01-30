# coding=utf-8
import json
import random
import time

import requests
from bson import ObjectId

from pymongo import MongoClient

import files

# 数据库的连接
client = MongoClient('localhost', 27017)
db = client.panda

table_chengshi = db.chengshi

allBlog = []
for blog in table_chengshi.find():
    allBlog.append(blog)
    files.save("property/blog.json", json.dumps(allBlog))

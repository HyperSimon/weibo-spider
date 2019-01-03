# coding=utf-8
import json

from pymongo import MongoClient

# 数据库的连接
from files import save

client = MongoClient('localhost', 27017)
db = client.panda
table_chengshi = db.chengshi


# 更新最后一条微博的id，不建议使用
def update_last_blog_id():
    data = table_chengshi.find().limit(1).sort([('_id', -1)])
    for d in data:
        last_blog_id = d['mblog']['idstr']
        save('sinceid.txt', last_blog_id)
        print(last_blog_id)


poster = []
for data in table_chengshi.find():
    user = data['mblog']['user']
    poster.append(user)

user_ids = []
r = {}
for user in poster:
    user_id = user['id']
    user_name = user['screen_name']
    if user_name not in r:
        r[user_name] = 1
    else:
        r[user_name] = r[user_name] + 1

l = []
for i in r:
    l.append({'username': i, 'post_times': r[i]})

l.sort(key=lambda x: x['post_times'], reverse=True)

print(json.dumps(l, sort_keys=True, indent=2, ensure_ascii=False))

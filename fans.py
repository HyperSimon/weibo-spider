# coding=utf-8
import json

import requests
from pymongo import MongoClient

import files

client = MongoClient('localhost', 27017)

# 连接所需数据库,test为数据库名
db = client.weibo
collection_fans = db.fans
collection_user = db.user

cookie = json.loads(files.read('property/cookie.txt'))  # 获取cookie

uid = "2327314842"
container_id = "231051_-_fans_-_%s" % uid
since_id = 1

followers_id = []
followers = []
users = []

headers = {
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    "Host": "passport.weibo.cn",
    "Connection": "keep-alive",
    "Content-Length": "339",
    "Origin": "https://passport.weibo.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4306305752058972",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
}


def fetch_fans(content_id, page):
    print("fetching %d 页数据" % page)
    url = "https://m.weibo.cn/api/container/getIndex" \
          "?containerid=%s" \
          "&since_id=%s" % (content_id, page)
    response = requests.get(url=url, cookies=cookie).json()
    cards = response['data']['cards']
    funs_card = filter(lambda c: "card_style" not in c, cards)
    for card_groups in funs_card:
        groups = card_groups['card_group']
        for group in groups:
            user = group['user']

            collection_user.insert(user)
            followers_id.append({'followerId': user['id']})


need_page = 20

funs_file = 'property/funs.json'
funs_json = files.read(funs_file)
print(funs_json)
start_page = json.loads(funs_json)["start_page"]
for i in range(need_page):
    fetch_fans(container_id, start_page + i)

va = {"start_page": need_page + start_page}
files.save(funs_file, json.dumps(va))

indb = []
has = collection_fans.find_one({'userId': uid})
for i in has['followers']:
    indb.append(i)

data = {'userId': uid, "followers": followers_id}
collection_fans.update({'userId': uid}, {"$set": data})
collection_fans.insert(data)

# coding=utf-8
import json

import requests
from pymongo import MongoClient

import mblog as blog

# 数据库的连接
import files

client = MongoClient('localhost', 27017)
db = client.panda
table_chengshi = db.chengshi

cookie = json.loads(files.read('cookie.txt'))  # 获取cookie


def get_weibo_data(since_id):
    url = "https://m.weibo.cn/api/container/getIndex" \
          "?extparam=%E5%A4%A7%E7%86%8A%E7%8C%AB%E6%88%90%E5%AE%9E" \
          "&containerid=100808b1f12e8d7f440882de1c1400ed74d2d5_-_feed" \
          "&luicode=20000174" \
          "&since_id=" + str(since_id)

    response = requests.get(url)
    rsp = json.loads(response.content)

    data = rsp['data']
    return data


def parse_data():
    sinceId = read('sinceid.txt')
    for i in range(500):
        print("正在读取第 " + str(i + 1) + " 页微博内容"),

        data = get_weibo_data(sinceId)
        cards = data['cards']

        for card in cards:
            if "show_type" in card:
                card_group = card['card_group']
                # for cg in card_group:
                #     mblog = cg['mblog']
                #     blogId = mblog['id']
                #     comments = blog.fetch_comments_of(blogId)
                #     liked = blog.fetch_like_user_of(blogId)
                #     mblog['comments'] = comments
                #     mblog['liked'] = liked
                #     cg['mblog'] = mblog

                table_chengshi.insert(card_group)
            else:
                print("不包含 show_type")

        if "pageInfo" in data:
            sinceId = data['pageInfo']['since_id']
        else:
            break

    save("sinceid.txt", str(sinceId))


def save(filename, contents):
    fh = open(filename, 'w+')
    fh.write(contents)
    fh.close()


def read(filename):
    fh = open(filename, "r")
    content = fh.readline()
    return content


parse_data()

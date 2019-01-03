# coding=utf-8
import json

import requests
from pymongo import MongoClient

# 数据库的连接
import files

client = MongoClient('localhost', 27017)
db = client.panda
table_chengshi = db.chengshi

cookie = json.loads(files.read('./property/cookie.txt'))  # 获取cookie


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


buffer = []
buffer_size = 100


def parse_data():
    sinceId = read('sinceid.txt')
    rg = 200
    for i in range(rg):
        print("正在读取第{0}页微博内容".format(i + 1))

        data = get_weibo_data(sinceId)
        cards = data['cards']

        for index, card in enumerate(cards):
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

                #  table_chengshi.insert(card_group) # use buffer instand
                buffer.extend(card_group)
            else:
                print("不包含 show_type")

        if "pageInfo" in data:
            sinceId = data['pageInfo']['since_id']
        else:
            break

        if len(buffer) >= buffer_size or i == rg - 1:
            # insert buffer to db and clear buffer
            print("当前 buffer:{0}, index:{1}".format(len(buffer), i))

            need_insert = []
            for b in buffer:
                value = table_chengshi.find_one({'mblog.id': b['mblog']['id']})
                if value is not None:
                    table_chengshi.update({'mblog.id': value['mblog']['id']}, {'$set': {"mblog": b['mblog']}})
                else:
                    need_insert.append(b)

            if len(need_insert) > 0:
                table_chengshi.insert_many(need_insert)
            print("更新%d条数据，新增%d条数据" % (len(buffer) - len(need_insert), len(need_insert)))

            buffer.clear()

            # log since id and save
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

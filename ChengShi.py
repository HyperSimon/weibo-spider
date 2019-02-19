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


def get_weibo_data(since_id):
    url = "https://m.weibo.cn/api/container/getIndex" \
          "?extparam=%E5%A4%A7%E7%86%8A%E7%8C%AB%E6%88%90%E5%AE%9E" \
          "&containerid=100808b1f12e8d7f440882de1c1400ed74d2d5_-_feed" \
          "&luicode=20000174" \
          "&since_id=" + str(since_id)

    data = []
    try:
        response = requests.get(url=url, headers=headers, timeout=2)
        print(response.content)
        rsp = json.loads(response.content)

        data = rsp['data']
    # except  as e:
    #     print(e)
    except Exception:
        print("异常")

    return data


buffer = []
buffer_size = 100


def parse_data():
    sinceId = read('sinceid.txt')
    rg = 500
    for i in range(rg):
        print("正在读取第{0}页微博内容".format(i + 1))

        data = get_weibo_data(sinceId)
        if len(data) < 1:
            break
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

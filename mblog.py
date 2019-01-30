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
table_comment = db.comment  # collection
table_chengshi = db.chengshi

cookie = json.loads(files.read('property/cookie.txt'))  # 获取cookie


def slow_down():
    time.sleep(random.randint(0, 1000) / 1000.0)  # 模拟用户操作


# 生成评论获取的 url
def make_url(max_id, mid):
    max_id_has_value = max_id is not None  # 是否包含 max_id
    max_id_str = ("&max_id=" + str(max_id) if max_id_has_value else "")  # 拼接参数
    url = "https://m.weibo.cn/comments/hotflow" \
          "?id=" + str(mid) + \
          "&mid=" + str(mid) + \
          "&max_id_type=0" + \
          max_id_str
    return url


# 获取评论的评论
def fetch_comments_of_comment(comment_id):
    allComment = []
    max_id = 0
    is_first_flag = True

    slow_down()
    while max_id != 0 | is_first_flag:
        slow_down()
        is_first_flag = False
        url = "https://m.weibo.cn/comments/hotFlowChild?" \
              "cid=%s&" \
              "max_id=%s&" \
              "max_id_type=0" % (str(comment_id), str(max_id))
        response = requests.get(url=url, cookies=cookie)
        content = json.loads(response.text)

        max_id = content['max_id']
        comments = content['data']
        allComment.extend(comments)

    return allComment


# 获取某条微博下的评论
def fetch_comments_of(mid):
    allComment = []
    mid = mid
    max_id = None
    current_page = 0  # 当前的页码
    has_more_comments = True

    while has_more_comments:
        time.sleep(1.2)

        url = make_url(max_id, mid)

        response = requests.get(url=url, cookies=cookie)
        rsp = json.loads(response.text)

        if rsp['ok'] == 0:
            continue

        data = rsp['data']

        # 获取该评论的基本信息
        max_id = data['max_id']  # max_id 分页
        comments = rsp['data']['data']  # 下级评论
        max = rsp['data']['max']  # 最大页数
        ok = rsp['ok']  # ok 码
        has_more_comments = current_page < max & ok == 1  # 是否有更多评论

        for c in comments:  # 遍历评论
            has_gt_2_pages = c['more_info_type'] == 1  # 该评论下是否有多于两条的评论
            blog_id = c['id']  # 获取该评论的id
            comment_id = c['bid']
            if has_gt_2_pages:
                slow_down()
                replays = fetch_comments_of_comment(blog_id)
                c['comments'] = []
                c['comments'] = replays

            replay_count = len(c['comments']) if c['comments'] != False else 0
            print("    微博评论Id: %s-%s, 下共有 %s 条评论" % (str(blog_id), comment_id, str(replay_count)))

        allComment.extend(comments)

        current_page += 1  # 页码自增

    return allComment


# 获取某条微博下的点赞用户
def fetch_like_user_of(blogId):
    currentPage = 0
    hasNextPage = True  # first page
    likedUsers = []

    while hasNextPage:
        slow_down()
        url = "https://m.weibo.cn/api/attitudes/show" \
              "?id=%s" \
              "&page=3" % (blogId)
        response = requests.get(url=url, cookies=cookie)
        data = json.loads(response.text)

        ok = data['ok']
        if ok != 1:
            break

        max = data['data']['max']
        liked = data['data']['data']  # 喜欢该微博的用户的信息、点赞的时间、以及该赞的id
        likedUsers.extend(liked)
        hasNextPage = currentPage < max

    return likedUsers


_id = files.read("property/blog.txt")
all_blog = table_chengshi.find({"_id": {"$gt": ObjectId(_id)}}) if (
        _id != "0") else table_chengshi.find().limit(20)

for blog in all_blog:
    print("当前微博Id:%s, Poster:%s" % (blog['mblog']['id'], blog['mblog']['user']['screen_name']))
    id = blog['_id']
    comments = fetch_comments_of(id)
    table_comment.insert_many(comments)
    files.save("property/blog.txt", id)

# fetch_comments_of(4324428303716828)

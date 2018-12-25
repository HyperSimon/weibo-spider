# coding=UTF-8

import json

import requests

import files


def fetch_cookie(username, password):
    url = "https://passport.weibo.cn/sso/login"

    data = {
        'username': (None, username),
        'password': (None, password),
    }

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

    response = requests.post(url=url, data=data, headers=headers)
    cookie = response.cookies.get_dict()
    files.save('cookie.txt', json.dumps(cookie))  # 存储cookie
    print "存储 cookie 到本地完成"
    return cookie


fetch_cookie("13048807364", "1236578simon")


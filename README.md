# PMACracker

phpmyadmin爆破工具

## 前言
原作者：https://github.com/TheKingOfDuck/PMACracker

phpmyadmin 先简称 pma, 太长了..

在此基础上改用Python3、增加了用户名字典、增加多线程功能、支持 pma 5.0.2 登录逻辑

尝试使用过支持批量导入url的神器，不过
+ 好像一旦发生网络原因就不会重试，直接瘫痪
+ pma 5.0.2 识别不了

然后暂时没有批量url的需求，因此有了这个fork


## 其他版本

pma 5.0.2 登录时去除了 post 登录表单后的 get 请求

见 [5.0.2分支](https://github.com/TARI0510/PMACracker/tree/5.0.2)


## 使用说明:

```bash
git clone https://github.com/TARI0510/PMACracker
cd PMACracker
# pma 5.0.2 版本 还需执行 `git checkout 5.0.2`
python3 fuckerbak.py
```

如果需要修改线程或者爆破延迟，可在 fuckerbak.py main里修改 threadNum 和 timeDelay 参数

相关依赖
```bash
python3 -m pip install requests
```

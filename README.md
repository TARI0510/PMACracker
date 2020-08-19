# PMACracker

phpmyadmin爆破工具

## 前言
原作者：https://github.com/TheKingOfDuck/PMACracker

在此基础上改用Python3、增加了用户名字典、增加多线程功能

尝试使用过支持批量导入url的神器，不过好像一旦发生网络原因就不会重试，直接断开

然后暂时没有批量url的需求，因此有了这个fork

使用说明: 
```bash
  git clone https://github.com/TARI0510/PMACracker
  cd PMACracker
  python3 fuckerbak.py
```

相关依赖
```bash
python3 -m pip install requests
```

to-do list
+ 让用户名初始化时也可以多线程


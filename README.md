# weibo_spider
graduate project, a weibo spider to find some interesting information such as "In social network , people tend to be happy or sad."

还是不用英语了。

这是我的项目介绍的地址:
http://wangshunping.github.io/%E9%A1%B9%E7%9B%AE/graduation-project/

### Update 2015.03.27
这是基于安医大近500个爬取的微博账号统计的结果。
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/mwRatio.png)
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/sex2totalcontent.png)
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/sex2zhuangfa.png)

## 东西还在持续更新中，欢迎fork 和 star。

### 联系
lionelwang93@163.com

## 用法

### 你需要安装的
1. python2.7     (是不是转到py3比较有big)
2. BeautifulSoup (超文本解析器)
3. requests      (http for human)
4. mysql         (...)

### 运行
1. 好啦，首先安装各种（安装遇到了问题可以邮件我）
2. 修改config.ini ,主要是连接数据库的参数，cookie，你要爬的学校和入口的用户id
3. 运行init.sql，建立数据库。
4. 运行 ``` python util.py ``` 来测试爬虫是否可以成功爬取，返回入口id的信息，并在数据库插入第一条信息
  如果成功了，会返回入口id的个人信息
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/success.png)

5. 运行 ```python NameListFactory.py``` 就可以欢乐的爬啦。

## 注意
1. 目前的线程为3，爬久了还是会封号。不过过几个小时会解封，解决策略是多申请几个号。

如果账号被暂时冻结， 那么会变成这个死样子...

![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/closeUser.png)


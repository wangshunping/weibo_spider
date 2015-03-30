# weibo_spider
graduate project, a weibo spider to find some interesting information such as "In social network , people tend to be happy or sad."

还是不用英语了。

Hi,我今年大四毕业，我猜你也是和我一个差不多大的少年。（如果是姑娘请联系我谢谢）

我不知道你是通过哪种渠道访问到了我的项目。如果你只是刚入门python或者根本不会，来吧，我们来撸一发，我们来玩些有趣的。

python 是一门非常简洁的语言，最重要的是，python的源码是可见的，它是真正的开源项目应该崇尚的语言。我在这个项目里面用到的爬虫，操作数据库，多线程，画图，统计或机器学习都是用python语言实现的。

如果你用python，你就不是一个人在战斗。

这个项目现在已经做到的程度是，下载源码，改动 config.ini 文件里面的学校名称，入口id, cookie，就可以画出你们学校的微博使用统计图统计图，我希望你把最后得到的图push给我，我希望帮助，或者和你一起完成前面的步骤（请先star我，我需要你的支持）；我希望通过我的源码，让你了解或者熟悉python，然后你再告诉我你有了一个什么碉堡了的想法，我来和你一起弄。

毕竟，

Talk is cheap, show me your code.

## 东西还在持续更新中，欢迎fork 和 star。

这是我的项目介绍的地址:
http://wangshunping.github.io/%E9%A1%B9%E7%9B%AE/graduation-project/

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

### Update 2015.03.27
这是基于安医大近500个爬取的微博账号统计的结果。
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/mwRatio.png)
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/sex2totalcontent.png)
![image](https://github.com/wangshunping/weibo_spider/raw/master/pic/sex2zhuangfa.png)

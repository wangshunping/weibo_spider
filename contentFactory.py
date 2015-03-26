# -*- coding:utf-8 -*-

import ConfigParser
import sys,re
from bs4 import BeautifulSoup as bs
from util import *
import time
import re
import threading
import Queue

homePage = 'http://weibo.cn/u/'
pageNum = '?page='

class contentFactory(threading.Thread):
    def __init__(self,queue):
        self.queue = queue
        threading.Thread.__init__(self)

        self.total = 0
        self.zhuangfa = 0
        self.end = False

        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        host = cf.get("db","host")
        port = int(cf.get("db","port"))
        user = cf.get("db","user")
        passwd = cf.get("db","passwd")
        db_name = cf.get("db","db")
        charset = cf.get("db","charset")
        use_unicode = cf.get("db","use_unicode")

        self.db = MySQLdb.connect(host=host, port=port, user=user,\
                                 passwd=passwd, db=db_name, \
                                  charset=charset,use_unicode=use_unicode)
        self.cursor = self.db.cursor()

    def run(self):
        while not self.queue.empty():
            t = self.queue.get()
            self.user_id = t[0]
            self.target = homePage + str(self.user_id)+pageNum
            for x in range(1,100):
                self.getTxt(self.target+str(x))
                if self.end:
                    self.end = False
                    break
            if self.total == 0:
                print "no weibo infomation... maybe some error in it"
                sys.exit(-3)

            sql = "UPDATE NAME SET CONTENT_VISIT= %s, CONTENT_TOTAL= %s, \
                CONTENT_ZHUANGFA= %s WHERE LINK_ID= %s"
            self.cursor.execute(sql,(1,self.total, self.zhuangfa, self.user_id))

            self.total = 0
            self.zhuangfa = 0
            print "finishend"

    def getTxt(self,url):
        time.sleep(5)
        content = get_content(url)
        soup = bs(content.text)
        weiboInfo = [x.get_text('|',strip=True).split('|')[0] for x in soup.find_all('div') if 'class' in x.attrs \
            if x.attrs['class'] == ['c']]

        for x in range(len(weiboInfo)-2):
            self.reZhuangfa(weiboInfo[x])
        print len(weiboInfo)
        if len(weiboInfo) == 2:
            self.end = True
        #print self.zhuangfa
        if len(weiboInfo) > 20:
            print "wocao... you bei fenghao la"
            sys.exit(5)

    def reZhuangfa(self,info):
        self.total += 1
        pattern = u'转发'
        pattern2 = u'［'
        pattern3 = u'＃'
        if re.match(pattern, info) == None:
        ## insert to database
            if re.match(pattern2, info) == None:
                if re.match(pattern3, info) == None:
                    sql = "INSERT IGNORE INTO CONTENT (LINK_ID, CONTENT) VALUES(%s, %s)"
                    self.cursor.execute(sql,(self.user_id,info))

        else:
            self.zhuangfa += 1


class updateContent(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        host = cf.get("db","host")
        port = int(cf.get("db","port"))
        user = cf.get("db","user")
        passwd = cf.get("db","passwd")
        db_name = cf.get("db","db")

        self.content_thread_amount = int(cf.get("content_thread_amount", \
                                               "content_thread_amount" ))
        try:
            self.db = MySQLdb.connect(host=host,port=port,user=user , \
                                      passwd=passwd, db=db_name)
            print "I have connect!"
        except:
            print "I can't connect to databases"
            sys.exit(-1)
        self.cursor = self.db.cursor()
    def run(self):
        queue = Queue.Queue()
        threads = []

        sql = "SELECT LINK_ID FROM MY_WEIBO_DATABASE.NAME where content_visit =0;"
        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        i=0

        for row in results:
            user_id = str(row[0])
            print user_id

            queue.put([user_id,i])
            i = i+1
        thread_amount = self.content_thread_amount

        for i in range(thread_amount):
            threads.append(contentFactory(queue))

        for i in range(thread_amount):
            threads[i].start()
            print str(threads[i]) + "begins"

        for i in range(thread_amount):
            threads[i].join()

        self.db.close()

        print 'All task done'



def main():
    app = updateContent()
    app.run()

if __name__ == '__main__':
    main()

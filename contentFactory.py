# -*- coding:utf-8 -*-

import ConfigParser
import sys,re
from bs4 import BeautifulSoup as bs
from util import *
import time
import re

homePage = 'http://weibo.cn/u/'
pageNum = '?page='

class contentFactory(object):
    def __init__(self,user_id):
        self.user_id = user_id
        self.target = homePage+str(self.user_id)+pageNum
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
        self.cursor.execute(sql,(0,self.total, self.zhuangfa, self.user_id))

        print "finishend"

    def getTxt(self,url):
        time.sleep(1)
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

    def reZhuangfa(self,info):
        self.total += 1
        pattern = u'转发'
        if re.match(pattern, info) == None:
            print info
            ## insert to database
            sql = "INSERT IGNORE INTO CONTENT (LINK_ID, CONTENT) VALUES(%s, %s)"
            self.cursor.execute(sql,(self.user_id,info))

        else:
            self.zhuangfa += 1


def main():
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")

    host = cf.get("db","host")
    port = int(cf.get("db","port"))
    user = cf.get("db","user")
    passwd = cf.get("db","passwd")
    db_name = cf.get("db","db")

    db = MySQLdb.connect(host=host, port=port, user=user,\
                              passwd=passwd, db=db_name )
    cursor = db.cursor()

    sql = "SELECT LINK_ID FROM MY_WEIBO_DATABASE.NAME where content_visit =0;"
    cursor.execute(sql)

    result = cursor.fetchall()
    link_id =[str(row[0]) for row in result]
    print link_id
    app = contentFactory(link_id[0])
    app.run()

if __name__ == '__main__':
    main()

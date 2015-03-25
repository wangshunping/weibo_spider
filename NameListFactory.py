# -*- coding:utf-8 -*-
'''
fans Url:       http://weibo.cn/1738181262/fans?page=2
follow Url:     https://weibo.cn/id/follow
infomation Url: https://weibo.cn/id/info

'''
from bs4 import BeautifulSoup as bs
from util import *
import sys,re
import ConfigParser
import MySQLdb
import threading
import Queue

class NameListFactory(threading.Thread):
    def __init__(self,queue):
        self.queue = queue
        threading.Thread.__init__(self)

        self.nameList = []
        self.tmpNameList = []
        self.homepage = 'http://weibo.cn/'
        self.fanspage = '/fans?page='
        self.infopage = '/info'

        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        self.school = cf.get("weibo","school").decode('utf-8')

        host = cf.get("db","host")
        port = int(cf.get("db","port"))
        user = cf.get("db","user")
        passwd = cf.get("db","passwd")
        db_name = cf.get("db","db")
        charset = cf.get("db","charset")
        use_unicode = cf.get("db","use_unicode")

        self.db = MySQLdb.connect(host=host,port=port,user=user, \
                                  passwd = passwd,db = db_name, \
                                  charset=charset,use_unicode=use_unicode)
        self.cursor = self.db.cursor()

    def run(self):
        while not self.queue.empty():
            t = self.queue.get()
            link_id = t[0]
            self.getMainNameList(link_id)
            for x in self.tmpNameList:
                try:
                    self.nameList = self.nameList + getUniversityStudent(x,self.school)
                except TypeError,e:
                    pass

            sql_str = "INSERT IGNORE INTO NAME (USERNAME, LAST_VISIT,LINK_ID, ADD_TIME,SEX,HOMETOWN) VALUES(%s, %s, %s, %s,%s,%s) "
            self.cursor.executemany(sql_str,self.nameList)

            time_now = int(time.time())
            sql = "UPDATE NAME SET LAST_VISIT = %s WHERE LINK_ID = %s "
            self.cursor.execute(sql,(time_now,link_id))

    def getMainNameList(self,inputid):
        self.tmpNameList = []
        inputUrl = self.homepage + inputid + self.fanspage
        for x in xrange(1,11):
            time.sleep(1)
            tmpUrl = inputUrl + str(x)
            print tmpUrl
            tmpContent = get_content(tmpUrl)
            soup = bs(tmpContent.text)
            listinfo = [link.get('href') for link in soup.find_all('a')\
                     if 'uid' in link.get('href')]
            self.tmpNameList.extend([reGetUid(x) for x in listinfo if reGetUid(x) is not None])
        self.tmpNameList = list(set(self.tmpNameList))

class updateNames(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        host = cf.get("db","host")
        port = int(cf.get("db","port") )
        user = cf.get("db","user")
        passwd = cf.get("db","passwd")
        db_name = cf.get("db","db")

        self.name_thread_amount = int(cf.get("name_thread_amount",\
                                           "name_thread_amount"))
        try:
            self.db = MySQLdb.connect(host=host,port=port,user=user,\
                                  passwd=passwd,db=db_name)
            print "I have connected~"
        except:
            print "I can't connect to database"
            sys.exit(-1)
        self.cursor = self.db.cursor()
    def run(self):
        queue = Queue.Queue()
        threads = []

        time_now = int(time.time())
        before_last_visit_time = time_now - 12*3600
        after_add_time = time_now - 24*3600*14

        sql = "SELECT LINK_ID FROM NAME WHERE LAST_VISIT < %s \
            AND ADD_TIME > %s \
            ORDER BY LAST_VISIT"
        self.cursor.execute(sql,(before_last_visit_time,after_add_time))
        results = self.cursor.fetchall()

        i = 0

        for row in results:
            link_id = str(row[0])
            print link_id

            queue.put([link_id,i])
            i = i+1
        thread_amount = self.name_thread_amount

        for i in range(thread_amount):
            threads.append(NameListFactory(queue))

        for i in range(thread_amount):
            threads[i].start()
            print str(threads[i]) + "begin~"

        for i in range(thread_amount):
            threads[i].join()



        self.db.close()

        print 'All task done'


def main():
    app = updateNames()
    app.run()

if __name__ == '__main__':
    main()

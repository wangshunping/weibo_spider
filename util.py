#-*- coding:utf-8 -*-
import requests
import gzip
import StringIO
import ConfigParser
import sys
from bs4 import BeautifulSoup
import time
import re
import MySQLdb

homePage = 'http://weibo.cn/'
infoPage = '/info'

def reGetUid(inputstr):
    import re
    patt = 'uid=([0-9]*)&rl'
    qwe = re.search(patt,inputstr)
    try:
        return qwe.group(1)
    except:
        return None

def get_content(toUrl):
    """ Return the content of given url

        Args:
            toUrl: aim url
            count: index of this connect

        Return:
            content if success
            'Fail' if fail
    """

    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    cookie = cf.get("cookie","cookie")
    cookdic = dict(Cookie=cookie)

    try:
        req = requests.get(toUrl,cookies = cookdic, timeout=100)
    except:
        return None
    if req.status_code != requests.codes.ok:
        print "haven't get 200, status_code is: "+str(req.status_code);
        sys.exit(-1)
    return req

def getUniversityStudent(inputid,school):
    time_now = int(time.time())
    inputUrl = homePage + inputid + infoPage
    tmpContent = get_content(inputUrl)
    soup = BeautifulSoup(tmpContent.text)
    time.sleep(1)
    divlabel = soup.find_all('div','tip')

    personalInfo = divlabel[0].next_sibling.get_text('|',strip=True)
    schoolInfo = divlabel[1].next_sibling.get_text()

    if school in schoolInfo:
        print personalInfo
        name,sex,hometown = impRe(personalInfo)
        return (name,0,inputid,time_now,sex,hometown)
    else:
        pass

def connectToDatabase(firstInfo):
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    host = cf.get("db","host")
    port = int(cf.get("db","port"))
    user = cf.get("db","user")
    passwd = cf.get("db","passwd")
    db_name = cf.get("db","db")
    charset = cf.get("db","charset")
    use_unicode = cf.get("db","use_unicode")
    try:
        db = MySQLdb.connect(host=host, port=port, user=user, \
                              passwd=passwd, db=db_name, \
                              charset=charset,use_unicode=use_unicode)
        cursor = db.cursor()
    except:
        print "Fail to connect to database"
        sys.exit(-1)
    print "connet to databse success ..."
    sql = "INSERT IGNORE INTO NAME (USERNAME,LAST_VISIT,LINK_ID,ADD_TIME,SEX,HOMETOWN) \
            VALUES(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, firstInfo)
    db.commit()
    print "insert first info to database success ..."

def impRe(target):
    print target,"......"
    pattern = u'昵称:([^\|]*)|'
    abc = re.match(pattern,target)
    name = abc.group(1)

    pattern = u'性别:([^\|])'
    abc = re.search(pattern,target)
    sex = abc.group(1)

    pattern = u'地区:([^\|]*)'
    abc = re.search(pattern,target)
    hometown = abc.group(1)

    return name,sex,hometown


def main():
    print "weibo spider test begin ~~"
    print "----------"
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    school = cf.get("weibo","school").decode('utf-8')
    mainid = cf.get("weibo","mainID")

    url = homePage + mainid
    content = get_content(url)
    firstInfo = getUniversityStudent(mainid, school)
    if firstInfo != None:
        print "weibo spider test pass"
    else:
        print "weibo spider test fail... "
        print "Cause func getUniveristyStudent return None "
        sys.exit(-2)
    print "----------"
    connectToDatabase(firstInfo)




if __name__ == "__main__":
    main()

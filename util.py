# -*- coding:utf-8 -*-

import requests
import gzip
import StringIO
import ConfigParser
import sys
from bs4 import BeautifulSoup

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

def processUrl(content):
    soup = BeautifulSoup(content)
    print soup.prettify()
    qwe = [link.get('href') for link in soup.find_all('a') if 'uid' in link.get('href')]
    print qwe

def reGetUid(inputstr):
    import re
    patt = 'uid=([0-9]*)&rl'
    qwe = re.search(patt,inputstr)
    try:
        return qwe.group(1)
    except:
        return None

def impRe(target):
    pattern = u'昵称:([^\|]*)|'
    abc = re.match(pattern,target)
    name = abc.group(1)

    pattern = u'性别:([^\|])'
    abc = re.search(pattern,target)
    sex = abc.group(1)

    pattern = u'地区:([^\|]*)'
    abc = re.search(pattern,target)
    hometown = abc.group(1)

    print name,sex,hometown


def main():
    url='http://weibo.cn/1738181262/follow?page=9'
    content = get_content(url)
    processUrl(content.text)
    #namestr = 'http://weibo.cn/attention/add? \
               #uid=3889609082&rl=1&st=d159be'
    #reGetUid(namestr)

if __name__ == "__main__":
    main()

# -*- coding:utf-8 -*-

'''
To get 昵称，性别，地区

'''
import re



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
    return name,sex,hometown

def main():
    target = u'昵称:卖芋头的小男孩|达人:体育 电影 宠物|性别:男|地区:江西 九江|生日:狮子座|感情状况：单身|简介:全年度有几多首歌 给天天的播|标签:|旅游|体育|狮子座|更多>>'
    impRe(target)

if __name__ == '__main__':
    main()

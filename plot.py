# -*- coding:utf-8 -*-

'''plot some pic using the data i scrapyed ~
    wdwdwd
'''

import MySQLdb
from ConfigParser import ConfigParser
import matplotlib.pyplot as plt
import re
from pylab import mpl
import numpy as np

class plotFactory(object):
    def __init__(self):
        cf = ConfigParser()
        cf.read("config.ini")

        host = cf.get("db", "host")
        port = int(cf.get("db", "port"))
        user = cf.get("db", "user")
        passwd = cf.get("db", "passwd")
        db_name = cf.get("db", "db")
        charset = cf.get("db", "charset")
        use_unicode = cf.get("db", "use_unicode")

        self.db = MySQLdb.connect(host=host, port=port, user=user,
                                  passwd=passwd, db=db_name,
                                  charset=charset, use_unicode=use_unicode)
        self.cursor = self.db.cursor()
        mpl.rcParams['font.sans-serif'] = ['SimHei']

    def run(self):
        self.getData()
        self.plotSexRatio()
        self.plotEffZhuRatio()
    def getData(self):
        sql = "SELECT SEX,CONTENT_TOTAL, CONTENT_ZHUANGFA FROM MY_WEIBO_DATABASE.NAME \
                WHERE CONTENT_VISIT = 1;"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.data = [[x, int(y), int(z)] for (x, y, z) in results]

    def plotSexRatio(self):
        sexlist = list(map(list,zip(*self.data)))[0]
        pattern = u'男'
        qwe = re.compile(pattern)
        self.men_label = [1 if qwe.match(x) != None else 0 for x in sexlist]
        men = sum(self.men_label)
        women = len(sexlist)  - men

        labels = u'男生人数:'+str(men),u'女生人数:'+str(women)
        sizes = [men,women]
        colors = ['yellowgreen','lightskyblue']
        explode = (0,0.1)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors \
                ,autopct='%1.1f%%',shadow=True,startangle=90)
        plt.axis('equal')
        plt.title(u'性别与用户数量')
        #plt.show()
        plt.savefig('pic/mwRatio.png')
        plt.close()

    def plotEffZhuRatio(self):
        self.total_men = [self.data[num][1]  for (num,x) in enumerate(self.men_label) if x ==1]
        self.zhuangfa_men = [self.data[num][2] for (num,x) in enumerate(self.men_label) if x==1]
        self.total_wo = [self.data[num][1] for (num,x) in enumerate(self.men_label) if x==0]
        self.zhuangfa_wo = [self.data[num][2] for (num,x) in enumerate(self.men_label) if x==0]


        self.plotTotal()
        self.plotZhuangfa()

    def plotTotal(self):
        ## begin to plot
        num_bins = 30
        M,m_bins = np.histogram(self.total_men, bins=num_bins)
        W,w_bins = np.histogram(self.total_wo,bins=num_bins)

        fig = plt.figure(figsize=(8,6),dpi=72, facecolor="white")
        axes = plt.subplot(111,axisbelow=True)

        plt.bar(m_bins[0:-1],+M,width=max(self.total_men)/num_bins,facecolor='#9999ff',edgecolor='white')
        for i,x in enumerate(m_bins[0:-1]):
            x += max(self.total_men)/num_bins/2
            y = M[i] + 0.3
            plt.text(x,y,M[i], color='#9999ff',size=9,\
                     horizontalalignment='center',verticalalignment='bottom')



        plt.bar(w_bins[0:-1],-W,width=max(self.total_wo)/num_bins,facecolor='#ff9999',edgecolor='white')
        for i,x in enumerate(w_bins[0:-1]):
            x += max(self.total_wo)/num_bins/2
            y = -W[i] - 3
            plt.text(x,y,W[i], color='#9999ff',size=9,\
                     horizontalalignment='center',verticalalignment='bottom')

        axes.set_xlim([0,1500])
        #axes.set_xticks([])
        axes.set_yticks([+30,-30])
        axes.set_yticklabels(['MAN','WOMAN'])

        labels = axes.get_yticklabels()
        labels[0].set_rotation(90)
        labels[0].set_color('#9999ff')
        labels[0].set_fontsize(25)
        labels[1].set_rotation(90)
        labels[1].set_color('#ff9999')
        labels[1].set_fontsize(25)

        axes.spines['top'].set_color('none')
        axes.spines['left'].set_color('none')
        axes.spines['right'].set_color('none')
        axes.spines['bottom'].set_color('none')

        axes.yaxis.set_ticks_position('left')

        plt.text(1500,60,u"安徽医科大学",color='black',size=36, \
                 horizontalalignment='right',verticalalignment='top')
        plt.text(1500,40 ,u'性别与微博数量的比较',color='.75',size=12,\
                 ha='right',va='top')
        plt.savefig('pic/sex2totalcontent.png')
        plt.close()


    def plotZhuangfa(self):
        ## begin to plot
        num_bins = 50
        M,m_bins = np.histogram(self.zhuangfa_men, bins=num_bins)
        W,w_bins = np.histogram(self.zhuangfa_wo,bins=num_bins)

        fig = plt.figure(figsize=(8,6),dpi=72, facecolor="white")
        axes = plt.subplot(111,axisbelow=True)

        plt.bar(m_bins[0:-1],+M,width=max(self.zhuangfa_men)/num_bins,facecolor='#9999ff',edgecolor='white')
        for i,x in enumerate(m_bins[0:-1]):
            x += max(self.zhuangfa_men)/num_bins/2
            y = M[i] + 0.3
            plt.text(x,y,M[i], color='#9999ff',size=9,\
                     horizontalalignment='center',verticalalignment='bottom')



        plt.bar(w_bins[0:-1],-W,width=max(self.zhuangfa_wo)/num_bins,facecolor='#ff9999',edgecolor='white')
        for i,x in enumerate(w_bins[0:-1]):
            x += max(self.zhuangfa_wo)/num_bins/2
            y = -W[i] - 3
            plt.text(x,y,W[i], color='#9999ff',size=9,\
                     horizontalalignment='center',verticalalignment='bottom')

        #axes.set_xlim([0,1200])
        #axes.set_xticks([])
        axes.set_yticks([+30,-30])
        axes.set_yticklabels(['MAN','WOMAN'])

        labels = axes.get_yticklabels()
        labels[0].set_rotation(90)
        labels[0].set_color('#9999ff')
        labels[0].set_fontsize(25)
        labels[1].set_rotation(90)
        labels[1].set_color('#ff9999')
        labels[1].set_fontsize(25)

        axes.spines['top'].set_color('none')
        axes.spines['left'].set_color('none')
        axes.spines['right'].set_color('none')
        axes.spines['bottom'].set_color('none')

        axes.yaxis.set_ticks_position('left')

        plt.text(1000,60,u"安徽医科大学",color='black',size=36, \
                 horizontalalignment='right',verticalalignment='top')
        plt.text(1000,40 ,u'性别与转发微博数量的比较',color='.75',size=12,\
                 ha='right',va='top')
        plt.savefig('pic/sex2zhuangfa.png')
        plt.close()

def main():
    app = plotFactory()
    app.run()

if __name__ == '__main__':
    main()

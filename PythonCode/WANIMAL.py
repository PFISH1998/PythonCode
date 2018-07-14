'''
爬虫程序爬取 WANIMAL Tumblr 的照片
'''


import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time
from requests import RequestException
import os

url = 'http://wanimal1983.org/page/'

data = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

def getContent(page):
    html = requests.get(url+str(page)).text
    s = requests.session()
    s.keep_alive = False
    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    data = soup.select('.photo-sets')
    return data


def getLink(items):
    print("")
    if items.p == None :
        lable = 'none'
    else:
        lable = items.p.string
    link = re.compile('.*?src="(.*?)".*?').findall(str(items))
    return (lable,link)


def downloadPic(pic):
    name = pic[0]
    picurl = pic[1]
    print(name,picurl)
    i=0
    for urls in picurl:
        i = i+1
        print('正在下载:{}'.format(urls))

        r = requests.get(urls,data,timeout=5)
        path = 'C:\\pic\\'+str(name+str(i))+'.jpg'
        with open(path,'wb') as f:
            f.write(r.content)
            print('保存成功')
            print('')
            time.sleep(3)


def saveData(pic):
    db = pymysql.connect(host='localhost',port=3306,user='root',passwd='pengyu',db='wanimal',charset='utf8')
    cursor = db.cursor()
    picurl = pic[1]
    name = pic[0]
    print(name,picurl)
    for url in picurl:
        if url == []:
            continue
        else:
            print(url)
            sql="INSERT INTO PICTURES (NAME,URLS) VALUES ('%s','%s')" % (name,url)
            cursor.execute(sql)
            db.commit()
    cursor.close()
    db.close()


def main():
    for page in range(100,120):#页码
        print('正在抓取第 {} 页'.format(page))
        for items in getContent(page):
            pic = getLink(items)
            # saveData(pic)
            downloadPic(pic)


if __name__ == '__main__':
    main()
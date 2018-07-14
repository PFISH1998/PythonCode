'''
爬取北京地铁每日客流量

'''



import requests as rq
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import xlwt
import time
import pymysql



url='https://www.bjsubway.com/support/cxyd/klxx/'

lasturl='https://www.bjsubway.com/support/cxyd/klxx/index_60.html'

data={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}


def getHtml(page):
    url = 'https://www.bjsubway.com/support/cxyd/klxx/'
    if page == 1:
        urls = url
    else:
        urls = url+str('index_')+str(page)+str('.html')
    try:
        print ('爬取第 {} 页数据'.format(page) )
        response=rq.get(urls,data)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
            result = soup.find_all('p')
        else:
            print('连接异常')
            return 1
        print(result)
        return result
    except RequestException :
        return 0


#
def getData(html):
    data = html.get_text()
    # 正则表达式得到日期与当日客流量
    item = re.compile('(.*?)（.*?客运量为(.*?)万人次.*?',re.S)
    day_data = re.findall(item,str(data))
    return day_data


# 存入 excel 表格
def writeData(items):
    i=0
    wb = xlwt.Workbook()
    ws = wb.add_sheet('data')
    headdata=('date','count')
    for n in range(2):
        ws.write(0,n,headdata[n],xlwt.easyxf('font: bold on'))
    print(len(items))
    # items=str(items)
    for ite in items:
        for item in ite:
            if item == []:
                continue
            else:
                i +=1
                print(i)
                date=re.compile("'(.*?)',").findall(str(item))[0]
                count=re.compile(", '(.*?)'").findall(str(item))[0]
                print(date)
                data=(date,count)
                for m in range(2):
                    ws.write(i,m,data[m])
                    wb.save('subway.xls')
    return i


# 存入数据库
def write_data_to_database(items):
    connect = pymysql.connect(
        host='localhost',port=3306,user='root',passwd='pengyu',db='subway',charset='utf8'
        )
    cursor = connect.cursor()
    for ite in items:
        for item in ite:
            if item == []:
                continue
            else:
                date=re.compile("'(.*?)',").findall(str(item))[0]
                count=re.compile(", '(.*?)'").findall(str(item))[0]
                print(date)
                print (count)
                sql="INSERT INTO SUBWAY (DATE,COUNT) VALUES ('%s',%d)" % \
                      (date,float(count))
                cursor.execute(sql)
                connect.commit()
    cursor.close()
    connect.close()




def main():
    data = []

    #设置爬取页码
    for page in range(4,65):
        time.sleep(5)
        for html in getHtml(page):
            Data = getData(html)
            print(Data)
            data.append(Data)
    return data


if __name__ == '__main__':
    items=main()
    write_data_to_database(items)


'''
爬虫获取拉勾网职位信息
'''

import requests
import json
import xlwt
import time


url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'

header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Referer':'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=sug&fromSearch=true&suginput=pachong'
        }

items = []
# pn=5
# kd='爬虫工程师'

def getContent(pn):
    data={'first':'true',
          'pn':pn,
          'kd':'python'}
    html=requests.post(url,data,headers=header).text
    print('正在爬取第 {} 页数据'.format(pn+1))
    return html

def getData(html):
    htmls=json.loads(html)
    for i in range(14):
        item = []
        item.append(htmls['content']['positionResult']['result'][i]['positionName'])
        item.append(htmls['content']['positionResult']['result'][i]['firstType'])
        item.append(htmls['content']['positionResult']['result'][i]['companyFullName'])
        item.append(htmls['content']['positionResult']['result'][i]['salary'])
        item.append(htmls['content']['positionResult']['result'][i]['city'])
        item.append(htmls['content']['positionResult']['result'][i]['workYear'])
        items.append(item)
    return items

def writeData(items):
    newtable='C:/weibo/items.xls'
    wb=xlwt.Workbook()
    ws=wb.add_sheet('test')
    headdata = ('职位','工作类型','公司','薪资','城市','工作经验')
    for i in range(6):
        ws.write(0,i,headdata[i],xlwt.easyxf('font: bold on'))

    index=1
    for item in items:
        for n in range(6):
            ws.write(index,n,item[n])
        index +=1
    wb.save(newtable)

def main():
    for pn in range(10):
        html = getContent(pn)
        items = getData(html)
        writeData(items)
        time.sleep(15)
    print('爬取结束！')


if __name__=='__main__':
    main()
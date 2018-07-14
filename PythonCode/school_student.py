'''
从学校官网爬取全校学生姓名学号
'''

import requests as rq
import xlwt
import re

i=0

url='bjryxxcx.aspx'


def getContent(num):

    data = {
        '__VIEWSTATE': '/wEPDwULLTE4NDU5NDgzNDlkZM5OMwrTbL+BAB5ITKltqeCct0vv',
        '__EVENTVALIDATION': '/wEWAwKay8+4BgK8uvvVDQKyk57DDSVjqko8qCLAZKTO3WIk4Ctf1iY8',
        'txtBjname': num,
        'btnchaxun': '查询'}
    try:
        html=rq.post(url,data=data).text
        finddata=re.compile('.*?<title>(.*?)</title>',re.S)
        compiledata=re.findall(finddata,html)
        if compiledata== ['\r\n\t错误页面提示\r\n']:
            print ('班级不存在')
            return None
        else:
            return html
    except:
        return None

def getData(html):
        info=re.compile('<span id="lblInformation">(.+?)</span>',re.S)
        data=re.findall(info,html)[0].split('</br>')[:-1]
        return data


def writeData(items):
    i=0
    wb = xlwt.Workbook()
    ws = wb.add_sheet('data')
    headdata=('stid','stname')
    for n in range(2):
        ws.write(0,n,headdata[n],xlwt.easyxf('font: bold on'))
    print(len(items))
    # items=str(items)
    for ite in items:
        for item in ite:
            i +=1
            print(i)
            stid=re.compile("(\d+)\s+\w+").findall(str(item))[0]
            stname=re.compile("\d+\s+(\w+)").findall(str(item))[0]
            print(stname)
            data=(stid,stname)
            for m in range(2):
                ws.write(i,m,data[m])
                wb.save('items2.xls')
    return i


def main():
    items=[]
    #生成班级
    for year in range(14, 18):
        #年级
        for dep in range(1, 8):
            #系别
            for n in range(1, 8):
                #专业
                for m in range(1, 7):
                    #班级
                    num = str(year) + str(50) + str(dep) + str(n) + str(m)
                    print(num)
                    html=getContent(num)
                    if html is None:
                        break
                    else:
                        data=getData(html)
                        items.append(data)
                        # items=saveData(data)

    return items


if __name__  ==  '__main__':
    items=main()
    print(items)
    writeData(items)
    items=writeData
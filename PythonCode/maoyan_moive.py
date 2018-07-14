import requests
from requests.exceptions import RequestException
import json
import re

header={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

url='http://maoyan.com/board/4?offset='

def getHtml(i):
    try:
        response=requests.get(url+str(i),headers=header)
        if response.status_code==200:
            html=response.text
            # print(html)
            return html
    except RequestException:
        return None


def getData(html):
    data=re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?data-src=.*?name"><a'
                    +'.*?">(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                    +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)

    items=re.findall(data,html)

    # print(items)

    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'start': item[2].strip()[3:],
            'time': item[3].strip()[5:],
            'integer': item[4]+item[5]
        }



def writeData(item):
    # for n in rang(10):
    #     item[n]
        with open('index.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(item,ensure_ascii=False)+'\n')
            f.close()


def main(i):
    html=getHtml(i)
    for item in getData(html):
        writeData(item)
    print('写入完成！')



if __name__ == '__main__':
    for i in range (1):
        print ('爬取第 {} 页数据'.format(i+1))
        main(i*10)
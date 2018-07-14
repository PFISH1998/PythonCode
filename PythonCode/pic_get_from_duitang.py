import requests
import urllib.parse
import json
import threading
import time


thread_lock=threading.BoundedSemaphore(value=10)

#'https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1feed&_type=&start=24'


def get_page(url):
    page = requests.get(url)
    page = page.content
    page = page.decode('utf-8')
    return page


def page_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=100'
    label = urllib.parse.quote(label)
    for index in range(0, 600, 100):
        u = url.format(label, index)
        print(u)
        page = get_page(u)
        pages.append(page)
    return pages


def pic_urls_from_pages(pages):
    pic_urls = []
    for page in pages:
        page_json = json.loads(page)
        object_json = page_json["data"]['object_list']
        for item in object_json:
            print(item)
            img_path = item["photo"]["path"]
            pic_urls.append(img_path)
    return pic_urls


def finall_in_page(page, startpart, endpart):
    all_string = []
    end = 0
    while page.find(startpart, end) != -1:
        start = page.find(startpart, end) + len(startpart)
        end = page.find(endpart, start)
        string = page[start: end]
        all_string.append(string)
    return all_string


def download_pics(url, n):
    r = requests.get(url)
    path = 'C:/pics/ab/'+str(n)+'.jpg'
    with open(path, 'wb')as f:
        f.write(r.content)
        print('正在下载第 {} 张图片'.format(n))



def main(label):
    pages = page_from_duitang(label)
    pic_urls = pic_urls_from_pages(pages)
    n = 0
    print(n)
    for url in pic_urls:
        n += 1
        download_pics(url,n)


main('刘亦菲')

# -*- coding: utf-8 -*-
import requests, re, os, jieba
from bs4 import BeautifulSoup


def getData(n):
    url = "http://zhushou.360.cn/list/index/cid/" + n
    page = requests.get(url)
    with open(n + '.html', 'w', encoding="utf8") as file:
        file.write(page.text)


def getDetail(url):
    page = requests.get("http://zhushou.360.cn" + url)
    soup = BeautifulSoup(page.text, 'html.parser')
    aa = soup.select("div .app-tags a")
    tags = [a.get_text() for a in aa]
    tags = "|".join(tags)
    desc = soup.select("div.breif")[0].get_text()
    desc1 = soup.select("div.breif")[0].select("table")[0].extract().get_text()
    desc = desc.replace(desc1, "")
    desc = desc.strip()
    desc = desc.replace('\n', "")
    desc = desc.replace('\r', '')
    return (tags, desc)


def parse(f):
    with open(f, "r", encoding="utf8")as file:
        text = file.read()
        soup = BeautifulSoup(text, 'html.parser')
        # print(soup.prettify())
        lis = soup.select("ul[class=iconList] li")
        print(len(lis))
        for li in lis:
            a = li.select("a")
            detail_href = a[1]["href"]
            name = a[1].get_text()
            href = a[2]["href"]
            cate = soup.select(".aurr")[0].get_text()
            package = ""
            detail = ("", "")
            matchObj = re.match(r'.*/(.*?)_\d+.apk', href)
            if matchObj:
                package = matchObj.group(1)
                detail = getDetail(detail_href)
            line = package + "~" + name + "~" + cate + "~" + detail[0] + "~" + detail[1]
            with open(cate + ".txt", "a", encoding="utf8")as f:
                f.write(line + "\n")


def parseAll():
    pathDir = os.listdir(".")
    for p in pathDir:
        if p.endswith('.html'):
            print(p)
            parse(p)


if __name__ == "__main__":
    # getData("11")
    # getData("12")
    # getData("14")
    # getData("15")
    # getData("16")
    # getData("17")
    # getData("18")
    # parseAll()
    pathDir = os.listdir(".")
    for p in pathDir:
        if p.endswith('.txt'):
            print(p)
            with open(p, 'r', encoding='utf8')as f:
                for line in f.readlines():
                    line_list = line.split('~')
                    seg_list = jieba.cut(line_list[4], cut_all=True)
                    seg = ','.join(seg_list)
                    seg = re.sub(',{1,}', ',',seg)
                    print(seg)
                    line_list[4]=seg
                    with open(p+'-jieba.txt','a',encoding='utf8')as f:
                        f.write('~'.join(line_list))

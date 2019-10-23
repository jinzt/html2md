#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

import os
import sys
import json
import getopt
import requests
import random
import re
import html2text
from bs4 import BeautifulSoup
import pdfkit

useragents = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    ]

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

def jinashu(url):
    print("---- jianshu")
    ## 浏览器头部
    headers = {
        'Host': 'www.jianshu.com',
        'Referer': 'https://www.jianshu.com/',
        'User-Agent': random.choice(useragents)
    }
    ## 获取网页主体
    html = requests.get(url,headers=headers).text

    ## bs4
    soup = BeautifulSoup(html,"html5lib")
    title = soup.find_all("title")[0].get_text()
    article = str(soup.find_all("div",class_="show-content")[0])

    ## 替图片的src加上https://方便访问
    article = re.sub('(src=")|(data-original-src=")','src="https:',article)

    ## 写入文件
    pwd = os.getcwd() # 获取当前的文件路径
    dirpath = pwd + '/jianshu/'
    write2md_and_pdf(dirpath,title,article)
    
    
def csdn(url):
    headers = {
        'Host': 'blog.csdn.net',
        'Referer': 'http://blog.csdn.net/',
        'User-Agent': random.choice(useragents)
    }
    ## 获取网页主体
    html = requests.get(url,headers=headers).text
    
    ## bs4
    soup = BeautifulSoup(html,'html5lib')
    title = soup.find_all('title')[0].get_text()
    article = str(soup.find_all('article')[0])

    ## 写入文件
    pwd = os.getcwd() # 获取当前的文件路径
    dirpath = pwd + '/CSDN/'
    write2md_and_pdf(dirpath,title,article)
   

def zhihu(url):
    headers = {
        'Host': 'zhuanlan.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': random.choice(useragents)
    }
    html = requests.get(url,headers=headers).text
    
    ## bs4
    soup = BeautifulSoup(html,'html5lib')
    title = soup.find_all('title')[0].get_text()
    article = str(soup.find_all('div',class_='Post-RichText')[0])

    ## 写入文件
    pwd = os.getcwd() # 获取当前的文件路径
    dirpath = pwd + '/ZhiHu/'
    write2md_and_pdf(dirpath,title,article)
    

def segmentfault(url):
    headers = {
        # 'Host': 'https://segmentfault.com',
        'Referer': 'https://segmentfault.com/',
        'User-Agent': random.choice(useragents)
    }
    html = requests.get(url,headers=headers).text
    
    ## bs4
    soup = BeautifulSoup(html,'html5lib')
    title = soup.find('title').text # 获取标题
    article = str(soup.find(class_='article__content'))
    ## 能够加载图片
    # article = re.sub('<p><span class="img-wrap">','',article)
    # article = re.sub('</span></p>','',article)
    article = re.sub('data-src="','src="https://segmentfault.com',article)
    print(article)
    # 写入文件
    pwd = os.getcwd() # 获取当前的文件路径
    dirpath = pwd + '/segmentfault/'
    write2md_and_pdf(dirpath,title,article)
    

def juejin(url):
    headers = {
        'Host': 'juejin.im',
        'Referer': 'https://juejin.im/',
        'User-Agent': random.choice(useragents)
    }
    res = requests.get(url=url,headers=headers).text # 获取整个html
    soup = BeautifulSoup(res,'html5lib')
    title = soup.find('title').text
    article = str(soup.find(class_='post-content-container'))
    ## 写入文件
    pwd = os.getcwd() # 获取当前的文件路径
    dirpath = pwd + '/segmentfault/'
    write2md_and_pdf(dirpath,title,article)
 
def gitchat(url):
    headers = {
        # 'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'Connection': 'keep-alive'
    }
    
    cookies = None
    with open('./static/gitchat_cookie.json', 'r') as f:      # 读取配置的cookie文件
        cookies = json.load(f)
    
    res = requests.get(url=url, cookies=cookies, headers=headers).text # 获取整个html
    soup = BeautifulSoup(res,'html5lib')
    title = soup.find('title').text
    #article = str(soup.find(class_='post-content-container'))
    article = str(soup.find(id='article_content'))
    #print(article)
    # img = "https://images.gitbook.cn/7634c020-9558-11e9-a6aa-5586d5604eb8"
    # res = requests.get(url=img, cookies=cookies, headers=headers).content  
    # f = open("data_md2.jpg", "wb")
    # f.write(res)
    # f.close()

    ## 写入文件
    pwd = os.getcwd() # 获取当前的文件路径
    dirpath = pwd + '/gitchat/'
    write2md_and_pdf(dirpath,title,article)     
 
def doelse(url):
    headers = {
        'User-Agent': random.choice(useragents)
    }
    res = requests.get(url=url ,headers=headers) # 获取整个html页面

    h = html2text.HTML2Text()
    h.ignore_links = False
    soup = BeautifulSoup(res.text,'html5lib')
    title = soup.title.text # 获取标题
    html = str(soup.body)
    article = h.handle(html)

    pwd = os.getcwd() # 获取当前文件的路径
    dirpath = pwd + '/Else/'
    if not os.path.exists(dirpath):# 判断目录是否存在，不存在则创建新的目录
        os.makedirs(dirpath)
    ## 写入文件
    write2md_and_pdf(dirpath,title,article)

"""
传入文件路径，title，article
"""
def write2md_and_pdf(dirpath,title,article):
    article = html_template.format(content=article)
    write2pdf(dirpath,title,article)
    write2md(dirpath,title,article)
 

"""
传入文件路径，title，article
"""
def write2md(dirpath,title,article):
    ## 创建转换器
    h2md = html2text.HTML2Text()
    h2md.ignore_links = False
    ## 转换文档
    article = h2md.handle(article)
    ## 写入文件
    if not os.path.exists(dirpath):# 判断目录是否存在，不存在则创建新的目录
        os.makedirs(dirpath)
    # 创建md文件
    with open(dirpath+title+'.md','w') as f:
    #with open(dirpath+title+'.md','w',encoding="utf8") as f:
        lines = article.splitlines()
        for line in lines:
            if line.endswith('-'):
                f.write(line)
            else:
                f.write(line+"\n")
    print(title+" md 下载完成....")

"""
传入文件路径，title，article
"""
def write2pdf(dirpath,title,article):
    ## 写入文件
    if not os.path.exists(dirpath):# 判断目录是否存在，不存在则创建新的目录
        os.makedirs(dirpath)

    pdfkit.from_string(article,dirpath + "out.pdf")
    if os.path.exists(dirpath + title + ".pdf"):
        os.remove(dirpath + title + ".pdf")
    os.rename(dirpath + "out.pdf",dirpath + title + ".pdf")
    print(title+" pdf 下载完成....")
    
def main(argv):
    try:
        opts,args = getopt.getopt(argv,"hf:",["url.txt"])
    except getopt.GetoptError:
        print("python html2md.py -f <url.txt>")
        sys.exit(2)
        
    print(opts)
    for opt,arg in opts:
        if opt == "-h":
            print("python html2md.py -u <url.txt>")
            sys.exit(2)
        elif opt in ("-f"):
            for line in open(arg):
                print(" http download", line)
                checkSite(line)
        else:
            print("python html2md.py -f <url.txt>")

## 检查网站，使用哪个下载器
def checkSite(url):
    if url.find('csdn') != -1:
        csdn(url)
    elif url.find('jianshu') != -1:
        jinashu(url)
    elif url.find('zhihu') != -1:
        zhihu(url)
    elif url.find('segmentfault') != -1:
        segmentfault(url)
    elif url.find('gitbook.cn') != -1:
        gitchat(url)           
    else:
        doelse(url)
    
    

if __name__ == "__main__":
    main(sys.argv[1:])
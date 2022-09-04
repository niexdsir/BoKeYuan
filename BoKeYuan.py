import re
import xmlrpc.client as xmlrpclib
from random import random, randint
from time import strftime

from bs4 import BeautifulSoup
import requests


#############FBI WARNING#############


#############修改 此处即可#############

serviceUrl, appkey = 'https://rpc.cnblogs.com/metaweblog/SirNie', 'SirNie'
usr, passwd = '如鯨向海', 'Aliez'

####################################


server = xmlrpclib.ServerProxy(serviceUrl)


# 在字符串指定位置插入字符
# str_origin：源字符串  pos：插入位置  str_add：待插入的字符串

def str_insert(str_origin, pos, str_add):
    str_list = list(str_origin)  # 字符串转list
    str_list.insert(pos, str_add)  # 在指定位置插入字符串
    str_out = ''.join(str_list)  # 空字符连接
    return str_out


def getContent():
    url = 'https://www.runoob.com/'

    url2s = ['vue2', 'html', 'css', 'js', 'htmldom', 'jquery', 'python3']
    for a in url2s:

        # 获取源码
        html = requests.get("https://www.runoob.com/" + a)
        # 打印源码
        soup = BeautifulSoup(html.text, 'lxml')
        list = soup.find_all(href=re.compile(a))
        urls = []
        for x in list:
            urls.append(str_insert(re.sub('\t|\n', '', str(x)), 9, url))
    return urls


def getBlogId():
    blogInfo = server.blogger.getUsersBlogs(appkey, usr, passwd)
    return blogInfo[0]['blogid']


def creatTitle():
    title = strftime('%m') + '月' + strftime('%d') + '日' + '总结'
    return title


def creatBlogContent():
    # 这一天干了啥 Done
    # 打算干啥 Will
    # 代码数 codeNum
    list = getContent()
    codeNum = randint(50, 500)
    donum = randint(0, len(list) - 1)

    return '今天干了啥：' + str(list[donum]) + '\n打算干啥：' + str(list[donum + 1]) + '代码数：' + str(codeNum)


def postBlog(BlogContent, title):
    #标签
    cate_list = ["[随笔分类]上传测试"]
    post = dict(dateCreate=strftime("%Y%m%dT%H:%M:%S"), description=BlogContent, title=title, categories=cate_list)
    server.metaWeblog.newPost(getBlogId(), usr, passwd, post, True)


if __name__ == "__main__":
    postBlog(creatBlogContent(), creatTitle())

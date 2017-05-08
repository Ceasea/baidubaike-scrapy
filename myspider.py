# coding:utf-8


"""
通过之前对网页的分析，在爬取时，我们需要以下几个模块
1.对页面上url进行管理，url管理器
2.对url管理器中的url进行爬取，并解析数据，html解析器
3.下载所需的内容，将其中的url传递给url管理器，内容传递给输出器，html下载器
4.将内容输出，html输出器
"""

# 实现爬取过程的类
import urllib2
import urlparse
import random
import time

import re
from bs4 import BeautifulSoup


class SpiderMain(object):
    # 主程序的各方法进行初始化
    def __init__(self):
        self.urls = manager()  # url管理器的下载方法
#        self.downloader = downloader()
        self.parser = parser()  # 解析器的解析方法
        self.outputer = outputer()  # 输出器的输出方法

    # 主程序的爬取方法
    # 以入口url开始
    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        count = 1
        """
        用url管理器中的has_new_url判断入口url及所有的url是否为空
        不为空则进行爬取
        """
        while self.urls.has_new_url():
            try:
                url = self.urls.get_new_url()
    #            print url
                url_cont = download(url)  # 下载url,得到内容url_cont对象
                new_urls, new_data = self.parser.parse(url, url_cont)  # 解析内容
                self.urls.add_new_urls(new_urls)  # 用url管理器的新增get_new_uls方法添加获得的urls
                self.outputer.collect_data(new_data)
                print 'craw %d : %s' % (count, url)

            except:
                print 'craw failed'

#            if count == 2:  # 爬取数量限制
#                break
            count = count + 1
            self.outputer.output()  # 输出数据
            time.sleep(random.random())


"""
url管理器收集所有url,爬取的，未爬取的，并传递下一个待爬取的url
1.新的url不为空
2.新旧url区分，已爬取的，未爬取有
"""


class manager(object):
    # 两个集合储存url
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    """
        出现两个add方法的原因：逻辑清晰
        第一个add实现对url的判断,决定是否添加
        第二个add实现批量添加,不在判断url的否为空或已爬取的url
    """

    # 添加单个url
    def add_new_url(self, url):
        # 为空则不添加
        if url is None:
            return
        # 不为空并判断url有没有被爬取，未被爬取则添加到new_urls中
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 添加多个url
    def add_new_urls(self, urls):
        if len(urls) == 0 or urls is None:
            return
        for url in urls:
            self.add_new_url(url)

    # 判断new_urls中是否有待爬取的url,有进行爬取
    def has_new_url(self):
        return len(self.new_urls) != 0

    # new_urls不为空, 取出一个url,并在new_url中删掉, 再添加到old_url中
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url


"""
url下载器
"""


def download(url):
    if url is None:
        return None
    send_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    req = urllib2.Request(url, headers=send_headers)
    response = urllib2.urlopen(req)

    if response.getcode() != 200:
        return None
    return response.read()


#class downloader(object):
#    pass


"""
url解析器,分别获得内容与新的url
"""


class parser(object):
    # get_url_data得到soup内的url

    def get_url_data(self, url, soup):
        new_urls = set()
        # 通过正则表达式匹配页面内的url
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link['href']
            # 匹配到的ulr只有一部分，用join方法将补全成完整url
            new_ful_url = urlparse.urljoin(url, new_url)
            new_urls.add(new_ful_url)
        return new_urls

    # get_cont_data得到soup内的内容
    def get_cont_data(self, url, soup):
        new_data = {}
        new_data['url'] = url
        # <dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        new_data['title'] = title_node.get_text()

        # <div class="lemma-summary">
        summary = soup.find('div', class_="lemma-summary")
        new_data['summary'] = summary.get_text()

        return new_data

    def parse(self, url, url_cont):
        if url is None or url_cont is None:
            return
        # 页面不为空则进行解析,解析得到的数据储存在soup中
        soup = BeautifulSoup(url_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self.get_url_data(url, soup)
        new_data = self.get_cont_data(url, soup)
        return new_urls, new_data


"""
url输出器
"""


class outputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output(self):
        id = 0
        fout = open('output.html', 'w')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")

        for data in self.datas:
            fout.write("<tr style='text-align:center;border:1px solid brown;'>")
#            fout.write("<td style='text-align:center;border:1px solid brown;'>%s</td>" % data['url'])
            fout.write("<td style='text-align:center;border:1px solid brown;'>%s</td>" % id)
            fout.write("<td style='text-align:center;border:1px solid brown;'>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td style='text-align:left;border:1px solid brown;'>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")
            id = id + 1




        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()


if __name__ == "__main__":
    root_url = "http://baike.baidu.com/item/Python"  # 入口url
    object_spider = SpiderMain()  # 建立一个爬取过程的对象
    object_spider.craw(root_url)  # 调用这个对象的craw方法进行爬取,这个方法，等会再实现

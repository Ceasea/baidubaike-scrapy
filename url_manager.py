# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 13:11:27 2017

@author: wjk
"""

class UrlManager(object):
    
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    # 1 如果抓取到的url为空则返回空，
    # 如果抓取到的url不在新、旧的url中，则增加到新urls表中
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.old_urls and url not in self.new_urls:
            self.new_urls.add(url)
        
    # 2 向url管理器添加批量url    
    def add_new_urls(self, urls):
        if urls in None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
        
     # 判断管理器中是否有新的url   
    def has_new_url(self):
        return len(self.new_urls) != 0
     
     # 从管理器中获得一个待爬取的url
    def get_new_url(self):
        # pop得到一个元素并删除
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
 
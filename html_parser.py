# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 13:12:06 2017

@author: wjk
"""

import re
import urlparse
from bs4 import BeautifulSoup


class HtmlParser(object):
    
    
    # 获得页面的url
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links =  soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link['href']
            new_ful_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_ful_url)
        return new_urls
        
     # 获得页面的数据   
    def _get_new_data(self, page_url, soup):
        res_data = {}
        
        #<dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title'] = title_node.get_text()
        
        #<div class="lemma-summary">
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()
        
        # url
        res_data['url'] = page_url
        
        return res_data

    
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='uft-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
 
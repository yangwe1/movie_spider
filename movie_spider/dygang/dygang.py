# coding=utf-8
__author__ = 'yw'
# import logging
import json
from pyquery import PyQuery
from requests import Session

from movie_spider.utils.retry import get_response


class MovieBay(object):
    def __init__(self, category, page=1):
        super(MovieBay, self).__init__()
        self.sess = Session()
        self.page = page
        self.category = category

    def get_list_url(self):
        list_url = []
        path_prefix = 'http://www.dygang.com/{}'.format(self.category)
        if self.page > 1:
            for page in range(self.page):
                list_url.append('{0}/index_{1}.htm'.format(path_prefix, page))
        list_url.append(path_prefix)
        return list_url

    def get_detail_url(self):
        detail_url = []
        for url in self.get_list_url():
            resp = get_response(url=url, sess=self.sess)
            if resp is not None:
                resp.encoding = 'gb2312'
                doc = PyQuery(resp.text)
                for each in doc("td[width='250']").items():
                    detail_url.append(each('a').attr.href)
        return detail_url

    def get_download_link(self):
        download_link = []
        for url in self.get_detail_url():
            resp = get_response(url=url, sess=self.sess)
            if resp is not None:
                resp.encoding = 'gb2312'
                doc = PyQuery(resp.text)
                for each in doc("table[bgcolor='#0099cc'] > tbody > tr").items():
                    if u'网盘' not in each.text() and each('a').attr.href is not None:
                        download_link.append(each('a').attr.href)
                        break
        return download_link

    def check_new_movie(self):
        new_links = []
        try:
            with open('{}.json'.format(self.category), 'r') as f:
                original_links = json.load(f)
        except IOError:
            with open('{}.json'.format(self.category), 'w') as f:
                json.dump(self.get_download_link(), f)
        else:
            now_links = self.get_download_link()
            for each in now_links:
                if each not in original_links:
                    new_links.append(each)
            with open('{}.json'.format(self.category), 'w') as f:
                json.dump(now_links, f, indent=2)
        return new_links


if __name__ == '__main__':
    m = MovieBay('1080p', 4)
    l = m.get_download_link()
    with open('1080p.json', 'w') as fd:
        json.dump(l, fd)
    for i in l:
        if 'magnet' not in i:
            print i

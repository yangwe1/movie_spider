# coding=utf-8
__author__ = 'yw'
import json
import re
import requests
from time import time
from urllib import unquote

reg = re.compile('window\.parent\._POST_CALLBACK_\d_\((.*?)\)')
reg_task_rtn = re.compile('\((.*?)\)')


class Thunder(object):
    def __init__(self, config):
        super(Thunder, self).__init__()
        self._conf = config
        self.sess = None
        self.json_callback_tail = None
        self.pid = None
        self.parent_callback_tail = 0

    def log_in(self):
        username = self._conf['username']
        password = self._conf['pwd']
        header_info = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': 1,
            'Host': 'yuancheng.xunlei.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'
        }
        self.sess = requests.Session()
        r = self.sess.get('http://yuancheng.xunlei.com/login.html', headers=header_info, timeout=10)
        r.raise_for_status()
        header_info_check = header_info.copy()
        del header_info_check['Upgrade-Insecure-Requests']
        del header_info_check['Cache-Control']
        header_info_check.update(
            {
                'Accept': 'image/webp,image/*,*/*;q=0.8',
                'Referer': 'http://i.xunlei.com/login/2.5/?r_d=1'
            }
        )
        payload = {
            'u': username,
            'business_type': 113,
            'cachetime': int(1000 * time())
        }
        header_info_post = header_info.copy()
        header_info_post.update(
            {
                'Host': 'login.xunlei.com',
                'Origin': 'http://i.xunlei.com',
                'Referer': 'http://i.xunlei.com/login/2.5/?r_d=1',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Upgrade-Insecure-Requests': 1
            }
        )
        resp = self.sess.get('https://login.xunlei.com/check/', headers=header_info_check, params=payload)
        cookie = resp.cookies.get_dict()
        # print cookie
        payload_local_js = {
            'kn': unquote(cookie['check_n']),
            'ke': cookie['check_e'],
            'captcha': cookie['check_result'][2:],
            'password': password
        }
        password_encrypted = requests.get(url='http://127.0.0.1:8888', params=payload_local_js, timeout=2)
        # print 'p', p_encrypted.content
        payload_post = {
            'p': password_encrypted.content,
            'u': username,
            'n': payload_local_js['kn'],
            'e': cookie['check_e'],
            'verifycode': payload_local_js['captcha'].upper(),
            'login_enable': 0,
            'business_type': 113,
            'v': 100,
            'cachetime': int(1000 * time())
        }
        logged_resp = self.sess.post('https://login.xunlei.com/sec2login/', headers=header_info_post, data=payload_post)
        header_info_last = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Referer': 'http://yuancheng.xunlei.com/login.html',
            'Connection': 'keep-alive',
            'DNT': 1,
            'Host': 'yuancheng.xunlei.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'
        }
        final_resp = self.sess.get(url='http://yuancheng.xunlei.com/', headers=header_info_last)

    def select_device(self):
        # checking if logged successfully here need to be rewrite
        if self.sess is not None:
            req_url = 'http://homecloud.yuancheng.xunlei.com/listPeer'
            header_info = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                'Connection': 'keep-alive',
                'DNT': 1,
                'Host': 'homecloud.yuancheng.xunlei.com',
                'Referer': 'http://yuancheng.xunlei.com/',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/45.0.2454.101 Safari/537.36'
            }
            self.json_callback_tail = int(1000 * time())
            payload = {
                'type': 0,
                'v': 2,
                'ct': 0,
                'callback': 'jQuery1720031343451933935285_{}'.format(self.json_callback_tail),
                '_': int(1000 * time())
            }
            resp = self.sess.get(url=req_url, headers=header_info, params=payload)
            device_info_str = resp.content.strip(payload['callback']).strip('(').strip(')')
            device_info_js = json.loads(device_info_str)
            # print device_info_str
            device_id = None
            for each_device in device_info_js['peerList']:
                if each_device['name'] == self._conf['device_name']:
                    device_id = each_device['pid']
            self.pid = device_id

    def create_task(self, url):
        if self.pid is not None:
            header_info = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'DNT': 1,
                'Host': 'homecloud.yuancheng.xunlei.com',
                'Origin': 'http://yuancheng.xunlei.com',
                'Referer': 'http://yuancheng.xunlei.com/',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/45.0.2454.101 Safari/537.36'
            }
            self.parent_callback_tail += 1
            urlparse_url = 'http://homecloud.yuancheng.xunlei.com/urlResolve' \
                           '?pid={0}&v=2&ct=0&' \
                           'callback=window.parent._POST_CALLBACK_{1}_'.format(self.pid, self.parent_callback_tail)
            payload = {
                'json': json.dumps({
                    'url': url
                })
            }
            urlparse_resp = self.sess.post(url=urlparse_url, data=payload)
            parse_result = json.loads(reg.findall(urlparse_resp.content)[0])
            # print parse_result
            file_name = parse_result['taskInfo']['name']
            url_in_next_submit = parse_result['taskInfo']['url']
            self.parent_callback_tail += 1
            create_url = 'http://homecloud.yuancheng.xunlei.com/createTask' \
                         '?pid={0}&v=2&ct=0&' \
                         'callback=window.parent._POST_CALLBACK_{1}_'.format(self.pid, self.parent_callback_tail)
            form_data = {
                'json': json.dumps({
                    "path": "C:/TDDOWNLOAD/",
                    "tasks": [{
                        "url": url_in_next_submit,
                        "name": file_name,
                        "gcid": "",
                        "cid": "",
                        "filesize": 0,
                        "ext_json": {
                            "autoname": 1
                        }
                    }
                    ]
                })
            }
            resp = self.sess.post(url=create_url, headers=header_info, data=form_data)
            move_file_name = json.loads(reg_task_rtn.findall(resp.content)[0])['tasks'][0][
                'name'] if reg_task_rtn.findall(resp.content) else 'Unknown'


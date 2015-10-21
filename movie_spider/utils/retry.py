# coding=utf-8

__author__ = 'yw'
from requests import request, Session
from requests.exceptions import ConnectionError, Timeout


def get_response(url, **kwargs):
    header_info = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/44.0.2403.157 Safari/537.36'
    }
    if 'retries' in kwargs:
        retries = kwargs.pop('retries')
        kwargs['headers'] = header_info
    else:
        retries = 3
    if 'sess' in kwargs:
        sess = kwargs.pop('sess')
    else:
        sess = Session()
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 10
    response = None
    try:
        response = sess.get(url, **kwargs)
    except Timeout, e:
        if retries > 0:
            kwargs['retries'] = retries - 1
            kwargs['sess'] = sess
            response = get_response(**kwargs)
        else:
            print e
    except ConnectionError, e:
        print e
    return response


def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += 1

        return wrapper

    return decorator

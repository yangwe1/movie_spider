# coding=utf-8
__author__ = 'yw'
import json
import traceback
from time import sleep

from movie_spider.dygang.dygang import MovieBay
from movie_spider.remote_dl.thunder import Thunder

movie = MovieBay('ys')
while True:
    try:
        new_movie = movie.check_new_movie()
    except:
        traceback.print_exc()
        sleep(60)
        continue
    if len(new_movie) == 0:
        sleep(3600)
        continue
    with open('config.json') as fd:
        config = json.load(fd)
    thunder = Thunder(config)
    try:
        thunder.log_in()
        thunder.select_device()
    except:
        traceback.print_exc()
    else:
        for i in new_movie:
            if 'magnet' not in i:
                thunder.create_task(i)
                sleep(1)
    sleep(3600)

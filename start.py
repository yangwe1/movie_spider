# coding=utf-8
__author__ = 'yw'
import json
import traceback
import time

from movie_spider.dygang.dygang import MovieBay
from movie_spider.remote_dl.thunder import Thunder
from movie_spider.utils.time_schedule import schedule

with open('config.json') as fd:
    config = json.load(fd)
interval = 3600 * config['interval']
movie = MovieBay(**config['moviebay'])
while True:
    schedule(config['start_time'], config['stop_time'])
    try:
        new_movie = movie.check_new_movie()
    except:
        traceback.print_exc()
        time.sleep(60)
        continue
    if len(new_movie) == 0:
        print "new movie NOT found, scanning will be restart in 1 hour."
        time.sleep(interval)
        continue
    thunder = Thunder(config['thunder'])
    try:
        thunder.log_in()
        thunder.select_device()
    except:
        traceback.print_exc()
    else:
        for i in new_movie:
            if 'magnet' not in i:
                thunder.create_task(i)
                print "new movie added:", i
                time.sleep(1)
    print "mission completed. scanning will be restart in %s hour." % config['interval']
    time.sleep(interval)

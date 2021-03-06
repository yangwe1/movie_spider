# coding=utf-8

__author__ = 'yw'

import logging
import logging.handlers
import json
import traceback
import time
from movie_spider.dygang.dygang import MovieBay
from movie_spider.remote_dl.thunder import Thunder
from movie_spider.utils.time_schedule import schedule
from movie_spider.utils.retry import retry
from movie_spider.utils.send_mail import SendMail

LOG_FILE = 'movie_spider.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
log = logging.getLogger(__file__)
log.addHandler(handler)
log.setLevel(logging.INFO)


@retry(3)
def add_movie(thunder_conf, movies):
    success = []
    if isinstance(movies, list):
        thunder = Thunder(thunder_conf)
        try:
            thunder.log_in()
            thunder.select_device()
        except Exception, e:
            traceback.print_exc()
            log.error(e, exc_info=True)
            raise e
        else:
            for i in movies:
                if 'magnet' not in i:
                    movie_name = thunder.create_task(i)
                    log.info("new movie added: %s" % i)
                    success.append(movie_name)
                    time.sleep(1)
    return success


if __name__ == '__main__':
    with open('config.json') as fd:
        config = json.load(fd)
    interval = 3600 * config['interval']
    movie = MovieBay(**config['moviebay'])
    while True:
        schedule(**config['time_schedule'])
        try:
            new_movie = movie.check_new_movie()
        except:
            traceback.print_exc()
            time.sleep(60)
            continue
        if len(new_movie) == 0:
            log.info("new movie NOT found, scanning will be restart in 1 hour.")
            time.sleep(interval)
            continue
        result = add_movie(config['thunder'], new_movie)
        try:
            mail = SendMail(config['mail'])
            mail.send_mail(','.join(result))
            log.info('mail sent successfully.')
            del mail
        except:
            log.error('ERROR at mailing..', exc_info=True)
        log.info("mission completed. scanning will be restart in %s hour." % config['interval'])
        time.sleep(interval)

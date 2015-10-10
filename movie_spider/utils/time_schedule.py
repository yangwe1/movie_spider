__author__ = 'yw'
# coding=utf-8
import time


def schedule(start, stop):
    start_h, start_m = start.split(':')
    stop_h, stop_m = stop.split(':')
    while True:
        current_h, current_m = time.strftime('%H:%M', time.localtime()).split(':')
        if int(start_h) < int(current_h) < int(stop_h):
            break
        elif int(current_h) == int(start_h) and int(current_m) > int(start_m):
            break
        elif int(current_h) == int(stop_h) and int(current_m) < int(stop_m):
            break
        else:
            time.sleep(3600)

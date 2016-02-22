#! /usr/bin/env python

'''
    Log when Internet connection is ONLINE or OFFLINE

'''

import logging
from os.path import isfile
import requests

log = logging.getLogger('uptime.py')
log.setLevel(logging.INFO)
fh = logging.FileHandler('online.log')
fh.setLevel(logging.INFO)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        "%Y/%m/%d %H:%M:%S")
fh.setFormatter(frmt)
log.addHandler(fh)

host_url = 'http://google.com'
my_stat = 'status'

if not isfile(my_stat):
    log.info("Status file created")
    with open(my_stat, 'w') as f:
        f.write('NEW')

try:
    response = requests.get(host_url).status_code
    cur_stat = 'ONLINE'
except requests.exceptions.ConnectionError:
    cur_stat = 'OFFLINE'

with open(my_stat, 'r') as old_stat:
    up_stat = old_stat.read()
    if cur_stat != up_stat:
        log.info("Status CHANGED: %s", cur_stat)
        with open(my_stat, 'w') as ch_stat:
            ch_stat.write(cur_stat)

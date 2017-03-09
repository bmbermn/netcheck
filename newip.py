#! /usr/bin/env python


import logging
from os.path import isfile
import requests
from socket import gethostname
import yaml

with open('config.yml') as f:
    config = yaml.load(f)
tg_api_url = 'https://api.telegram.org/bot'
tg_api_token = config['Bots']['<username>']['token']
tg_api_method = 'sendMessage'
tg_api_bot_url = tg_api_url + tg_api_token + '/' + tg_api_method
tg_chat_id = config['Bots']['<username>']['chat_id']

log = logging.getLogger('newip.py')
log.setLevel(logging.INFO)
fh = logging.FileHandler(config['Logging']['logfile'])
fh.setLevel(logging.INFO)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        "%Y/%m/%d %H:%M:%S")
fh.setFormatter(frmt)
log.addHandler(fh)


my_host = gethostname()
ip_file = config.['Logging']['ip_file']

try:
    ip_url = 'https://api.ipify.org'
    my_ip = requests.get(ip_url, timeout=5).content.strip()
except requests.exceptions.ConnectionError:
    my_ip = 'CONNECTION TIMEOUT'

def payload(type):
    if type == 'new':
        status = 'New IP'
    elif type == 'set':
        status = 'Set IP'

    text_msg = ("*HOST STATUS*\nHost: %s\nStatus: %s\nIP: %s"
                % (my_host, status, my_ip))

    msg_data = {'chat_id': tg_chat_id,
                'text': text_msg,
                'parse_mode': 'Markdown'}

    return msg_data


if isfile(ip_file):
    with open(ip_file) as old_ip:
        cur_ip = old_ip.read()
        if cur_ip == my_ip:
            log.info("IP has not updated -- %s", my_ip)
        elif my_ip == 'CONNECTION TIMEOUT':
            log.warn("IP has not updated -- %s", my_ip)
        else:
            log.info("IP address CHANGED -- %s", my_ip)
            with open(ip_file, 'w') as new_ip:
                new_ip.write(my_ip)
                requests.get(tg_api_bot_url, data=payload('new'))
else:
    with open(ip_file, 'w') as save_ip:
        save_ip.write(my_ip)
    log.info("IP address established -- %s", my_ip)
    requests.get(tg_api_bot_url, data=payload('set'))

#! /usr/bin/env python


import logging
import netifaces
from os.path import isfile
import requests
from socket import gethostname
import yaml

with open('config.yml') as fr:
    config = yaml.load(fr)

log = logging.getLogger('newip.py')
log.setLevel(logging.INFO)
fh = logging.FileHandler(config['Logging']['logfile'])
fh.setLevel(logging.INFO)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        "%Y/%m/%d %H:%M:%S")
fh.setFormatter(frmt)
log.addHandler(fh)

ip_url = 'https://api.ipify.org'
tg_api_url = 'https://api.telegram.org/bot'
tg_api_token = config['Bots']['botname']['token']
tg_api_method = 'sendMessage'
tg_api_bot_url = tg_api_url + tg_api_token + '/' + tg_api_method
tg_chat_id = config['Bots']['botname']['chat_id']

my_host = gethostname()
wan_ip = config['Host']['wan_ip']
lan_ip = config['Host']['lan_ip']

def set_lan_ip():
    for iface in netifaces.interfaces():
        try:
            if iface != 'lo':
                host_ip = netifaces.ifaddresses(iface)[2][0]['addr']
                global lan_ip
                if lan_ip != host_ip and host_ip != '':
                    config['Host']['lan_ip'] = host_ip
                    lan_ip = host_ip
                    return lan_ip
        except KeyError:
            pass


def payload(type):
    if type == 'new':
        status = 'New IP'
    elif type == 'set':
        status = 'Set IP'

    text_msg = ("*HOST STATUS*\nHost: %s\nStatus: %s\nIP: %s\nLAN: %s"
                % (my_host, status, wan_ip, lan_ip))

    msg_data = {'chat_id': tg_chat_id,
                'text': text_msg,
                'parse_mode': 'Markdown'}

    return msg_data


if config['Host']['hostname'] == '':
    config['Host']['hostname'] = my_host

try:
    my_ip = requests.get(ip_url, timeout=5).content.strip()
except requests.exceptions.ConnectionError:
    my_ip = 'CONNECTION TIMEOUT'


with open('config.yml', 'w+') as fw:
    if wan_ip == '':
        config['Host']['wan_ip'] = my_ip
        wan_ip = my_ip
        set_lan_ip()
        log.info("IP address established -- %s", my_ip)
        fw.write(yaml.dump(config, default_flow_style=False))
        requests.get(tg_api_bot_url, params=payload('set'))
    elif wan_ip == my_ip:
        set_lan_ip()
        log.info("IP has not updated -- %s", my_ip)
        fw.write(yaml.dump(config, default_flow_style=False))
    elif my_ip == 'CONNECTION TIMEOUT':
        set_lan_ip()
        log.warn("IP has not updated -- %s", my_ip)
        fw.write(yaml.dump(config, default_flow_style=False))
    elif wan_ip != my_ip:
        config['Host']['wan_ip'] = my_ip
        wan_ip = my_ip
        set_lan_ip()
        log.info("IP address CHANGED -- %s", my_ip)
        fw.write(yaml.dump(config, default_flow_style=False))
        requests.get(tg_api_bot_url, params=payload('new'))


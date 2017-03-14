#! /usr/bin/env python


from datetime import datetime
import logging
import requests
from socket import gethostname
import sys
import yaml

rebooted = False

try:
    if sys.argv[1] == 'reboot':
        rebooted = True
except IndexError:
    pass

now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

with open('config.yml') as fr:
    config = yaml.load(fr)

log = logging.getLogger('uptime.py')
log.setLevel(logging.INFO)
fh = logging.FileHandler(config['Logging']['logfile'])
fh.setLevel(logging.INFO)
frmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                         "%Y/%m/%d %H:%M:%S")
fh.setFormatter(frmt)
log.addHandler(fh)

tg_api_url = 'http://api.telegram.org/bot'
tg_api_token = config['Bots']['botname']['token']
tg_api_method = 'sendMessage'
tg_api_bot_url = tg_api_url + tg_api_token + '/' + tg_api_method
tg_chat_id = config['Bots']['botname']['chat_id']

my_host = gethostname()
log_check = config['Online']['check']
log_latest = config['Online']['latest']
log_status = config['Online']['status']

check_url = 'https://google.com'

try:
    response = requests.get(check_url).status_code
    if response == 200:
        online_status = 'Online'
    else:
        online_status = 'Offline'
except requests.exceptions.ConnectionError:
    online_status = 'Offline'


def notify_telegram_bot(status, latest, check):
    text_msg = ("*HOST UPTIME*\nHost: %s\nStatus: %s\nLatest: %s\nCheck: %s"
                % (my_host, status, latest, check))

    msg_data = {'chat_id': tg_chat_id,
                'text': text_msg,
                'parse_mode': 'Markdown'}

    requests.get(tg_api_bot_url, params=msg_data)


with open('config.yml', 'w+') as fw:
    if rebooted and online_status == 'Online':
        log.info("Status CHANGED: Reboot")
        notify_telegram_bot('Reboot', log_latest, now)
        config['Online']['check'] = now
        config['Online']['latest'] = now
        config['Online']['status'] = 'Online'
        fw.write(yaml.dump(config, default_flow_style=False))
    elif rebooted and online_status == 'Offline':
        log.warn("Status CHANGED: Reboot")
        config['Online']['check'] = now
        config['Online']['status'] = 'Offline'
        fw.write(yaml.dump(config, default_flow_style=False))
    elif log_status == 'Online' and online_status == 'Online':
        log.info("Status remains: Online")
        config['Online']['check'] = now
        config['Online']['latest'] = now
        fw.write(yaml.dump(config, default_flow_style=False))
    elif log_status == 'Online' and online_status == 'Offline':
        log.warn("Status CHANGED: Offline")
        config['Online']['check'] = now
        config['Online']['status'] = 'Offline'
        fw.write(yaml.dump(config, default_flow_style=False))
    elif log_status == 'Offline' and online_status == 'Online':
        log.info("Status CHANGED: Online")
        notify_telegram_bot('Online', log_latest, now)
        config['Online']['check'] = now
        config['Online']['latest'] = now
        config['Online']['status'] = 'Online'
        fw.write(yaml.dump(config, default_flow_style=False))
    elif log_status == 'Offline' and online_status == 'Offline':
        log.warn("Status remains: Offline")
        config['Online']['check'] = now
        fw.write(yaml.dump(config, default_flow_style=False))

#! /usr/bin/env python

'''
    Requires the installation of the Twilio Python library.

        pip install twilio

    The config module can be downloaded here:

        https://www.red-dove.com/config-doc/#download
'''

from config import Config
import logging
from os.path import isfile
from socket import gethostname
from twilio.rest import TwilioRestClient
import requests

CONF = file('config.cfg')
cfg = Config(CONF)

log = logging.getLogger('newip.py')
log.setLevel(logging.INFO)
fh = logging.FileHandler('online.log')
fh.setLevel(logging.INFO)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        "%Y/%m/%d %H:%M:%S")
fh.setFormatter(frmt)
log.addHandler(fh)

ip_url = 'https://api.ipify.org'
mobile_ph = cfg.mobile_phone
twilio_ph = cfg.twilio_phone
account_sid = cfg.twilio_account_sid
auth_token = cfg.twilio_auth_token
client = TwilioRestClient(account_sid, auth_token)

my_host = gethostname()
ip_file = 'ip'

try:
    my_ip = requests.get(ip_url, timeout=5).content.strip()
except requests.exceptions.ConnectionError:
    my_ip = 'CONNECTION TIMEOUT'
    exit(1)

if isfile(ip_file):
    with open(ip_file, 'r') as old_ip:
        cur_ip = old_ip.read()
        if cur_ip != my_ip:
            log.info("IP address CHANGED -- %s", my_ip)
            with open(ip_file, 'w') as new_ip:
                new_ip.write(my_ip)
            sms = client.messages.create(to=mobile_ph,
                                        from_=twilio_ph,
                                        body="New IP: "+my_host+": "+my_ip)
else:
    with open(ip_file, 'w') as save_ip:
        save_ip.write(my_ip)
    log.info("IP address established -- %s", my_ip)
    sms = client.messages.create(to=mobile_ph,
                                from_=twilio_ph,
                                body="Set IP: "+my_host+": "+my_ip)

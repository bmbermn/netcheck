#! /usr/bin/env python

'''
    Requires the installation of the Twilio Python library.

        pip install twilio

    Pushbullet can be installed with pip

        pip install pushbullet.py
'''

import config
import logging
from os.path import isfile
from socket import gethostname
import requests

ip_url = 'https://api.ipify.org'
ip_file = 'ip'
my_host = gethostname()
account_sid = config.twilio['account_sid']
auth_token = config.twilio['auth_token']
mobile_ph = config.twilio['mobile_phone']
twilio_ph = config.twilio['twilio_phone']
pb_api_key = config.pushbullet['access_token']

## Pushbullet notifications
def pb_push(msg):
    try:
        from pushbullet import Pushbullet
    except ImportError:
        print "Install pushbullet.py library"
        exit(2)

    if pb_api_key != 0000:
        pb = Pushbullet(pb_api_key)
        push = pb.push_note(my_host, msg)

## Twilio SMS
def twilio_sms(host, ip):
    try:
        from twilio.rest import TwilioRestClient
    except ImportError:
        print "Install twilio library"
        exit(3)

    client = TwilioRestClient(account_sid, auth_token)
    sms = client.messages.create(to = mobile_ph,
                                from_ = twilio_ph,
                                body = "Set IP: %s: %s" % (host, ip))

## Logging
log = logging.getLogger('newip.py')
log.setLevel(logging.INFO)
fh = logging.FileHandler('online.log')
fh.setLevel(logging.INFO)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        "%Y/%m/%d %H:%M:%S")
fh.setFormatter(frmt)
log.addHandler(fh)

## Get the IP
try:
    my_ip = requests.get(ip_url, timeout=5).content.strip()
except requests.exceptions.ConnectionError:
    my_ip = 'CONNECTION TIMEOUT'
    exit(1)

## IP check, logging, and notifications
if isfile(ip_file):
    with open(ip_file, 'r') as old_ip:
        cur_ip = old_ip.read()
        if cur_ip != my_ip:
            with open(ip_file, 'w') as new_ip:
                new_ip.write(my_ip)
            status_msg = "IP address CHANGED -- %s" % my_ip
            log.info(status_msg)
            pb_push(status_msg)
            twilio_sms(my_host, my_ip)
else:
    with open(ip_file, 'w') as save_ip:
        save_ip.write(my_ip)
    status_msg = "IP address established -- %s" % my_ip
    log.info(status_msg)
    pb_push(status_msg)
    twilio_sms(my_host, my_ip)

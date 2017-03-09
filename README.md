# netcheck
Rename 'config.yml-sample' to 'config.yml', and add your details.

This uses the Telegram platform to send notifications.
https://telegram.org

In addition to a free sign-up, you'll need to create a bot.
Use the botfather for assistance.
https://core.telegram.org/bots

Required modules (pip install):
* logging
* netifaces
* requests
* yaml


## newip.py
If ISP changes your IP, this sends a Pushbullet notitication or Twilio SMS.

Push notification and SMS contains the hostname and new IP.

Logging happens, regardless of Pushbullet or Twilio account.

## uptime.py
Checks for your online status, and logs it.

If status changes, ONLINE<=>OFFLINE, it gets logged, with a time stamp.

Can't send a notification when offline, obviously, but can notify when online.

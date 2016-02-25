# netcheck
Rename 'config.py-sample' to 'config.py', and add your details.

Send SMS via Twilio, and push notification via Pushbullet.

Twilio: https://www.twilio.com/

`$ pip install twilio`

Pushbullet: https://www.pushbullet.com/

`$ pip install pushbullet.py`

## newip.py
If ISP changes your IP, this sends a Pushbullet notitication or Twilio SMS.

SMS and notification contains the hostname, and new IP.

Logging happens, regardless of Pushbullet or Twilio account.

## uptime.py
Checks for your online status, and logs it.

If status changes, ONLINE<=>OFFLINE, it gets logged, with a time stamp.

Can't send a notification when offline, obviously, but can notify when online.

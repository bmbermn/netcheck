# netcheck
Rename 'config.py-sample' to 'config.py', and add your details.

Can SMS via Twilio, and send push notifications via Pushbullet.

Twilio: https://www.twilio.com/

pip install twilio

Pushbullet: https://www.pushbullet.com/

pip install pushbullet.py


# newip.py
When ISP changes your IP, this can send a Twilio SMS, or Pushbullet notitication

to advise on the new IP address.

# uptime.py
Checks for your online status, and logs it.

If status changes, ONLINE<=>OFFLINE, it gets logged, with a time stamp.

Can't send a notification when offline, obviously, but can notify when online.

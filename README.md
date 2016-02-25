# netcheck
Rename 'config.py-sample' to 'config.py', and add your details.

<<<<<<< HEAD
Set "enable = 1" to use the corresponding service.

Send push notification via Pushbullet, and SMS via Twilio.
=======
Send SMS via Twilio, and push notification via Pushbullet.

Twilio: https://www.twilio.com/

`$ pip install twilio`
>>>>>>> ce5c6a66758c243eae5025458bd069436820c8cf

Pushbullet: https://www.pushbullet.com/

`$ pip install pushbullet.py`
<<<<<<< HEAD

Twilio: https://www.twilio.com/

`$ pip install twilio`
=======
>>>>>>> ce5c6a66758c243eae5025458bd069436820c8cf

## newip.py
If ISP changes your IP, this sends a Pushbullet notitication or Twilio SMS.

<<<<<<< HEAD
Push notification and SMS contains the hostname and new IP.
=======
SMS and notification contains the hostname, and new IP.
>>>>>>> ce5c6a66758c243eae5025458bd069436820c8cf

Logging happens, regardless of Pushbullet or Twilio account.

## uptime.py
Checks for your online status, and logs it.

If status changes, ONLINE<=>OFFLINE, it gets logged, with a time stamp.

Can't send a notification when offline, obviously, but can notify when online.

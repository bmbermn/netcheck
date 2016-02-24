# netcheck
Rename 'config.cfg-sample' to 'config.cfg', and add your Twilio details.
'config.cfg' file only needed for newip.py.

# newip.py
Needs Twilio and config module.
Twilio module can be installed via pip.
Download the config module here: https://www.red-dove.com/config-doc/#download

# uptime.py
Checks for your online status, and logs it.
If status changes, ONLINE<=>OFFLINE, it gets logged, with a time stamp.
Helpful to determine when ISP issues happen overnight.

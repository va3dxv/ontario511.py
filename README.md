# ontario511.py
Parses road reports from 511.on.ca json and converts text to u-law audio for Asterisk/app_rpt

01/01/2019

Brian Graves - VA3DXV

va3dxv@gmail.com

https://github.com/va3dxv

This script requires access to http://api.voicerss.org (it's free)
as well as lame and sox to create the .ul file for asterisk
(sudo apt-get install lame && sudo apt-get install sox)

Run this file from roots crontab to create the audio file every hour (sudo crontab -e)

0 */1 * * * /usr/local/sbin/ontario511.py >/dev/null 2>&1

Add this to your /etc/asterisk/rpt.conf under [functions]
where 85 is the DTMF * command you want to use and where 99999 is your node number

85=cmd,asterisk -rx "rpt localplay 99999 /etc/asterisk/custom/ontario511"

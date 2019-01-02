#!/usr/bin/python
#
# ontario511.py
#
# 01/01/2019
#
# Brian Graves - VA3DXV
#
# va3dxv@gmail.com
#
# https://github.com/va3dxv
#
# This script requires access to http://api.voicerss.org (it's free)
# as well as lame and sox to create the .ul file for asterisk
#
# Run this file from roots crontab to create the audio file every hour
# 0 */1 * * * /usr/local/sbin/ontario511.py >/dev/null 2>&1
#
# Add this to /etc/asterisk/rpt.conf under [functions]
# 85=cmd,asterisk -rx "rpt localplay 99999 /etc/asterisk/custom/ontario511"
#
# (where 99999 is your node number)
#
#################################
import requests
import subprocess
import shlex
import os
#
# configuration
#
# set your voicerss API key here
voicersskey = "someapikeygoeshere"
# set your desired voice language here
voicersslang = "en-us"
# set speed of speech here
voicerssspeed = "-1"
# set format of initial audio before converting to ulaw
voicerssformat = "44khz_16bit_mono"
#
# end configuration
#
roadreports = requests.get(
    "https://511on.ca/api/v2/get/roadconditions"
).json()
textfile = open("/tmp/ontario511.txt", "w")
textfile.write("Current highway conditions..\r\n")
for items in roadreports:
    area = (items["AreaName"])
    location = (items["LocationDescription"] .split("|")[0])
    condition = (items["Condition"])
    roadname = (items["RoadwayName"])
    vis = (items["Visibility"])
# this if statement defines areas and roads you want. The whole list is huge, don't do it!
    if (area == "Eastern" and roadname == "417" or roadname == "416"):
        if ("Quebec" in location or "Arnprior" in location and roadname == "417"):
            continue
        textfile.write("..Highway %s %s. %s. Visibility is %s. \r\n" %
                       (roadname, location, condition[0], vis))
textfile.write("End of report.")
textfile.close()
ontario511 = open("/tmp/ontario511.txt", "r")
getmp3 = requests.get("http://api.voicerss.org/",
                      data={"key": voicersskey, "r": voicerssspeed,
                            "src": ontario511, "hl": voicersslang, "f": voicerssformat}
                      )
ontario511.close()
mp3file = open("/tmp/ontario511.mp3", "wb")
mp3file.write(getmp3.content)
mp3file.close()
# convert to wav with lame (apt-get install lame) then to ulaw with sox (apt-get install sox)
subprocess.call(shlex.split("lame --decode /tmp/ontario511.mp3 /tmp/ontario511.wav"))
subprocess.call(shlex.split("sox -V /tmp/ontario511.wav -r 8000 -c 1 -t ul /etc/asterisk/custom/ontario511.ul"))
# cleanup
subprocess.call(shlex.split("rm -f /tmp/ontario511.txt"))
subprocess.call(shlex.split("rm -f /tmp/ontario511.mp3"))
subprocess.call(shlex.split("rm -f /tmp/ontario511.wav"))
#################################
# output sample (depends on if statement):
#
# Current highway conditions..
# ..Highway 416 From Highway 401 to Fallowfield Road. Bare and dry road. Visibility is Good.
# ..Highway 417 From Highway 138 to Gloucester. Bare and dry road. Visibility is Good.
# ..Highway 417 From Gloucester to Fitzroy. Bare and dry road. Visibility is Good.
# ..Highway 416 From Fallowfield Road to Highway 417. Bare and dry road. Visibility is Good.
# End of report.
#
#EOF

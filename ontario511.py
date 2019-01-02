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
#
# configuration
#
# set your voicerss API key here
voicersskey = "yourvoicerssapikeygoeshere"
# set your desired voice language here
voicersslang = "en-us"
# set speed of speech here
voicerssspeed = "-1"
# set format of initial audio before converting to ulaw
voicerssformat = "44khz_16bit_mono"
#
# end configuration
#
temppath = "/tmp/"
aslpath = "/etc/asterisk/custom/"
scriptname = "ontario511"
aslfile = aslpath + "ontario511"
filetxt = temppath + scriptname + ".txt"
filemp3 = temppath + scriptname + ".mp3"
filewav = temppath + scriptname + ".wav"
fileul = aslfile + ".ul"

roadreports = requests.get(
    "https://511on.ca/api/v2/get/roadconditions"
).json()
textfile = open(filetxt, "w")
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
ontario511 = open(filetxt, "r")
getmp3 = requests.get("http://api.voicerss.org/",
                      data={"key": voicersskey, "r": voicerssspeed,
                            "src": ontario511, "hl": voicersslang, "f": voicerssformat}
                      )
ontario511.close()
mp3file = open(filemp3, "wb")
mp3file.write(getmp3.content)
mp3file.close()
# convert to wav with lame (apt-get install lame) then to ulaw with sox (apt-get install sox)
subprocess.call(shlex.split("lame --decode " + filemp3 + " " + filewav))
subprocess.call(shlex.split("sox -V " + filewav + " -r 8000 -c 1 -t ul " + fileul))
# cleanup
subprocess.call(shlex.split("rm -f " + filetxt))
subprocess.call(shlex.split("rm -f " + filemp3))
subprocess.call(shlex.split("rm -f " + filewav))
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

#!/usr/bin/python3.5
#
# ontario511.py
#
# 15/12/2018
#
# Brian Graves - VA3DXV
#
# va3dxv@gmail.com
#
#####################################################################################################
import requests
import subprocess
import shlex

roadreports = requests.get (
        "https://511on.ca/api/v2/get/roadconditions"
).json()


file=open("/tmp/ontario511.txt","+w")

file.write("Current highway conditions..\r\n")
for items in roadreports:
        area = (items["AreaName"])
        location = (items["LocationDescription"] .split("|")[0])
        condition = (items["Condition"])
        roadname = (items["RoadwayName"])
        vis = (items["Visibility"])
        if (area == "Eastern" and roadname == "417" or roadname == "138" or roadname == "416"):
            if ("Quebec" in location or "Arnprior" in location): continue
            file.write("..Highway %s %s. %s. Visibility is %s. \r\n" % (roadname,location,condition[0],vis))
file.write("End of report.\r\n")
file.close()

subprocess.call(shlex.split("/usr/local/sbin/tts_audio.sh /tmp/ontario511.txt"))
subprocess.call(shlex.split("rm -f /tmp/ontario511.txt"))
subprocess.call(shlex.split("mv /tmp/ontario511.ul /etc/asterisk/custom"))


#####################################################################################################
#
# output:
#
# Current highway conditions..
# Highway 138 From Cornwall to Highway 417 . Bare and dry road . visibility is Good ..
# Highway 416 From Highway 401 to Fallowfield Road . Bare and dry road . visibility is Good ..
# Highway 417 From Highway 138 to Gloucester . Bare and dry road . visibility is Good ..
# Highway 417 From Gloucester to Fitzroy . Bare and dry road . visibility is Good ..
# Highway 416 From Fallowfield Road to Highway 417 . Bare and dry road . visibility is Good ..
# End of report.
#
#EOF

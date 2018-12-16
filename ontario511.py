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
# To Do:
# 1) Integrate voicerss.org API for text to speech
#
#####################################################################################################
import requests

roadreports = requests.get (
        "https://511on.ca/api/v2/get/roadconditions"
).json()

for items in roadreports:
        area = (items["AreaName"])
        location = (items["LocationDescription"] .split("|")[0])
        condition = (items["Condition"])
        roadname = (items["RoadwayName"])
        vis = (items["Visibility"])
        if (area == "Eastern" and roadname == "417" or roadname == "138" or roadname == "416"):
            if ("Quebec" in location or "Arnprior" in location): continue
            print("..Highway %s %s. %s. Visibility is %s." % (roadname,location,condition[0],vis))
        
#####################################################################################################
# output
# Highway 138 From Cornwall to Highway 417 . Bare and dry road . visibility is Good ..
# Highway 416 From Highway 401 to Fallowfield Road . Bare and dry road . visibility is Good ..
# Highway 417 From Highway 138 to Gloucester . Bare and dry road . visibility is Good ..
# Highway 417 From Gloucester to Fitzroy . Bare and dry road . visibility is Good ..
# Highway 416 From Fallowfield Road to Highway 417 . Bare and dry road . visibility is Good ..
#
#EOF

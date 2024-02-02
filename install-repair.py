# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2

# Quick repair tool for PterodactylRun


import os
import sys
import time
import requests

from platform import system as OS

if OS == "Windows":
    cl = "cls"
else:
    cl = "clear"

moduleList = [
    "os",
    "sys",
    "time",
    "json",
    "pygame",
    "random",
    "platform",
    "requests",
    "threading",
    "configparser"
]

urlDict = {
    "ini": "https://github.com/Kieferrrrr/PterodactylRun/resources/etc/config.ini",
    "json": "https://github.com/Kieferrrrr/PterodactylRun/resources/etc/scores.json"
}

# nothing here anymore
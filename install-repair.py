# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2

# Quick repair tool for PterodactylRun


import os
import sys
import time
import requests
import configparser

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

class IR:

    def menu():
        print(" [1] Install Modules")
        print(" [2] Repair Utility Files\n")
        choice = int(input(" >> "))
        if choice == 1:
            IR.install()
        elif choice == 2:
            IR.repair()
        else:
            print(" Invalid Option")
            time.sleep(2)
            os.system(cl)
            IR.menu()

    def install():
        for i in moduleList:
            os.system(f"pip install {i}")
        print("\n All required modules should be installed\n    Run 'py PterodactylRun.py'")

    def repair():
        print

IR.menu()
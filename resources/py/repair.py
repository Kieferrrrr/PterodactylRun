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


class repair:

    def main():
        os.system(cl)
        print(" PterodactylRun - Repair")
        print("\n [1] Install Missing Resources\n [2] Repair config.ini\n [3] Repair scores.jsonc\n [4] Exit\n")

        choice = int(input(" >> "))

        if choice == 1:
            print("\n Installing all modules with pip\n")
            for i in moduleList:
                os.system(f"pip install {i}")
            print("\n All modules should now be installed")
            time.sleep(2)
            repair.main()

        elif choice == 2:
            print("\n Repairing config.ini\n")
            try:
                iniContents = requests.get(urlDict["ini"])
            except:
                print("\n Cannot connect to GitHub\n    Are you connected to the internet?")
                time.sleep(2)
                repair.main()
            try:
                os.remove("resources/config.ini")
            except:
                pass
            file = open("resources/config.ini", "a")
            file.write(iniContents.text)
            file.close()
            print("\n Repaired config.ini\n")
            time.sleep(2)
            repair.main()

        elif choice == 3:
            print("\n Repairing scores.jsonc\n")
            try:
                jsonContents = requests.get(urlDict["json"])
            except:
                print("\n Cannot connect to GitHub\n    Are you connected to the internet?")
                time.sleep(2)
                repair.main()
            try:
                os.remove("resources/scores/scores.jsonc")
            except:
                pass
            file = open("resources/scores/scores.jsonc", "a")
            file.write(jsonContents.text)
            file.close()
            print("\n Repaired scores.jsonc\n")
            time.sleep(2)
            repair.main()

        elif choice == 4:
            sys.exit()


        else:
            print(" Invalid Choice\n    Restarting")
            time.sleep(2)
            repair.main()


try:
    repair.main()
except KeyboardInterrupt:
    print(" CTRL+C Pressed\n    Exiting...")
    time.sleep(2)
    sys.exit(" bye :)")
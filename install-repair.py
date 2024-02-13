# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2

# Quick repair tool for PterodactylRun
# Build Version 1.5.1

import os   # These 3 modules are used
import sys  # within this file, they
import time # should come with Python 3

# Newest versions of these modules at the time of development
moduleList = [
    "pygame==2.5.2", # Python game engine 
    "requests==2.31.0", # Used to rebuild utility files 
    "configparser==6.0.0" # Used to retrieve values in resoruces/etc/config.ini
]

urlDict = {
    "ini": "https://raw.githubusercontent.com/Kieferrrrr/PterodactylRun/main/resources/etc/config.ini",
    "json": "https://raw.githubusercontent.com/Kieferrrrr/PterodactylRun/main/resources/etc/scores.json"
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
            print(" Invalid Option\n")
            time.sleep(2)
            IR.menu()

    def install():
        print("\n Consult the README.md file for minimum required module versions\n if installing modules does not fix module requirement issue\n")
        time.sleep(3)
        for i in moduleList:
            os.system(f"pip install {i}")
        print("\n All required modules should be installed\n    Run 'py PterodactylRun.py'")

    def repair():
        import requests
        print("\n  [1] Repair config.ini")
        print(" [2] Repair score.json\n")
        rChoice = int(input(" >> "))
        if rChoice == 1:
            iniContent = requests.get(urlDict["ini"])
            try:
                os.remove("resources/etc/config.ini")
            except:
                pass
            iniFile = open("resources/etc/config.ini")
            iniFile.write(iniContent.text())
            iniFile.close()
            print("\n Rebuilt conifg.ini File")
            time.sleep(2)
            sys.exit()
        elif rChoice == 2:
            jsonContent = requests.get(urlDict["json"])
            try:
                os.remove("resources/etc/scores.json")
            except:
                pass
            jsonFile = open("resources/etc/scores.json")
            jsonFile.write(jsonContent.text())
            jsonFile.close()
            print("\n Rebuilt scores.json File")
            time.sleep(2)
            sys.exit()
        else:
            print(" Invalid Option\n")
            time.sleep(2)
            IR.repair()

IR.menu()

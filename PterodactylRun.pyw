# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2
# Submission 1

# Main Game File for PterodactylRun
# Build Version 1.6.0

import os
import sys
import json
import random
import pygame # Needs installing
import configparser # Needs installing

from time import sleep
from datetime import datetime

# Dictionary of basic/common errors
errs = {
    1: " CTRL+C pressed", # Keyboard interrupt pressed in the terminal
    2: " Cannot import PterodactylRun.pyw as a module", # PterodactylRun.pyw is not a module
    3: " Error reading config.ini\n     using default settings\n     run install-repair.py to fix", # config.ini could not be found/used
    4: " Error reading scores.json\n     not loading or saving high scores\n     run install-repair.py to fix", # scores.json could not be found/used
    5: " Unable detect your operating system\n     please create an issue on GitHub with the myOS tag", # Your OS was not recognised
    6: " A value in config.ini is not useable\n    using default settings", # A value in config.ini is not in the correct format
    7: " Failed to save high score\n    run install-repair.py to fix" # scores.json is missing
}

if sys.platform == "win32": # Windows
    cl = "cls"
    os.system("mode 80,20 && title PterodactlyRun - Version 1.6.0 - CLI") # .pyw should hide the terminal but if its ran in the CLI its there
    detOS = "Windows"
elif sys.platform == "linux" or sys.platform == "linux2": # Linux
    cl = "clear"
    detOS = "Linux"
elif sys.platform == "darwin": # MacOS
    cl = "clear"
    detOS = "MacOS"
else:
    print(errs[5])
    detOS = "Unreocgnised"

print(" PterodactylRun Build Version 1.6.0 Debug Output")
print(f" Detected host system - {detOS}")

vw = 700 # Screen view width
vh = 350 # Screen view height

ptDir = f"{os.path.dirname(os.path.realpath(__file__))}/"
ptDir = ptDir.replace("\\", "/")

pygame.init()
screenCTRL = pygame.display.set_mode((vw, vh))
clock = pygame.time.Clock()

# Class for getting and setting variables in /resources/etc
class dataHandler:
    def __init__(self):
        # Default config.ini settings incase of file error
        self.startSpeed = 3
        self.fps = 60
        self.saveHigh = True
        self.saveDir = f"{ptDir}resources/etc/scores.json"
        self.saveDebug = False
        self.debugDir = None # Just to avoid errors
        self.invincible = False
        # Default score.json settings incase of file errors
        self.highscore = "00000"

    def getINI(self):
        try:
            conf = configparser.ConfigParser()
            conf.read(f"{ptDir}resources/etc/config.ini")
            try:
                # General configurations for the game
                self.startSpeed = conf["CONFIG"]["startSpeed"]
                self.fps = conf["CONFIG"]["fps"]
                self.saveHigh = conf["CONFIG"]["saveHigh"]
                self.saveDir = conf["CONFIG"]["saveDir"]
                # Configurations to aid debugging
                self.saveDebug = conf["DEBUG"]["saveDebug"]
                self.debugDir = conf["DEBUG"]["debugDir"]
                # Cheat options
                self.invincible = conf["CHEAT"]["invincible"]
            except:
                main.errMsgGeneric(errs[6])
        except:
            main.errMsgGeneric(errs[3])

    def getJSON(self):
        try:
            with open(self.saveDir, "r") as jsonFile:
                jsonData = json.loads(jsonFile.read())
                self.highscore = jsonData["highscore"]
        except:
            main.errMsgGeneric(errs[4])

    def setJSON(self, score):
        try:
            with open(self.saveDir, "r") as jsonFile:
                jsonData = {"highscore": "{:05d}".format(score)}
                jsonFile.seek(0)
                json.dump(jsonData, jsonFile, indent=4)
                jsonFile.truncate() 
                print(f" New highscore saved to scores.json ({score})")
        except:
            main.errMsgGeneric(errs[7])

    def setTXT(self, output):
        with open(self.debugDir, "a") as txtFile:
            txtFile.write(f"{output}\n")


# Class for functions and variables related to the pterodactyl
class pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.flyingImg = pygame.image.load(f"{ptDir}resources/img/pterodactylA.png")
        self.fallingImg = pygame.image.load(f"{ptDir}resources/img/pterodactylB.png")
        # Image handling
        self.playerImg = self.fallingImg
        self.playerRect = self.playerImg.get_rect()
        self.playerRect.center = (vw // 4, vh // 2)
        # Integers
        self.gravity = 0.2
        self.flySpeed = 5
        self.Yspeed = 0
        # Menu animation
        self.gravityOn = False
        self.playerTimer = datetime.now().timestamp()

    def update(self):
        print

    def flap(self):
        print


# Class for the main game loop
class main(object):
    def __init__(self):
        # Instances of classes
        self.dataParsing = dataHandler()
        self.player = pterodactyl()
        self.cactiCTRL = cacti()
        self.trexCTRL = trex()
        # Data fetching
        self.dataParsing.getINI()
        self.dataParsing.getJSON()
        # Assets
        self.bgImg = pygame.image.load(f"{ptDir}resources/img/700x175.png")
        self.trexIco = pygame.image.load(f"{ptDir}resources/img/trexSmall.png")
        self.textBig = pygame.font.Font(f"{ptDir}resources/etc/GameOver.ttf", 75)
        self.textSmall = pygame.font.Font(f"{ptDir}resources/etc/GameOver.ttf", 48)
        # Integers
        self.level = 1
        self.levelScore = 0
        self.score = 00000
        self.kills = 00000
        self.img1X = -350
        self.img2X = 350
        self.imgY = 275
        self.scrollSpeed = self.dataParsing.startSpeed

    # Main game loop function
    def play(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_SPACE and self.player.playerRect.y > 0:
                        self.player.flap()
                        self.player.gravityOn = True
                        break
            # Create UI elements
            leftTxt = self.textSmall.render("x{:05d}".format(self.kills).ljust(12) + f"Level {self.level}", True, "#454545")
            middleTxt = self.textBig.render("PterodactylRun", True, "#454545")
            rightTxt = self.textSmall.render("Score {:05d}".format(self.score).ljust(16) + f"High {self.highscore}", True, "#454545")
            # Scroll the floor
            self.img1X = self.img1X - self.scrollSpeed # Scroll image one
            self.img2X = self.img2X - self.scrollSpeed # Scroll image two
            # Show world assets
            screenCTRL.blit(255, 255, 255) # Paint the sky white
            screenCTRL.blit(self.bgImg, (self.img1X, self.imgY)) # Show floor image one
            screenCTRL.blit(self.bgImg, (self.img2X, self.imgY)) # Show floor image two            
            # Show UI text elements
            self.screenCTRL.blit(leftTxt, (60, 12)) # Show t-rex counter and level
            self.screenCTRL.blit(middleTxt, (vw / 3, 0)) # Show pterodactylRun Title
            self.screenCTRL.blit(rightTxt, (vw - 250, 12)) # Show score and highscore
            self.screenCTRL.blit(self.trexIco, (10, 2.5)) # Show t-rex kill counter icon
            # Reload scrolling animation
            if self.img1X <= -700:
                self.img1X = 700
            if self.img2X <= -700:
                self.img2X = 700
            # Start game screen
            if self.player.gravityOn == False:
                txtG = self.textBig.render("Press [SPACE] to Start", True, "#454545")
                self.screenCTRL.blit(txtG, (vw / 3.6, 50))

    # Killing the pterodactyl and breaking the main loop
    def die(self):
        self.running = False
        if int(self.score) > int(self.highscore):
            self.dataParsing.setJSON(self.score)
            restart = self.textBig.render("Game Over Press [SPACE] to Restart", True, "#454545")
            while True:
                screenCTRL.blit(restart, (vw / 6, 50))

    # Broad spectrum error handler for fixable errors
    def errMsgGeneric(self, err):
        print(err)

    # Error handling for fatal errors
    def errMsgFatal(self, err):
        print


# Class for functions and variables related to the cacti
class cacti():
    def __init__(self):
        # Assets
        self.cactusImgA = pygame.image.load(f"{ptDir}resources/img/cactusImgA.png")
        self.cactusImgB = pygame.image.load(f"{ptDir}resources/img/cactusImgB.png")
        self.cactiImgs = [self.cactusImgA, self.cactusImgB]
        # Integers
        self.rndX = None
        # Nested dictionary of rendered cacti variables
        self.cactiVars = {
            1: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False},
            2: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False},
            3: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False},
            4: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False}
        }
        # Queue of previously generated cacti X co-ordinates
        self.cactiPrevious = []
        
    def spawner(self):
        for i in self.cactiVars:
            # Building a cactus
            if self.cactiVars[i]["ALIVE"] == False:
                while True:
                    self.rndX = random.randint(700, 1400)
                    for x in len(self.cactiPrevious):
                        if self.cactiPrevious[x] == self.rndX:
                            continue
                        elif self.cactiPrevious[x] != self.rndX:
                            self.cactiPrevious.append(self.rndX)
                            print(f" Cactus spawned at {self.rndX}")
                            if len(self.cactiPrevious) == 4:
                                self.cactiPrevious.pop(0)
                            break
                    break
                self.cactiVars[i]["X"] = self.rndX
                self.cactiVars[i]["IMG"] = random.choice(self.cactiImgs)
                self.cactiVars[i]["ALIVE"] = True
                self.cactiVars[i]["AVOIDED"] = False
            # Controlling spawned cacti
            elif self.cactiVars[i]["ALIVE"] == True:
                self.cactiVars[i]["X"] = self.cactiVars[i]["X"] - self.getMain.scrollSpeed
                if self.cactiVars[i]["X"] <= vw // 4:
                    if self.player.playerRect.y < 108:
                        if self.cactiVars[i]["AVOIDED"] == False:
                            self.getMain.score = self.getMain.score + 1
                            self.cactiVars[i]["AVOIDED"] = True
                        elif self.player.playerRect.y >= 108:
                            print(" You crashed into a cactus")
                            self.getMain.die()
                screenCTRL.blit(self.cactiVars[i]["IMG"], (self.cactiVars[i]["X"], vh / 2.08))
                if self.cactiVars[i]["X"] <= -125:
                    self.cactiVars[i]["ALIVE"] = False


# Class for functions and variables related to the trexes
class trex:
    def __init__(self):
        # Assets
        self.trexA = pygame.image.load(f"{ptDir}resources/img/trexA.png")
        self.trexB = pygame.image.load(f"{ptDir}resources/img/trexB.png")
        # T-rex control variables
        self.trexX = None
        self.trexImg = self.trexA
        self.spawned = False
        self.killed = False
        self.stepTimer = None

    def rng(self):
        if self.spawned == False:
            rnd = random.randint(0, 1000)
            if rnd == 500:
                self.spawned = True
                self.trexX = random.randint(700, 1400)
                print(f" T-Rex spawned at {self.trexX}")
        elif self.spawned == True:
            trex.alive()

    def alive(self):
        self.trexX = self.trexX - (main().scrollSpeed + 1)
        screenCTRL.blit(self.rexA, (self.trexX, vh / 1.9))
        self.stepTimer = datetime.now().timestamp
        if self.stepTimer - datetime.now().timestamp >= 0.1:
            if self.trexImg == self.trexA:
                self.trexImg = self.trexB
            elif self.trexImg == self.trexB:
                self.trexImg = self.trexA
            self.stepTimer = datetime.now().timestamp()
        if self.trexX <= -730:
            self.spawned = False



if __name__ == "__main__":
    try:
        pygame.display.set_icon(pygame.image.load(f"{ptDir}resources/img/trexSmall.png"))
        pygame.display.set_caption("PterodactylRun - Build Version 1.6.0")
        main().play()
    except KeyboardInterrupt:
        main.errMsgFatal(main, errs[1])
else:
    main.errMsgFatal(main, errs[2])
    sleep(2)
    sys.exit()
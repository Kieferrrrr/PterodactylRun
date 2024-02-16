# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2
# Submission 1

# Main Game File for PterodactylRun
# Build Version 1.7.0

import os
import sys
import json
import random

from time import sleep
from datetime import datetime

try:
    import pygame
    import configparser
except:
    print(" Required modules are not installed\n     run install-repair.py")

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
    os.system("title PterodactlyRun - Version 1.7.0 - CLI") # .pyw should hide the terminal but if its ran in the CLI its there
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

print(" PterodactylRun Build Version 1.7.0 Debug Output")
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
            except configparser.Error:
                main.errMsgGeneric(self, errs[6])
        except FileNotFoundError:
            main.errMsgGeneric(self, errs[3])

    def getJSON(self):
        try:
            with open(f"{ptDir}{self.saveDir}", "r") as jsonFile:
                jsonData = json.loads(jsonFile.read())
                self.highscore = jsonData["highscore"]
            jsonFile.close()
        except FileNotFoundError:
            main.errMsgGeneric(self, errs[4])

    def setJSON(self, score):
        score = int(score)
        try:
            with open(f"{ptDir}{self.saveDir}", "+r") as jsonFile:
                jsonData = {"highscore": "{:05d}".format(score)}
                jsonFile.seek(0)
                json.dump(jsonData, jsonFile, indent=4)
                jsonFile.truncate() 
                print(f" New highscore saved to scores.json ({score})")
            jsonFile.close()
        except FileNotFoundError:
            main.errMsgGeneric(self, errs[7])


# Class for functions and variables related to the pterodactyl
class pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.flyingImg = pygame.image.load(f"{ptDir}resources/img/pterodactylA.png")
        self.fallingImg = pygame.image.load(f"{ptDir}resources/img/pterodactylB.png")
        # Image handling
        self.image = self.fallingImg
        self.rect = self.image.get_rect()
        self.rect.center = (vw // 4, vh // 2)
        # Integers
        self.gravity = 0.2
        self.flySpeed = 5
        self.Yspeed = 0
        # Menu animation
        self.gravityOn = False
        self.playerTimer = datetime.now().timestamp()

    def update(self):
        if self.gravityOn:
            self.Yspeed = self.Yspeed + self.gravity
            self.rect.y = self.rect.y + self.Yspeed
        else:
            if self.image == self.fallingImg:
                if datetime.now().timestamp() - self.playerTimer >= 0.5:
                    self.image = self.flyingImg
                    self.playerTimer = datetime.now().timestamp()
            elif self.image == self.flyingImg:
                if datetime.now().timestamp() - self.playerTimer >= 0.5:
                    self.image = self.fallingImg
                    self.playerTimer = datetime.now().timestamp()

    def flap(self):
        self.Yspeed = -self.flySpeed
        if self.image == self.fallingImg:
            if datetime.now().timestamp() - self.playerTimer >= 0.1:
                self.image = self.flyingImg
                self.playerTimer = datetime.now().timestamp()
        elif self.image == self.flyingImg:
            if datetime.now().timestamp() - self.playerTimer >= 0.1:
                self.image = self.fallingImg
                self.playerTimer = datetime.now().timestamp()


# Class for the main game loop
class main():
    def __init__(self):
        # Instances of classes
        self.dataParsing = dataHandler()
        self.player = pterodactyl()
        self.cactiCTRL = cacti()
        self.trexCTRL = trex()
        # Sprites
        self.playerSprite = pygame.sprite.Group()
        self.playerSprite.add(self.player)
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
        self.scrollSpeed = int(self.dataParsing.startSpeed)
        self.highscore = self.dataParsing.highscore

    # Main game loop function
    def play(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_SPACE and self.player.rect.y > 0:
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
            screenCTRL.fill((255, 255, 255)) # Paint the sky white
            screenCTRL.blit(self.bgImg, (self.img1X, self.imgY)) # Show floor image one
            screenCTRL.blit(self.bgImg, (self.img2X, self.imgY)) # Show floor image two            
            # Show UI text elements
            screenCTRL.blit(leftTxt, (60, 12)) # Show t-rex counter and level
            screenCTRL.blit(middleTxt, (vw / 3.1, 0)) # Show pterodactylRun Title
            screenCTRL.blit(rightTxt, (vw - 250, 12)) # Show score and highscore
            screenCTRL.blit(self.trexIco, (10, 2.5)) # Show t-rex kill counter icon
            # Start game screen
            if self.player.gravityOn == False:
                txtG = self.textBig.render("Press [SPACE] to Start", True, "#454545")
                screenCTRL.blit(txtG, (vw / 3.8, 50))
            # Move and show the player
            self.playerSprite.update()
            self.playerSprite.draw(screenCTRL)
            # Reload scrolling animation
            if self.img1X <= -700:
                self.img1X = 700
            if self.img2X <= -700:
                self.img2X = 700
            # Call entity spawning and controlling functions
            if self.player.gravityOn:
                self.score = self.cactiCTRL.spawner(self.player, self.scrollSpeed, self.score)
                self.score, self.kills = self.trexCTRL.rng(self.player, self.scrollSpeed, self.score, self.kills)
            # Are you even in the air lmao
            if self.player.rect.y >= vh / 1.6:
                print(" You crashed into the floor")
                main.die(self, self.score)
            # Checking and setting level
            if int(self.score) >= self.levelScore + 50:
                self.levelScore = self.levelScore + 50
                self.level = self.level + 1
                self.scrollSpeed = self.scrollSpeed + 1
            # PyGame 
            pygame.display.flip()
            clock.tick(int(self.dataParsing.fps))

        pygame.quit()
        sys.exit()

    # Killing the pterodactyl and breaking the main loop
    def die(self, score):
        self.score = score
        self.running = False
        if int(self.score) > int(self.highscore):
            self.dataParsing.setJSON(self.score)
        restart = self.textBig.render("Game Over Press [SPACE] to Restart", True, "#454545")
        while True:
            #self.playerSprite.draw(screenCTRL)
            screenCTRL.blit(restart, (vw / 7, 50))
            for i in self.cactiCTRL.cactiVars:
                if self.cactiCTRL.cactiVars[i]["ALIVE"] == True:
                    screenCTRL.blit(self.cactiCTRL.cactiVars[i]["IMG"] , (self.cactiCTRL.cactiVars[i]["X"], vh / 2.08))
            if self.trexCTRL.spawned == True:
                screenCTRL.blit(self.trexCTRL.trexImg, (self.trexCTRL.trexX, vh / 1.9))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_SPACE:
                        print(" Restarted game")
                        main().play()
            pygame.display.flip()

    # Broad spectrum error handler for fixable errors
    def errMsgGeneric(self, err):
        print(err)

    # Error handling for fatal errors
    def errMsgFatal(self, err):
        pygame.quit
        print(err)
        input(" Press enter to exit")
        sys.exit()


# Class for functions and variables related to the cacti
class cacti():
    def __init__(self):
        # Instance of class pterodactyl
        #self.player = pterodactyl()
        # Assets
        self.cactusImgA = pygame.image.load(f"{ptDir}resources/img/cactusA.png")
        self.cactusImgB = pygame.image.load(f"{ptDir}resources/img/cactusB.png")
        self.cactiImgs = [self.cactusImgA, self.cactusImgB]
        # Integers
        self.rndX = None
        self.rect = self.cactusImgA.get_rect()
        self.a = None
        self.b = None
        # Nested dictionary of rendered cacti variables
        self.cactiVars = {
            1: {"X": None, "IMG": None, "A":None, "B":None, "ALIVE": False, "AVOIDED": False},
            2: {"X": None, "IMG": None, "A":None, "B":None, "ALIVE": False, "AVOIDED": False},
            3: {"X": None, "IMG": None, "A":None, "B":None, "ALIVE": False, "AVOIDED": False},
            4: {"X": None, "IMG": None, "A":None, "B":None, "ALIVE": False, "AVOIDED": False}
        }
        # Queue of previously generated cacti X co-ordinates
        self.cactiPrevious = []
        
    def spawner(self, player, scrollSpeed, score):
        self.score = score
        for i in self.cactiVars:
            # Building a cactus
            if self.cactiVars[i]["ALIVE"] == False:
                while True:
                    self.rndX = random.randint(700, 1400)
                    for x in range(len(self.cactiPrevious)):
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
                if self.cactiVars[i]["IMG"] == self.cactusImgA:
                    self.cactiVars[i]["A"] = 160
                    self.cactiVars[i]["B"] = 230
                if self.cactiVars[i]["IMG"] == self.cactusImgB:
                    self.cactiVars[i]["A"] = 130
                    self.cactiVars[i]["B"] = 230
                self.cactiVars[i]["ALIVE"] = True
                self.cactiVars[i]["AVOIDED"] = False
                print(f" Cactus spawned at {self.cactiVars[i]['X']}")
            # Controlling spawned cacti
            if self.cactiVars[i]["ALIVE"] == True:
                self.cactiVars[i]["X"] = self.cactiVars[i]["X"] - scrollSpeed
                if self.cactiVars[i]["AVOIDED"] == False:
                    if player.rect.y >= 100 and self.cactiVars[i]["X"] in range(self.cactiVars[i]["A"], self.cactiVars[i]["B"]):
                        print(" You crashed into a cactus")
                        self.cactiVars[i]["AVOIDED"] = False
                        main.die(main(), self.score)
                    if self.cactiVars[i]["X"] <= 175:
                        self.cactiVars[i]["AVOIDED"] = True
                        self.score = self.score + 1
                elif self.cactiVars[i]["AVOIDED"] == True:
                    pass
                screenCTRL.blit(self.cactiVars[i]["IMG"], (self.cactiVars[i]["X"], vh / 2.08))
                if self.cactiVars[i]["X"] <= -125:
                    self.cactiVars[i]["ALIVE"] = False
        return self.score


# Class for functions and variables related to the trexes
class trex():
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

    def rng(self, player, scrollSpeed, score, kills):
        self.player = player
        self.scrollSpeed = scrollSpeed
        self.score = score
        self.kills = kills
        if self.spawned == False:
            rnd = random.randint(0, 1000)
            if rnd == 500:
                self.spawned = True
                self.trexX = random.randint(700, 1400)
                self.stepTimer = datetime.now().timestamp()
                print(f" T-Rex spawned at {self.trexX}")
        elif self.spawned == True:
            trex.alive(self)
        return self.score, self.kills

    def alive(self):
        self.trexX = self.trexX - (self.scrollSpeed + 1)
        screenCTRL.blit(self.trexImg, (self.trexX, vh / 1.9))
        if datetime.now().timestamp() - self.stepTimer >= 0.1:
            if self.trexImg == self.trexA:
                self.trexImg = self.trexB
            elif self.trexImg == self.trexB:
                self.trexImg = self.trexA
            self.stepTimer = datetime.now().timestamp()
        if self.trexX <= -730:
            self.spawned = False
        if self.spawned == True:
            if self.player.rect.y >= 90 and self.trexX in range(160, 230):
                print(" You killed a T-Rex")
                self.spawned = False
                self.kills = self.kills + 1
                self.score = self.score + 5


if __name__ == "__main__":
    try:
        pygame.display.set_icon(pygame.image.load(f"{ptDir}resources/img/trexSmall.png"))
        pygame.display.set_caption("PterodactylRun - Build Version 1.7.0")
        main().play()
    except KeyboardInterrupt:
        main.errMsgFatal(main, errs[1])
else:
    main.errMsgFatal(main, errs[2])
    sleep(2)
    sys.exit()

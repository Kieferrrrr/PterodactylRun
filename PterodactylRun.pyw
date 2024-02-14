# PterodactlRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2

# Main Game File for PterodactylRun
# Build Version 1.5.1

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
    4: " Error readin scores.json\n     not loading or saving high scores\n     run install-repair.py to fix", # scores.json could not be found/used
    5: " Unable detect your operating system\n     please create an issue on GitHub with the myOS tag", # Your OS was not recognised
    6: " A value in config.ini is not useable\n    using default settings" # A value in config.ini is not in the correct format
}

if sys.platform == "win32": # Windows
    cl = "cls"
    os.system("mode 80,20 && title PterodactlyRun - Version 1.5.1 - CLI") # .pyw should hide the terminal but if its ran in the CLI its there
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

print(" PterodactylRun Build Version 1.5.1 Debug Output")
print(f" Detected host system - {detOS}")

vw = 750 # screen view width
vh = 350 # screen view height

fileDir = os.path.realpath(__file__) # Game directory
dir = os.path.dirname(fileDir)

pygame.init()

# Class for getting and setting values in config.ini and scores.json
class dataHandler:
    def getINI(self):
        conf = configparser.ConfigParser()
        try:
            conf.read(f"resources/etc/config.ini")
            startSpeed = conf["CONFIG"]["startSpeed"]
            fps = conf["CONFIG"]["fps"]
            saveHigh = conf["CONFIG"]["saveHigh"]
            self.saveDir = conf["CONFIG"]["saveDir"]
            self.saveDebug = conf["DEBUG"]["saveDebug"]
            self.debugDir = conf["DEBUG"]["debugDir"]
            self.testMode = conf["TEST"]["testMode"]
            if self.testMode == True:
                print(" You are in test mode\n    you cannot set a highscore")
        except:
            main.errMsgGeneric(errs[3])
            fps = 60
            startSpeed = 3
            saveHigh = True
            self.saveDir = f"resources/etc/scores.json"
            self.saveDebug = False
            self.debugDir = None
            self.testMode = False
        return int(fps), int(startSpeed), saveHigh

    def getJSON(self):
        try:
            file = open(self.saveDir, "r")
            jsonData = json.loads(file.read())
            self.highscore = jsonData["highscore"]
            file.close()
        except:
            self.noJSON = True
            self.highscore = "00000"
            main.errMsgGeneric(errs[4])
        return self.highscore

    def setJSON(self, score):
        try:
            file = open(self.saveDir, "r+")
            jsonData = {"highscore": "{:05d}".format(score)}
            file.seek(0)
            json.dump(jsonData, file, indent=4)
            file.truncate()
            file.close()
            print(f" New highscore saved to scores.json ({score})")
        except:
            print(" Failed to save new highscore")
            main.errMsgGeneric(errs[5])

# Class for functions and variables related to the pterodactyl
class pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.fallingImg = pygame.image.load(f"resources/img/pterodactylA.png")
        self.flyingImg = pygame.image.load(f"resources/img/pterodactylB.png")
        # Image Handling
        self.image = self.fallingImg
        self.rect = self.image.get_rect() # getting the x, y, width, height
        self.rect.center = (vw // 4, vh // 2) # Set the center to 1/4 of the screen width and 1/2 of the screen height
        # Integers
        self.gravity = 0.2
        self.flySpeed = 5
        self.Yspeed = 0
        # Menu Animation
        self.gravityOn = False
        self.cTime = datetime.now().timestamp()

    def update(self):
        if self.gravityOn:
            self.Yspeed = self.Yspeed + self.gravity
            self.rect.y = self.rect.y + self.Yspeed

    def flap(self):
        self.Yspeed = -self.flySpeed
        if self.image == self.fallingImg:
            if datetime.now().timestamp() - self.cTime >= 0.1:
                self.image = self.flyingImg
                self.cTime = datetime.now().timestamp()
        elif self.image == self.flyingImg:
            if datetime.now().timestamp() - self.cTime >= 0.1:
                self.image = self.fallingImg
                self.cTime = datetime.now().timestamp()


# Class for the main game loop
class main:
    def __init__(self):
        # config.ini and scores.json
        self.dataParsing = dataHandler()
        self.fps, self.startSpeed, self.saveHigh = self.dataParsing.getINI()
        self.highscore = self.dataParsing.getJSON()
        # Sprites and Entities
        self.playerSprite = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player = pterodactyl()
        self.cactusCTRL = cactus()
        self.trexCTRL = trex()
        self.playerSprite.add(self.player)
        # Assets
        self.backImg = pygame.image.load(f"resources/img/700x175.png")
        self.trexIco = pygame.image.load(f"resources/img/trexSmall.png")
        self.textBig = pygame.font.Font(f"resources/etc/GameOver.ttf", 75)
        self.textSmall = pygame.font.Font(f"resources/etc/GameOver.ttf", 48)
        # Integers
        self.level = 1
        self.levelScore = 0
        self.score = 00000
        self.kills = 00000
        self.img1X = -350
        self.img2X = 350
        self.bothImgY = 275
        self.scrollSpeed = self.startSpeed
        # PyGame Gameplay
        self.screenCTRL = pygame.display.set_mode((vw, vh))
        self.clock = pygame.time.Clock()

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
            # Scroll the floor
            self.img1X = self.img1X - self.scrollSpeed # Scroll image one along the X axis
            self.img2X = self.img2X - self.scrollSpeed # Scroll image two along the X axis
            # Show world assets
            self.screenCTRL.fill((255,255,255)) # Paint the sky white
            self.screenCTRL.blit(self.backImg, (self.img1X, self.bothImgY)) # Show floor image one
            self.screenCTRL.blit(self.backImg, (self.img2X, self.bothImgY)) # Show floor image two
            # Create UI text elements
            txtA = self.textSmall.render("x{:05d}".format(self.kills).ljust(12) + f"Level {self.level}", True, "#454545")
            txtB = self.textBig.render("PterodactylRun", True, "#454545")
            txtC = self.textSmall.render("Score {:05d}".format(self.score).ljust(16) + f"High {self.highscore}", True, "#454545")
            # Show UI text elements
            self.screenCTRL.blit(txtA, (60, 12)) # Show t-rex counter and level
            self.screenCTRL.blit(txtB, (vw / 3, 0)) # Show pterodactylRun Title
            self.screenCTRL.blit(txtC, (vw - 250, 12)) # Show score and highscore
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
            # Spawn, scroll, show and die to cacti
            if self.player.gravityOn == True:
                for i in self.cactusCTRL.cacti:
                    if self.cactusCTRL.cacti[i]["ALIVE"] == False:
                        while True:
                            rndX = random.randint(700, 1400)
                            if rndX <= self.cactusCTRL.lastX - 120 or rndX >= self.cactusCTRL.lastX + 120:
                                self.cactusCTRL.lastX = rndX
                                print(f" Spawned cactus at {self.cactusCTRL.lastX}")
                                break
                            else:
                                print(" Tried to spawn cactus too close to last cactus")
                        self.cactusCTRL.cacti[i]["X"] = rndX
                        self.cactusCTRL.cacti[i]["IMG"] = random.choice(self.cactusCTRL.cactiImgs)
                        self.cactusCTRL.cacti[i]["ALIVE"] = True
                        self.cactusCTRL.cacti[i]["AVOIDED"] = False
                    elif self.cactusCTRL.cacti[i]["ALIVE"] == True:
                        self.cactusCTRL.cacti[i]["X"] = self.cactusCTRL.cacti[i]["X"] - self.scrollSpeed
                        if self.cactusCTRL.cacti[i]["X"] <= vw // 4:
                            if self.player.rect.y < 108: # when i put this on the above "if" statement with an "and" it didnt work for some reason
                                if self.cactusCTRL.cacti[i]["AVOIDED"] == False:
                                    self.score = self.score + 1
                                    self.cactusCTRL.cacti[i]["AVOIDED"] = True
                            else:
                                print(" You crashed into a cactus")
                                main.die(self)
                        self.screenCTRL.blit(self.cactusCTRL.cacti[i]["IMG"], (self.cactusCTRL.cacti[i]["X"], vh / 2.08))
                        if self.cactusCTRL.cacti[i]["X"] <= -125:
                            self.cactusCTRL.cacti[i]["ALIVE"] = False

                self.trexCTRL.rng()
                if self.trexCTRL.spawned == True:
                    self.trexCTRL.trexX = self.trexCTRL.trexX - (self.scrollSpeed + 1)
                    self.screenCTRL.blit(self.trexCTRL.trexImg, (self.trexCTRL.trexX, vh / 1.9))
                    if self.trexCTRL.tTime - self.trexCTRL.tTime >= 0.1:
                        if self.trexCTRL.trexImg == self.trexCTRL.trexA:
                            self.trexCTRL.trexImg = self.trexCTRL.trexB
                            self.trexCTRL.tTime = datetime.now().timestamp()
                        elif self.trexCTRL.trexImg == self.trexCTRL.trexB:
                            self.trexCTRL.trexImg = self.trexCTRL.trexA
                            self.trexCTRL.tTime = datetime.now().timestamp()
                    if self.trexCTRL.trexX <= -730:
                        self.trexCTRL.spawned = False
                    


            if self.player.rect.y >= vh / 1.6:
                print(" You crashed into the floor")
                main.die(self)
            # Checking and setting level
            if self.score == self.levelScore + 50 or self.score > self.levelScore + 50:
                self.levelScore = self.levelScore + 50
                self.level = self.level + 1
                self.scrollSpeed = self.scrollSpeed + 1
            # Commit changes
            self.playerSprite.update()  
            self.playerSprite.draw(self.screenCTRL)
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

    def die(self):
        self.running = False
        if int(self.score) > int(self.highscore):
            self.dataParsing.setJSON(self.score)
        restart = self.textBig.render("Game Over Press [SPACE] to Restart", True, "#454545")
        while True:
            self.screenCTRL.blit(restart, (vw / 6, 50))
            self.playerSprite.draw(self.screenCTRL) # Keep the pterodactyl corpse on screen
            for i in self.cactusCTRL.cacti: # Keep all the cacti on screen
                self.screenCTRL.blit(self.cactusCTRL.cacti[i]["IMG"], (self.cactusCTRL.cacti[i]["X"], vh / 2.08))
            if self.trexCTRL.spawned == True:
                self.screenCTRL.blit(self.trexCTRL.trexImg, (self.trexCTRL.trexX, vh / 1.9))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_SPACE:
                        print(" Restarted game")
                        main().play()
            pygame.display.flip()

    # Broad spectrum error messages for fixable errors
    def errMsgGeneric(self, err):
        print(err)
        return
    
    # Fatal error messages
    def errMsgFatal(self, err):
        pygame.quit()
        print(err)
        sys.exit()


# Basically just seperating the cacti variables away from the rest
class cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.cactusA = pygame.image.load(f"resources/img/cactusBigA.png")
        self.cactusB = pygame.image.load(f"resources/img/cactusBigB.png")
        self.cactiImgs = [self.cactusA, self.cactusB]
        # Variables
        self.rect = self.cactusA.get_rect()
        self.lastX = 0
        # Nested dictionary of rendered cacti variables
        self.cacti = {
            1: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False},
            2: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False},
            3: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False},
            4: {"X": None, "IMG": None, "ALIVE": False, "AVOIDED": False}
        }
    

# And again, just sperating the t-rex variables
class trex(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.trexA = pygame.image.load(f"resources/img/trexA.png")
        self.trexB = pygame.image.load(f"resources/img/trexB.png")
        # T-rex control variables
        self.trexX = None
        self.trexImg = self.trexA
        self.spawned = False
        self.killed = False
        self.tTime = datetime.now().timestamp()

    def rng(self):
        if self.spawned == False:
            rand = random.randint(0, 1000)
            if rand == 500:
                self.spawned = True
                self.trexX = random.randint(700, 1400)
                print(f" T-Rex spawned at {self.trexX}")


if __name__ == "__main__":
    try:
        pygame.display.set_icon(pygame.image.load(f"resources/img/trexSmall.png"))
        pygame.display.set_caption("PterodactylRun - Build Version 1.5.1")
        main().play()
    except KeyboardInterrupt:
        main.errMsgFatal(main, errs[1])
else:
    main.errMsgFatal(main, errs[2])
    sleep(2)
    sys.exit()

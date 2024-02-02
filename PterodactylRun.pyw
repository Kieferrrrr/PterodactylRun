# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2

# Main Game File for PterodactylRun
# Build Version 1.0.4

import os
import sys
import json
import pygame
import configparser

from time import sleep
from datetime import datetime
from tkinter import messagebox

from platform import system as OS


# Dictionary of basic/common errors
errs = {
    1: " Error Building GUI Window", # engine.guiGen() did not function correctly
    2: " Error Rendering World", # engine.recurringGen() did not function correctly
    3: " Error During Game Keep Alive", # Game ran into a fatal error whilst playing
    4: " CTRL+C Pressed", # Keyboard interrupt, user wants to quit
    5: " Error Loading config.ini", # Config file is not where it should be or not existant
    6: " Error Loading scores.jsonc", # score saving file is not where it should be or not existant
    7: " Current Working Directory is Not the Same as the Game File", # Game must be run from the directory PterodactylRun.py is in
    8: " PterodactylRun.py Cannot be Imported as a Module", # Attempted to import PterdactylRun.py to another file
    9: " 'savesscores' values in config.ini is not useable" # savescores value in config.ini is not True/False
}

if OS() == "Windows":
    cl = "cls"
    os.system("mode 80,20 && title Pterodactly Run - Version 1.0.4 - CLI") # .pyw should hide the terminal but if its ran in the CLI its there
else:
    cl = "clear"


vw = 750 # screen view width
vh = 350 # screen view height


# Class for getting and setting values in config.ini and scores.json
class dataHandler:
    def getINI(self):
        conf = configparser.ConfigParser()
        try:
            conf.read("resources/etc/config.ini")
        except:
            print(errs[5])
            sleep(2)
            sys.exit()
        fps = conf['CONFIG']['fps']
        saveScores = conf['CONFIG']['saveScores']
        self.saveDir = conf['CONFIG']['saveDir']
        return int(fps), saveScores

    def getJSON(self):
        file = open(self.saveDir, "r")
        jsonData = json.loads(file.read())
        self.highscore = jsonData["highscore"]
        lastscore = jsonData["lastscore"]
        file.close()
        return self.highscore, lastscore

    def setJSON(self, score):
        if int(score) > int(self.highscore):
            file = open(self.saveDir, "r+")
            jsonData = {"highscore": f"{score}", "lastscore": f"{score}"}
            file.seek(0)
            json.dump(jsonData, file, indent=4)
            file.truncate()
            file.close()
        elif int(score) < int(self.highscore):
            file = open(self.saveDir, "r+")
            jsonData = {"highscore": f"{self.highscore}", "lastscore": f"{score}"}
            file.seek(0)
            json.dump(jsonData, file, indent=4)
            file.truncate()
            file.close()

# Class for all functions and variables related to the pterodactyl
class pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.fallingImg = pygame.image.load("resources/img/pterodactylA.png")
        self.flyingImg = pygame.image.load("resources/img/pterodactylB.png")
        # Image Handling
        self.image = self.fallingImg
        self.rect = self.image.get_rect() # getting the x, y, width, height
        self.rect.center = (vw // 4, vh // 2) # Set the center to 1/4 of the screen width and 1/2 of the screen height
        # Integers
        self.gravity = 0.5
        self.flySpeed = 5
        self.Yspeed = 0
        # Menu Animation
        self.gravityOn = False
        self.cTime = datetime.now().timestamp()

    def update(self):
        if self.gravityOn:
            self.Yspeed = self.Yspeed + self.gravity
            self.rect.y = self.rect.y + self.Yspeed
        elif datetime.now().timestamp() - self.cTime >= 0.5:
            if self.image == self.fallingImg:
                self.image = self.flyingImg
                self.cTime = datetime.now().timestamp()
            else:
                self.image = self.fallingImg
                self.cTime = datetime.now().timestamp()

    def flap(self):
        self.Yspeed = -self.flySpeed
        self.image = self.flyingImg


class hazards:
    def __init__(self):
        # Assets
        self.trexA = pygame.image.load("resources/img/trexA.png")
        self.trexB = pygame.image.load("resources/img/trexB.png")
        self.trexC = pygame.image.load("resources/img/trexB.png")


# Class for the main game loop
class main:
    def __init__(self):
        # config.ini and scores.json
        self.dataParsing = dataHandler()
        self.fps, self.savescores = self.dataParsing.getINI()
        self.highscore, self.lastscore = self.dataPasing.getJSON()
        # Sprites
        self.allSprites = pygame.sprite.Group()
        self.player = pterodactyl()
        self.allSprites.add(self.player)
        # PyGame Gameplay
        self.screenCTRL = pygame.display.set_mode((vw, vh))
        self.clock = pygame.time.Clock()
        # Assets
        self.backImg = pygame.image.load("resources/img/700x150.png")
        self.textBig = pygame.font.Font("resoruces/etc/GameOver.ttf", 75)
        self.textSmall = pygame.font.Font("resoruces/etc/GameOver.ttf", 48)
        # Integers
        self.score = 00000
        self.kils = 00000
        self.img1X = 0
        self.img2X = 700
        self.bothImgY = 275

    def play(self):
        running = True
        img1X = self.img1X
        img2X = self.img2X
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_SPACE:
                        self.player.flap()
                        self.player.gravityOn = True
                        break

            img1X = img1X - 1
            img2X = img2X - 1
            self.screenCTRL.fill((255,255,255))
            self.screenCTRL.blit(self.backImg, (img1X, self.bothImgY))
            self.screenCTRL.blit(self.backImg, (img2X, self.bothImgY))
            if img1X == -350 or img1X < -350:
                img1X = 350
            if img2X == -350 or img2X < -350:
                img2X = 350
            if img1X > 350:
                img1X = 0
            if img2X > 350:
                img2X = 350

            txtA = self.textBig.render("PterodactylRun", True, "#454545")
            txtB = self.textSmall.render("Score {:05d}".format(self.score), True, "#454545")
            txtC = self.textSmall.render(f"High {self.highscore}", True, "#454545")
            txtD = self.textSmall.render("x{:05d}".format(self.kills), True, "#454545")

            self.screenCTRL.blit(txtA, (vw / 3, 0))
            self.screenCTRL.blit(txtB, (vw - 120, 12))
            self.screenCTRL.blit(txtC, (vw - 225, 12))
            self.screenCTRL.blit(txtD, (50, 12))
            self.sprites.update()
            self.sprites.draw(self.screenCTRL)
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

    def die(self):
        if self.savescores == True:
            dataHandler.writeJSON(self.score)
        elif self.savescores == False:
            print
        else:
            print(f"{errs[9]}\n     Saving score as a default") # popup window errs[] maybe
            dataHandler.writeJSON(self.score)

    # Broad spectrum error handling
    def errMsgGeneric(err):
        print

    # Fatal error handling
    def errMsgFatal(err):
        pygame.quit()
        print(err)
        # Tk().wm_withdraw() #to hide the main window
        messagebox.showinfo(title="Fatal Error", message=err)


if __name__ == "__main__":
    try:
        pygame.init()
        pygame.display.set_caption("PterodactylRun - V1.0.4")
        main().play()
    except KeyboardInterrupt:
        main.errMsgFatal(errs[4])
else:
    print(errs[8])
    sleep(2)
    sys.exit()

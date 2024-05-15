# PterodactylRun

# Level 3 Extended Diploma Computer Science
# Year 2
# Unit 14 - Assignment 2 - Part 2
# Submission 2

# Main Game File for PterodactylRun
# Build Version 2.0.0

import os
import sys
import json
import random

from datetime import datetime

try: # Modules which need installing
    import pygame
    import configparser
    from colorama import just_fix_windows_console
except:
    print(" Required modules are not installed\n     run install-repair.py")


__version__ = "2.0.0"

# Dictionary of basic/common errors
errs = {
    1: "CTRL+C pressed", # Keyboard interrupt pressed in terminal
    2: "Cannot import PterodactylRun.pyw as a module", # PterodactylRun.pyw is not a module
    3: "Error reading config.ini - using default settings - run install-repair.py to fix", # config.ini could not be found/used
    4: "Error reading scores.json - not loading or saving high scores - run install-repair.py to fix", # scores.json could not be found/used
    5: "Unable to detect your operating system", # Your OS was not recognised
    6: "A value in config.ini is not useable - using default settings - run install-setup.py to fix", # A value in config.ini is not the correct format
    7: "Failed to save high score - run install-repair.py to fix" # scores.json could not be found/used during writing
}

if sys.platform == "win32": # Windows
    os.system(f"title PterodactlyRun - Version {__version__} - CLI") # .pyw should hide the terminal but if its ran in the CLI its there
    detOS = "Windows"
    just_fix_windows_console() # Force ANSI colour codes to work
elif sys.platform == "linux": # Linux
    detOS = "Linux"
elif sys.platform == "darwin": # MacOS
    detOS = "MacOS"
else:
    print(errs[5])
    detOS = "Unreocgnised"

vw = 700 # Screen view width
vh = 350 # Screen view height

firstRun = True # main.play() cant see this

white = "\x1b[38;5;254m" # Text
grey = "\x1b[38;5;245m"  # Events and info
blue = "\x1b[38;5;45m"   # Variables
amber = "\x1b[38;5;220m" # Errors
red = "\x1b[38;5;196m"   # Fatal errors

ptDir = f"{os.path.dirname(os.path.realpath(__file__))}/" # Full directory of the PterodactylRun.pyw file
ptDir = ptDir.replace("\\", "/") # Fixing directories such as "C:\Users\test\Desktop\PterodactylRun/resources/etc"

pygame.init()
screenCTRL = pygame.display.set_mode((vw, vh))
clock = pygame.time.Clock()

print(f"\n{white} PterodactylRun Build Version {blue}{__version__} {white}Debug Output")
print(f"{white} Detected Host System - {blue}{detOS}{white}\n")

# Broad spectrum error message controller for simple errors
def throwErr(err, fatal: bool):
        if not fatal:
            print(f" {white}[{amber}Error{white}] {err}")
        if fatal: # Controlled exit for fatal errors
            print(f" {white}[{amber}Error{white}]-[{red}Fatal{white}] {err}")
            pygame.quit
            if detOS == "Windows":
                os.system("title %ComSpec%") # Reset the CLI title
            sys.exit()


# Main class for controlling all gameplay from
class main:
    def __init__(self):
        # Instances of classes
        self.dataParsing = dataHandler()
        self.player = pterodactyl()
        self.trexCTRL = trex()
        self.cacti = {1: cactus(), 2: cactus(), 3: cactus(), 4: cactus()}
        # Data fetching
        self.dataParsing.getINI()
        self.dataParsing.getJSON()
        # Image and etc assets
        self.bgImg = pygame.image.load(f"{ptDir}resources/img/700x175.png")
        self.trexIco = pygame.image.load(f"{ptDir}resources/img/trexSmall.png")
        self.textBig = pygame.font.Font(f"{ptDir}resources/etc/GameOver.ttf", 75)
        self.textSmall = pygame.font.Font(f"{ptDir}resources/etc/GameOver.ttf", 48)
        # Variables
        self.level = 1
        self.levelScore = 0
        self.score = 00000
        self.kills = 00000
        self.img1X = -350
        self.img2X = 350
        self.imgY = 275
        self.scrollSpeed = int(self.dataParsing.startSpeed)
        self.highscore = self.dataParsing.highscore
        # Cacti
            # List for storing previous cacti X co-ordinates for all for instances to see
        self.cStore = []
        for i in range(1, 5):
            self.cacti[i].mainAccess = self
        # T-Rex
        self.trexCTRL.mainAccess = self

    def play(self):
        global firstRun
        if firstRun == True:
            print(f" {white}[{grey}Info{white}] FPS: {blue}{self.dataParsing.fps}")
            print(f" {white}[{grey}Info{white}] Start speed: {blue}{self.scrollSpeed}")
            print(f" {white}[{grey}Info{white}] Saving scores: {blue}{self.dataParsing.saveHigh}")
            print(f" {white}[{grey}Info{white}] Score directory: {blue}{self.dataParsing.saveDir}{white}\n")
            firstRun = False
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
            self.gui() # Render GUI elements
            # Start game screen
            if not self.player.gravityOn:
                self.player.start()
                txtG = self.textBig.render("Press [SPACE] to Start", True, "#454545")
                screenCTRL.blit(txtG, (vw / 3.8, 50))
            # Scroll the floor
            self.img1X = self.img1X - self.scrollSpeed # Scroll image one
            self.img2X = self.img2X - self.scrollSpeed # Scroll image two
            # Reload scrolling animation if its finished its cycle
            if self.img1X <= -700:
                self.img1X = 700
            if self.img2X <= -700:
                self.img2X = 700
            # Entity spawning and control
            if self.player.gravityOn:
                for i in range(1, 5):
                    self.score = self.score + self.cacti[i].ctrl()
                self.score = self.score + self.trexCTRL.ctrl()
                # Make the pterodacatyl fall
                self.player.fall()
            self.render() # Render everything on screen
            # Are you even in the air lmao
            if self.player.rect.y >= vh / 1.6:
                print(f" {white}[{grey}Event{white}] You crashed into the floor")
                main.die(self)
            # Update level data based on score        
            if self.score / self.level == 50:
                self.level = self.level + 1
                self.scrollSpeed = self.scrollSpeed + 1
                print(f" {white}[{grey}Event{white}] Reached Level {blue}{self.level}{white} Speed is now {blue}{self.scrollSpeed}{white}")
        # Exit
        pygame.quit()
        sys.exit()
    
    def die(self):
        self.running = False
        if self.dataParsing.saveHigh == True:
            if int(self.score) > int(self.highscore):
                self.dataParsing.setJSON(self.score)
        restart = self.textBig.render("Game Over Press [SPACE] to Restart", True, "#454545")
        while True:
            self.gui()
            for i in range(1, 5):
                screenCTRL.blit(self.cacti[i].img, (self.cacti[i].x,  vh / 2.08))
            if self.trexCTRL.alive:
                screenCTRL.blit(self.trexCTRL.img, (self.trexCTRL.x, vh / 1.9))
            screenCTRL.blit(restart, (vw / 7, 50))
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.system("title %ComSpec%")
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_SPACE:
                        print(f" {white}[{grey}Event{white}] Restarted game")
                        main().play()

    def gui(self):
        # Create UI elements
        leftTxt = self.textSmall.render("x{:05d}".format(self.kills).ljust(12) + f"Level {self.level}", True, "#454545")
        middleTxt = self.textBig.render("PterodactylRun", True, "#454545")
        rightTxt = self.textSmall.render("Score {:05d}".format(self.score).ljust(16) + f"High {self.highscore}", True, "#454545")
        # Show world assets
        screenCTRL.fill((255, 255, 255)) # Paint the sky white
        screenCTRL.blit(self.bgImg, (self.img1X, self.imgY)) # Show floor image one
        screenCTRL.blit(self.bgImg, (self.img2X, self.imgY)) # Show floor image two            
        # Show UI text elements
        screenCTRL.blit(leftTxt, (60, 12)) # Show t-rex counter and level
        screenCTRL.blit(middleTxt, (vw / 3.1, 0)) # Show pterodactylRun Title
        screenCTRL.blit(rightTxt, (vw - 250, 12)) # Show score and highscore
        screenCTRL.blit(self.trexIco, (10, 2.5)) # Show t-rex kill counter icon
        # Show pterodactyl
        screenCTRL.blit(self.player.img, (vw // 4, self.player.rect.y))

    def render(self):
        pygame.display.flip()
        clock.tick(int(self.dataParsing.fps))


# Class for getting and setting variables in /resources/etc
class dataHandler:
    def __init__(self):
        # Default config.ini settings incase of file read errors
        self.startSpeed = 3
        self.fps = 60
        self.saveHigh = True
        self.saveDir = f"{ptDir}resources/etc/scores.json"
        # Default score.json value incase of file read error
        self.highscore = "00000"

    def getINI(self):
        try:
            conf = configparser.ConfigParser()
            conf.read(f"{ptDir}resources/etc/config.ini")
            try:
                # General configurations for the game
                self.startSpeed = conf["CONFIG"]["startSpeed"]
                self.fps = conf["CONFIG"]["fps"]
                self.saveHigh = int(conf["CONFIG"]["saveHigh"])
                self.saveHigh = bool(self.saveHigh) # int to bool conversion to change 1 to True and 0 to False
                self.saveDir = conf["CONFIG"]["saveDir"]
            except configparser.Error:
                throwErr(errs[6], fatal=False)
        except FileNotFoundError:
            throwErr(errs[3], fatal=False)

    def getJSON(self):
        try:
            with open(f"{ptDir}{self.saveDir}", "r") as jsonFile:
                jsonData = json.loads(jsonFile.read())
                self.highscore = jsonData["highscore"]
            jsonFile.close()
        except FileNotFoundError:
            throwErr(errs[4], fatal=False)

    def setJSON(self, score):
        score = int(score)
        try:
            with open(f"{ptDir}{self.saveDir}", "+r") as jsonFile:
                jsonData = {"highscore": "{:05d}".format(score)}
                jsonFile.seek(0)
                json.dump(jsonData, jsonFile, indent=4)
                jsonFile.truncate() 
                print(f" {white}[{grey}Event{white}] New highscore saved to scores.json ({blue}{score}{white})")
            jsonFile.close()
        except FileNotFoundError:
            throwErr(errs[7], fatal=False)


# Class for all variables and functions to do with the pterodactyl
class pterodactyl:
    def __init__(self):
        # Pterodactyl asset images
        self.imgA = pygame.image.load(f"{ptDir}resources/img/pterodactylA.png") # Falling
        self.imgB = pygame.image.load(f"{ptDir}resources/img/pterodactylB.png") # Flying
        # Image handling
        self.img = self.imgB
        self.rect = self.img.get_rect()
        self.rect.center = (vw // 4, vh // 2)
        # Integers
        self.fallSpeed = 0
        self.gravity = 0.2
        self.flapStrength = 5
        # Menu animation
        self.gravityOn = False
        self.playerTimer = datetime.now().timestamp()

    def start(self):
        if datetime.now().timestamp() - self.playerTimer >= 0.5:
            if self.img == self.imgA: # Falling image
                self.img = self.imgB
            elif self.img == self.imgB: # Flying image
                self.img = self.imgA
            self.playerTimer = datetime.now().timestamp()

    def fall(self):
        if datetime.now().timestamp() - self.playerTimer >= 0.1:
            if self.img == self.imgB:
                self.img = self.imgA
        self.fallSpeed = self.fallSpeed + self.gravity # Players fall speed is increased due to gravity
        self.rect.y = self.rect.y + self.fallSpeed     # Players Y co-ordinate is increased (visually falls)
    
    def flap(self):
        self.img = self.imgB
        self.playerTimer = datetime.now().timestamp()
        self.fallSpeed = -self.flapStrength


# Class for all variables and functions to do with the trex
class trex:
    def __init__(self):
        # Trex asset images
        self.imgA = pygame.image.load(f"{ptDir}resources/img/trexA.png")
        self.imgB = pygame.image.load(f"{ptDir}resources/img/trexB.png")
        # T-rex status vars
        self.x = None
        self.img = self.imgA
        self.alive = False
        self.killed = False
        self.stepTimer = None
        # Access to main
        self.mainAccess = None

    def ctrl(self) -> int:
        if self.alive == False:
            if random.randint(0, 1000) == 500:
                self.alive = True
                self.x = random.randint(700, 1400)
                self.stepTimer = datetime.now().timestamp()
                print(f" {white}[{grey}Event{white}] T-Rex spawned at {blue}{self.x}{white}")
        elif self.alive == True:
            self.x = self.x - (self.mainAccess.scrollSpeed + 1) # Trex always runs faster than the floor scrolls
            screenCTRL.blit(self.img, (self.x, vh / 1.9))
            # step timer image changing
            if datetime.now().timestamp() - self.stepTimer >= 0.1:
                if self.img == self.imgA:
                    self.img = self.imgB
                elif self.img == self.imgB:
                    self.img = self.imgA
                self.stepTimer = datetime.now().timestamp()
            if self.mainAccess.player.rect.y >= 90 and self.x in range(160, 230):
                print(f" {white}[{grey}Event{white}] You killed a T-Rex")
                self.alive = False
                self.mainAccess.kills = self.mainAccess.kills + 1
                self.mainAccess.score = self.mainAccess.score + 5
            if self.x <= -730:
                self.alive = False
            if self.killed == True:
                self.alive = False
                return 5 # Adds 5 to the score in main if a trex is killed
        return 0 # Adds nothing to the score if you do not kill the trex


# Class for all variables and functions to do with the cacti
class cactus:
    def __init__(self):
        # Cactus asset images
        self.imgA = pygame.image.load(f"{ptDir}resources/img/cactusA.png")
        self.imgB = pygame.image.load(f"{ptDir}resources/img/cactusB.png")
        self.imgs = [self.imgA, self.imgB]
        # Cactus status vars
        self.x = None # Current X co-ordinate
        self.img = None # Asset image
        self.alive = False # Cactus is buffered
        self.avoided = False # Cactus is infront or behind player
        # Access to main
        self.mainAccess = None

    def ctrl(self) -> int:
        score = 0
        if self.alive == False:
            self.x = self.xSet(store=self.mainAccess.cStore)
            self.mainAccess.cStore.append(self.x)
            self.img = random.choice(self.imgs)
            self.alive = True
            self.avoided = False
            print(f" {white}[{grey}Event{white}] Cactus spawned at {blue}{self.x}{white}")
        elif self.alive == True:
            self.x = self.x - self.mainAccess.scrollSpeed
            self.xUpdate(store=self.mainAccess.cStore)
            if self.avoided == False:
                if self.mainAccess.player.rect.y >= 100 and self.x in range(vw // 4 - 56, vw // 4 + 56):
                    print(f" {white}[{grey}Event{white}] You crashed into a cactus")
                    self.avoided = False
                    self.mainAccess.die()
                if self.x <= 175:
                    self.avoided = True
                    score = 1
            elif self.avoided == True:
                pass
            screenCTRL.blit(self.img, (self.x, vh / 2.08))
            if self.x <= -125:
                self.alive = False
        return int(score) # Returns a 1 or 0
        
    def xSet(self, store: list[int]) -> int:
        if len(store) == 0:
            x = random.randint(700, 1400)
            return x
        if len(store) >= 4:
            store.pop(0)
        if len(store) >= 1:
            while True:
                x = random.randint(700, 1400)
                tooClose = False
                for stored in store:
                    #if abs(x - stored) < 56:
                    if x in range(stored - 70, stored + 150):
                        tooClose = True
                        break
                if not tooClose:
                    return x
    
    def xUpdate(self, store: list[int]):
        store.pop(0)
        store.append(self.x)
        

if __name__ == "__main__":
    try:
        pygame.display.set_icon(pygame.image.load(f"{ptDir}resources/img/trexSmall.png"))
        pygame.display.set_caption(f"PterodactylRun - Build Version {__version__}")
        main().play()
    except KeyboardInterrupt:
        throwErr(errs[1], fatal=True)
else:
    throwErr(errs[2], fatal=True)
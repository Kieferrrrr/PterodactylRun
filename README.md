# PterodactylRun
College Assignment Work for a Games Development Unit
[.GIF OF GAMEPLAY]

# Description - Build Version 1.7.0
PterodactylRun is a blend of FlappyBird and the Chromium Dino Game, the aim of PterodactylRun is to keep the pterodactyl away from the
ground and the hazards that lay on it whilst looking out for T-Rexes to collect. Version 1.7.0 is the best fully working build with 
neat-ish code which i submitted for the college assignment first submission. During the resubmission period of the assignment a 
version 2 will be made to fix and rework errors and bad python practices (becuase theres a few). Version 2 will improve the code,
reduce/remove bugs and include new features. However, 1.7.0 is playable enough to get the idea of the games concept and functionality.

## How To Play
PterodactylRun is very simple to play, tap or hold the space bar to make the pterodactyl fly over cacti and stay off the ground.
When a T-Rex appears you have to fly close to the ground and hit it, hitting a T-Rex is worth 5 points and each cactus and you 
avoid is worth 1 point. Each time you go over 50 points you progress to the next level which increases the speed of the game.

### Clone and Install
```shell
git clone https://github.com/Kieferrrrr/PterodactylRun
cd PterodactylRun
py install-repair.py
```

### Running
```shell
py PterodactylRun.pyw
```

## install-repair.py
PterodactylRun comes with a python file called "install-repair.py", this file is for installing the required modules that Python3 installs
might not come with. The other function of this file is for rebuilding the utility files "config.ini" and "scores.json".


## Minimum Technical Requirements
PterodactylRun was created using a mix of Python 3.9.1 and Python 3.11.3 and it functions fine on both of these versions however the modules
which require installation have minimum Python version requirements. At the time of development the install-repair.py file will install the
versions of the modules specified below. Bearing this in mind, at the time of development you will require a minimum of Python 3.8 to run this
code.

### PyGame 2.5.2
Python >= 3.6

### Requests 2.31.0
Python >= 3.7

### Configparser 6.0.0
Python >= 3.8


## Licensing and Chromium Information
Assets used are from the original Chromium source code which are licensed under the BSD 3-Clause license, this license allows modification
and redistribution of its content aslong as it is published under the same BSD 3-Clause license and no warranty or liability it provided.

### Chromium GitHub Repo
https://github.com/chromium/chromium

### Chromium Licensing Agreement
https://github.com/chromium/chromium/blob/main/LICENSE

### Chromium Dino Game Source Code
https://github.com/chromium/chromium/blob/main/components/neterror/resources/offline.js

### Chromium Dino Game Assets
https://github.com/chromium/chromium/blob/main/components/neterror/resources/images/default_100_percent/offline/100-offline-sprite.png
https://github.com/chromium/chromium/blob/main/components/neterror/resources/images/default_200_percent/offline/200-offline-sprite.png

### Information About the Chromium Dino Game
https://blog.google/products/chrome/chrome-dino/

### Information About the BSD 3-Clause License
https://choosealicense.com/licenses/bsd-3-clause/
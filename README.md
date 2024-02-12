# PterodactylRun
College Assignment Work for a Games Development Unit
[.GIF OF GAMEPLAY]

# Description - Build Version 1.0.5
PterodactylRun is a blend of FlappyBird and the Chromium Dino Game, the aim of PterodactylRun is to keep the pterodactyl away from the
ground and the hazards that lay on it whilst looking out for T-Rexes to collect. Version 1.0.5 is the first fully working build with 
neat-ish code which i submitted for the college assignment first submission.

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

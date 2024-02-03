# PterodactylRun
College Assignment Work for a Games Development Unit
[.GIF OF GAMEPLAY]

# Description - Build Version 1.0.4
PterodactylRun is a blend of FlappyBird and the Chrome Dino Game, the aim of PterodactylRun is to keep the pterodactyl away from the
ground and the hazards that lay on it whilst looking out for T-Rexes to collect. 

## How To Play
PterodactylRun is very simple to play, tap or hold the space bar to make the pterodactyl fly over cacti, rocks and stay of the ground.
When a T-Rex appears you have to fly close to the ground and hit it, hitting a T-Rex is worth 5 points and each cactus and rock you 
avoid is worth 1 point. Each time you go over 250 points you progress to the next level which increases the speed of the game.

### Clone and Install
'''shell
git clone https://github.com/Kieferrrrr/PterodactylRun
cd PterodactylRun
py install-repair.py
'''

### Running
'''shell
py PterodactylRun.py
'''

## install-repair.py
PterodactylRun comes with a python file called "install-repair.py", this file is for installing the required modules that Python3 installs
might not come with. The other function of this file is for rebuilding the utility files "config.ini" and "scores.json".
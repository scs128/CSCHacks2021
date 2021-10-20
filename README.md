# A Case of the Monday's (CSC Hacks)

## Project Description
We are working on creating a roguelike-esq game in python utilizing the pygame library. Our game will take place in an office/workplace setting as you fight off droves of zombie co-workers and bosses. Currently just a one room shooter in which you gain points for each zombie you kill, we aim to implement a shop system, randomly generated rooms, bosses, and more in the future.

## Team Information
Scott Sullivan
* Pitt Information Science, 2023
* scs128@pitt.edu
* https://www.linkedin.com/in/scottsullivan01/

Andrew Fiore
* Pitt Health Information Management, 2023
* apf19@pitt.edu
* https://www.linkedin.com/in/andrew-fiore-b24182204/

Matt Shiber
* Pitt Statistics, 2023
* mds168@pitt.edu

## MVP Demo

#### Dependencies
 - [Python](https://www.python.org/) (version 3.7.7 or greater)
 - [Pygame](https://www.pygame.org/wiki/about)

### How to Demo Our Game

1. First, you'll want to start by downloading a version of python 3.7.7 or greater. These can be found [Here](https://www.python.org/downloads/). If you already have python download you can check your version by using ```python --version``` in the terminal.

2. Next, your going to want to download pygame, a library for creating games in python. This can be done using python's built in package installer: pip. Just run the command ```python3 -m pip install -U pygame --user``` in the terminal to download it. You can test if its download by running an included example like so, ```python3 -m pygame.examples.aliens```. 

    If you do not have pip installed with your version of python, you can use any of the ways listed [Here](https://pip.pypa.io/en/stable/installation/#ensurepip) to install pip on your device.

3. Now that you have the dependencies downloaded, all you have to do is clone our [repository](https://github.com/scs128/CSCHacks2021) and run ```Rogue.py``` in the terminal.

### Known Bugs
* Zombie collision with objects in the room is very iffy, sometimes teleporting to other sides of the object. We are currently working on this.
* Sometimes when player is hit by a zombie near a wall the character will teleport across the room. Also currently working to fix this since they come from the same logic we used for collision at first.
* Zombies do not collide with eachother, this isn't a bug we just have not implemented collision between zombies yet.

## Feedback

If you have demo'd the current state of our game and have any feedback on what we've done, suggestions on what we could do, or something you think would be cool, we'd love to hear it! You can leave all feedback and suggestions [in this google form](https://forms.gle/ZvYj9mZQgRrRbkNv7), and we greatly appreciate you taking the time to play our game and responding!

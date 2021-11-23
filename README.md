mGameController
===============

Provides the ability to get control inputs from game devices in Assetto Corsa

mGameController 0.6

GitHub Page: https://github.com/thedixieflatline/mGameController

mGameController an app for the game Assetto Corsa.

Provides the ability to get control inputs from game devices in Assetto Corsa

App developed by David Trenear


Please submit bugs or requests to the Assetto Corsa forum

http://www.assettocorsa.net/forum/index.php


You will need to use the Pygame I have supplied in the source as it is compiled to run in Python 3.3


To activate copy mGameController folder to C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python



This app is more of a tutorial on how to do this. I have developed this for something I am working on in my own Assetto Corsa apps.

I thought other app developers would appreciate knowing how to do this and perhaps even use the technique.

I will continue to develop this into a more generic class to handle a lot of this so developers can just plug and go on more easily integrate it into their own work if they wish.
If there is a lot of interest I might even look at adding in serial device support in the future

This code is setup to be a demo and also I have combined some logic together rather than split it all up to make it easier to read

Also some of the processing in the main loop could be moved out and some values stored on start up and not updated every frame

Again this was for readability and to make it easier to follow as well as to show beginners how to handle the inputs and how to scan for and work changes to capabilities of using different devices



I have commented throughout but the best place to start the tutorial from is the acUpdate function near the bottom

First read the comments in acUpdate that explain the 2 ways to get inputs and the pros and cons and features of each method

Then go and look at the 2 different class descriptions.
Start with class GameController and then read class DisplayClass

Take note of what happens when each class is initialized and the secondary init of DisplayClass
DisplayClass also contains the 2 functions that run the program and do all of the work



Pygame docs online here
http://www.pygame.org/docs/   

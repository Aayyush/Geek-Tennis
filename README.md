# Introduction 
Geek Tennis is a simple math trivia based game that uses the scoring mechanism used in tennis. 

# Design Document 
Link: https://docs.google.com/document/d/1ePfLg7rh5XdB3AfLKPVsJC5AKqsdLpQo2Ag_X8UiFrs/edit?usp=sharing

# Usage 
1. Setup a virtual environment.
2. Install dependencies using pip install -r requirements.txt 
3. Add cocos2d-0.6.7 to the PYTHONPATH using the command export PYTHONPATH="$PYTHONPATH:<path to cocos2d-0.6.7>"
4. Run python game_gui.py to the run the GUI version of the game and python game_cli.py to run the command line version. 

# Design 
This project is designed into 3 main parts. 

### Game Engine
This game engine uses the game_states.txt and game_transitions.txt to build the DFA for the game. This game engine can 
build any DFA given correct dat ain the states and transitions file. 

### Game 
The game object handles all the information regarding a game session. This is the model of the game and can be used to 
build other interfaces on top of it. 

### GUI
This comprises of a collection of layer objects that show a simple UI using cocos2d framework. 

# Dependencies 
1. Cocos2d
2. Pyglet 

# Contributors 
Aayush Gupta
Peniel Abebe 
Swarnim Bhandari 

# Notes 
Due to the resolution of OS x, the game does not span the entire screen which is a bug on pyglet. 
In order to solve this issue, run the patch using the command:

patch < osx_hidpi.patch -d <root-directory>/venv/lib/python3.6/site-packages/pyglet-1.4.3-py3.6.egg/pyglet/gl

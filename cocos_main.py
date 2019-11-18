# TODO: Refactor 

import cocos 
from cocos.text import Label 
from cocos import scene 
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.menu import Menu, MenuItem, CENTER
from cocos.scenes import FadeTransition
from cocos.scene import Scene

from pyglet.window.key import symbol_string

from game import GameDifficulty, Game
from game_engine import GameEngine

from threading import Thread
from question_generator import Question

import time

playerName = ""
difficultyLevel = None 
game = None

GAME_STATES_FILENAME = "game_states.txt"
GAME_TRANSITIONS_FILENAME = "game_transitions.txt"


"""
Initial Screen when the game is started. 
Takes the user's name as input and transitions to the next Layer. 
"""
class IntroductionLayer(ColorLayer):
    is_event_handler = True
    
    def __init__(self):
        super(IntroductionLayer, self).__init__(0xBF907A, 0x806052, 0xFFC0A3, 0x403029)

        self.player_name = ''

        self.game_name_label = Label(
            "Geek Tennis",
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.player_name_label = Label(
            "Enter your name: ",
            font_name = "Times New Roman",
            font_size = 20, 
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.instruction_label = Label(
            "Press enter when you are done!",
            font_name = "Times New Roman",
            font_size = 15,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.player_name_label.position = director._window_virtual_width/2, director._window_virtual_height/2
        self.game_name_label.position = director._window_virtual_width/2, director._window_virtual_height/2 + 50
        self.instruction_label.position = director._window_virtual_width/2, director._window_virtual_height/2 + 100

        self.show_intro_layer() 
    
    def show_intro_layer(self):
        self.add(self.game_name_label)
        self.add(self.player_name_label)
        self.add(self.instruction_label)
    
    def update_player_name(self):
        self.player_name_label.element.text = "Enter your name: " + self.player_name
    
    def on_key_press(self, key, modifiers):
        char_key = symbol_string(key)
        print(char_key)
        if char_key == "ENTER":
            print("Transition to next layer with the username.")
            global playerName
            playerName = self.player_name
            director.replace(FadeTransition(Scene(DifficultyLayer())))

        elif 'A' <= char_key <= 'z':
            self.player_name += char_key 
            self.update_player_name()
        
"""
After the user enters his/her name, this Layer is displayed which shows a menu to 
choose the game difficulty. 
"""
class DifficultyLayer(Menu):
    is_event_handler = True

    def __init__(self):
        super(DifficultyLayer, self).__init__("Choose Difficulty")

        self.menu_halign = CENTER 
        self.menu_valign = CENTER 

        menu_items = [
            (MenuItem("Easy", self.easy_difficulty)),
            (MenuItem("Medium", self.medium_difficulty)),
            (MenuItem("Hard", self.hard_difficulty)),
        ]

        self.create_menu(menu_items)
    
    def easy_difficulty(self):
        print("Easy")
        global difficultyLevel
        difficultyLevel = GameDifficulty.Easy
        self.transition_next_scene()

    def medium_difficulty(self):
        print("Medium")
        global difficultyLevel
        difficultyLevel = GameDifficulty.Medium
        self.transition_next_scene()

    def hard_difficulty(self):
        print("Hard")
        global difficultyLevel
        difficultyLevel = GameDifficulty.Hard
        self.transition_next_scene()
    
    def transition_next_scene(self):
        print("Next Scene")
        print("Player Name: {} Difficulty: {}".format(playerName, difficultyLevel))
        director.replace(FadeTransition(Scene(GameScreen())))
        print("Game Initialized")

"""
This is the main game screen which displays a timer and the question 
with options to choose from. 

This screen also has the score board. 
"""
class GameScreen(ColorLayer):
    is_event_handler = True 

    def __init__(self):
        super(GameScreen, self).__init__(0xBF907A, 0x806052, 0xFFC0A3, 0x403029)
    
        self.is_timer_done = False 
        self.game = Game(
            game_engine = GameEngine.BuildGameEngineFromStatesAndTransitions(GAME_STATES_FILENAME, GAME_TRANSITIONS_FILENAME),
            player_name = playerName,
            difficulty_level = difficultyLevel
        )

        self.timer_label = Label(
            "00", 
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.question_label = Label(
            "Question Text",
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.timer_label.position = (director._window_virtual_width/10)*9, director._window_virtual_height/10
        self.question_label.position = director._window_virtual_width/2, director._window_virtual_height/2
    
        self.add(self.timer_label)
        self.add(self.question_label)

        # Use the game object to populate quesiton and timer field. 
        self.question = Question(2, 3, '+', 10)
    
        self.question_label.element.text = str(self.game.get_question())
        # Start the timer at the end 
        # Set the label to qustion time. 
        self.timer_label.element.text = self.format_time(self.question.time)

        Thread(target=self.question_timer, args=[self.question.time]).start()

        # Lazy wait until the timer is done. 
        while self.is_timer_done: continue

        # Update the global game object. 
        global game 
        game = self.game

        # director.replace(FadeTransition(Scene(TimeLimitExceeded())))

    def question_timer(self, timer_duration):
        a = 0
        while a < timer_duration:
            # Set 1 second timer and update the timer.  
            a += 1
            self.update_timer()
            time.sleep(1)
        self.is_timer_done = True 
                
    def update_question(self):
        pass
        
    def format_time(self, t):
        return "{}".format(t)

    def update_timer(self):
        self.timer_label.element.text  = self.format_time(self.question.time)

"""
This layer is shown the user exceeds the time limit on the question.
"""     
class TimeLimitExceeded(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(GameScreen, self).__init__(0xBF907A, 0x806052, 0xFFC0A3, 0x403029)
   
        # Retrieve the global quesiton 
        self.game = game 
        self.message_label =  Label(
            "You are out of time!! ", 
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.info_label = Label(
            "Score: {}".format(self.game.get_current_state()), 
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.next_quesiton_label = Label(
            "Press ENTER to proceed to your next challenge", 
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        
        self.message_label.position = director._window_virtual_width/2, director._window_virtual_height/2 - 50
        self.info_label.position = director._window_virtual_width/2, director._window_virtual_height/2
        self.next_quesiton_label.position = director._window_virtual_width/2, director._window_virtual_height/2 + 50

        self.add(self.message_label)
        self.add(self.info_label)
        self.add(self.next_quesiton_label)

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "ENTER":
            # Move back to game string by updating the next question. 
            print("Moving on to next question")
            director.replace(FadeTransition(Scene(GameScreen())))

# Starting off the cocos2d application
director.init(
    autoscale = True, 
    caption = "Geek Tennis"
)
director.run(
    scene.Scene(
        IntroductionLayer()
    )
)
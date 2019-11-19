# TODO: Refactor 

import sys
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

from threading import Thread, Timer
from question_generator import Question

import time

from cocos.actions import IntervalAction
from cocos.actions.interval_actions import MoveTo
from cocos import cocosnode

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
        
class UpdateTimerAction(IntervalAction):
    
    def __init__(self, duration):
        super(UpdateTimerAction, self).__init__()
        self.duration  = duration
    
    def update(self, t):
        """
        t is from 0 to 1 which evenly maps out the time interval 
        """
        self.target.element.text = str(self.duration - int(t*self.duration))
        
        
"""
This is the main game screen which displays a timer and the question 
with options to choose from. 

This screen also has the score board. 
"""
class GameScreen(ColorLayer):
    is_event_handler = True 

    def __init__(self):
        super(GameScreen, self).__init__(0xBF907A, 0x806052, 0xFFC0A3, 0x403029)

        # Placeholders
        self.answer = ""
        self.question = None 

        # Initialize game
        self.game = Game(
            game_engine = GameEngine.BuildGameEngineFromStatesAndTransitions(GAME_STATES_FILENAME, GAME_TRANSITIONS_FILENAME),
            player_name = playerName,
            difficulty_level = difficultyLevel
        )

        # Create required labels. 
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

        self.answer_label =  Label(
            "Answer Text",
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.score_board_label = Label(
            "Score: ",
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.instruction_label = Label(
            "Press Enter to submit answer!",
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.timer_label.position = (director._window_virtual_width/10)*9, director._window_virtual_height/10
        self.question_label.position = director._window_virtual_width/2, director._window_virtual_height/2
        self.answer_label.position = director._window_virtual_width/2, director._window_virtual_height/2 - 50
        self.score_board_label.position = director._window_virtual_width/10, director._window_virtual_height/10
        self.instruction_label.position = director._window_virtual_width/2, (director._window_virtual_height/10)*9

        self.add(self.instruction_label)
        self.add(self.timer_label)
        self.add(self.question_label)
        self.add(self.score_board_label)
        self.add(self.answer_label)

        self.display_question()
    
    def is_timer_done(self, callback, *args, **kwargs):
        if self.timer_label.element.text == '0':
            self.handle_answer()
    
    def display_question(self):
        # Reinitialize answer to empty string. 
        self.answer = ""
        self.answer_label.element.text = "_"

        self.question = self.game.get_question()
        self.question_label.element.text = str(self.question)
        self.timer_label.element.text = str(self.question.time)

        # Schedule callback to check for timer every second.
        self.schedule_interval(callback = self.is_timer_done, interval = 1)

        # Add action for timer. 
        self.timer_label.do(UpdateTimerAction(self.question.time))    
    
    def handle_answer(self):
        if self.game.submit_answer(int(self.answer)):
            print("Correct Answer")
        else:
            print("Incorrect Answer")
        
        # Update Score board. 
        self.score_board_label.element.text = " Score: {}".format(self.game.get_current_state())

        # If not game over, continue with next quesiton. 
        if not self.game.is_game_over():
            self.display_question()
        else:
            # Move to next screen with score. 
            director.replace(FadeTransition(Scene(ScoreBoardScreen())))

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "ENTER":
            self.handle_answer()
        else:
            print(key - ord('0'))
            self.answer += chr(key)
            self.answer_label.element.text = self.answer
    
    def on_exit(self):
        global game
        game = self.game
        super(GameScreen, self).on_exit()



class ScoreBoardScreen(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(ScoreBoardScreen, self).__init__(0xBF907A, 0x806052, 0xFFC0A3, 0x403029)
   
        self.score_label = Label(
            "Score {}".format(game.get_current_state()), 
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
            )
        
        self.instruction_label = Label(
            "Press Enter to Exit.", 
            font_name = "Times New Roman",
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
            )
        
        self.score_label.position = director._window_virtual_width/2, director._window_virtual_height/2
        self.instruction_label.position = director._window_virtual_width/2, director._window_virtual_height/2 - 100

        self.add(self.score_label)
        self.add(self.instruction_label)

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "ENTER":
            sys.exit()
            
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
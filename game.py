import enum
from game_engine import Action
from question_generator import QuestionGenerator, GameDifficulty

"""
Game object that tracks all the information about a game session. 
"""
class Game:
    def __init__(self, game_engine, player_name, difficulty_level = GameDifficulty.Easy):
        self.player_name = player_name
        self.game_engine = game_engine
        self.question_generator = QuestionGenerator(difficulty=difficulty_level)
        self.curr_question = None
    
    def is_game_over(self):
        return self.game_engine.current.is_end_state()
    
    def get_question(self):
        self.curr_question = self.question_generator.generate_question()
        return self.curr_question
    
    def submit_answer(self, answer):
        is_correct = False
        if self.curr_question.get_answer() == int(answer):
            is_correct = True
            self.game_engine.execute_action(Action.Win)
        else:
            self.game_engine.execute_action(Action.Loose)
        return is_correct
    
    def get_current_state(self):
        return str(self.game_engine.current)
    


    

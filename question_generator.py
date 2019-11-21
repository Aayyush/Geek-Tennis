import random
import enum

class GameDifficulty(enum.Enum):
    Easy = 1
    Medium = 2 
    Hard = 3 

"""
Question object. 
Specifies timer for the question. 
"""
class Question:
    def __init__(self, operand_1, operand_2, operation, time):
        self.operand_1 = int(operand_1)
        self.operand_2 = int(operand_2)
        self.operation = operation 
        self.time = time
    
    def _calculate_answer(self):
        if self.operation == '+':
            return self.operand_1 + self.operand_2
        elif self.operation == '-':
            return self.operand_1 - self.operand_2
        elif self.operation == '*':
            return self.operand_1*self.operand_2
        elif self.operation == '/':
            return self.operand_1//self.operand_2
        elif self.operation == '%':
            return self.operand_1 % self.operand_2
    
    def get_answer(self):
        return self._calculate_answer()
    
    def __str__(self):
        return "{} {} {}".format(self.operand_1, self.operation, self.operand_2)
    
"""
Generates Question object based on difficulty set by the user. 
"""
class QuestionGenerator:
    def __init__(self, difficulty = GameDifficulty.Easy):
        self.difficulty = difficulty
        self.difficulty_operand_length_mapping = {
            GameDifficulty.Easy: 2,
            GameDifficulty.Medium: 3, 
            GameDifficulty.Hard: 4
        }

        self.difficulty_operator_mapping = {
            GameDifficulty.Easy: ['+', '-'],
            GameDifficulty.Medium: ['+', '-', '/', '*'],
            GameDifficulty.Hard: ['*', '/', '%']
        }

        self.difficulty_time_mapping = {
            GameDifficulty.Easy: 15,
            GameDifficulty.Medium: 8,
            GameDifficulty.Hard: 5
        }

    def generate_question(self):
        operand_length = self.difficulty_operand_length_mapping[GameDifficulty(self.difficulty)]
        operand_1 = random.randint(10**(operand_length-1), 10**(operand_length))
        operand_2 = random.randint(10**(operand_length-1), 10**(operand_length))
        if operand_2 > operand_1:
            operand_1, operand_2 = operand_2, operand_1
            
        operation = random.choice(self.difficulty_operator_mapping[self.difficulty])

        return Question(operand_1, operand_2, operation, self.difficulty_time_mapping[self.difficulty])
        

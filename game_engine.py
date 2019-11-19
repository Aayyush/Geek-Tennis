import enum 
from cutom_exceptions import *

class Action(enum.Enum):
    Win = 1
    Loose = 2 

"""
StateNode represents individual nodes in the DFA. 
Transitions for win and loose point. 
"""
class StateNode:
    def __init__(self, name):
        self.name = name
        self.win = None
        self.loose = None
    
    def is_start_state(self):
        return self.name == "start"
    
    def is_end_state(self):
        return self.name == "win" or self.name == "loose"
    
    def __str__(self):
        return self.name

"""
GameEngine uses the game_states.txt and game_transitions.txt to load up the DFA. 
The game uses this engine to track the user's state at any time. 
"""
class GameEngine:
    def __init__(self, start):
        self.start = start
        self.current = start 

    @classmethod
    def BuildGameEngineFromStatesAndTransitions(cls, game_state_filename, game_transition_filename):
        # Build a map from the name to the State
        state_map = {}
        with open(game_state_filename) as fd:
            for state in fd:
                state_map[state.strip()] = StateNode(name = state.strip())
        
        with open(game_transition_filename) as fd:
            for transition in fd:
                state_1, action, state_2 = transition.strip().split(' ')
                if state_1 not in state_map or state_2 not in state_map:
                    raise InvalidStateException()
                
                if action == 'w':
                    state_map[state_1].win = state_map[state_2]
                elif action == 'l':
                    state_map[state_1].loose = state_map[state_2]
                else:
                    raise InvalidActionException()
        return GameEngine(start = state_map['start'])
    
    def execute_action(self, action):
        if action == Action.Win:
            self.current = self.current.win
        elif action == Action.Loose:
            self.current = self.current.loose
    

if __name__ == '__main__':
    game_engine = GameEngine.BuildGameEngineFromStatesAndTransitions("game_states.txt", "game_transitions.txt")
    print()
    
from game import Game, GameDifficulty
from game_engine import GameEngine

from threading import Thread
import time

GAME_STATES_FILENAME = "game_states.txt"
GAME_TRANSITIONS_FILENAME = "game_transitions.txt"

def question_timer(t):
    
    for i in range(t):
        print("Time: {}\r\n".format(i))
        time.sleep(1)
    
def main():
    while True:
        user_name = input("Name: ").strip()
        if user_name.isalpha():
            print()
            break 
        print("Invalid username. Name can only consist of alphabets.")

    while True:
        while True:
            try:
                difficulty = int(input("Choose difficulty:\n\t1. Easy\n\t2. Medium\n\t3. Hard\n"))
            except ValueError:
                print("Input can only be integer. Please try again!")
                continue
            
            if 0 < difficulty < 4:
                break
            print("Invalid choice. Please choose a number from 1 to 3.")
        
        game = Game(
            game_engine = GameEngine.BuildGameEngineFromStatesAndTransitions(GAME_STATES_FILENAME, GAME_TRANSITIONS_FILENAME),
            player_name = user_name,
            difficulty_level = difficulty
            )
        
        print("-"*20 + "Starting the Game" + "-"*20)

        while not game.is_game_over():
            
            curr_question = game.get_question()
            timer = curr_question.time

            # Start timer. 
            Thread(target = question_timer, args= [timer]).start()

            while True:
                try:
                    answer = int(input(curr_question))
                except ValueError:
                    print("Invalid Input. Answers can only be integers")
                    continue
                
                
                
                if timer >= 0 and game.submit_answer(answer): # Correct.
                    print("Good one!")
                else:
                    print("You missed it! :(")
                print("Score: {}".format(game.get_current_state()))
                break
            print()
        
        # Game is over.
        if game.get_current_state() == 'win':
            print("Congratulations!! You won.")
        else:
            print("Better luck next time :(")
        
        while True:
            play_again = input("Play again(y/n)?")
            if play_again == 'y' or play_again == 'n':
                break
            print("Invalid Choice. Press 'y' for Yes and 'n' for No")

        if play_again == 'n':
            print("-"*20 + "Ending the Game" + "-"*20)
            break
        print()
    print("Thank you for playing :)")

if __name__ == '__main__':
    main()
    
        
                    
                


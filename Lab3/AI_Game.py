#To implement the game we ask user for input:
#   R - Rock
#   P - Paper
#   S - Scissors
import random

def getUserChoice():
    while True:
        user_input = input("Enter your choice (R, P, or S): ").upper()  # Convert to uppercase for case-insensitivity
        if user_input in ['R', 'P', 'S']:
            return user_input
        else:
            print("Invalid input. Please enter R, P, or S.")

def play_game ():
    user_name = input("Let's play a game of Rock Paper Scissors. To begin, please enter players name: ")

# 1. Display the rules
    print('''               RULES: 
          1. You will be asked to enter a letter
                R - Rock
                P - Paper
                S - Scissors
          2. Once your choice is selected, the AI make a random choice
          3. The results of the choices will be displayed
          4. Best 2/3 wins (Ties don't count)
                        Good Luck!!  ''')
# 2. Start the game
    user_score = 0
    AI_score = 0
    game_over = False

    while game_over == False:
        user_choice = getUserChoice()
        AI_Choice = random.choice(['R', 'P', 'S'])
        

        if user_choice == AI_Choice:
            print("It's a tie!")

        elif user_choice == 'R' and AI_Choice == 'S':
            print(f"{user_name} wins! Rock beats Scissors.")
            user_score += 1
        elif user_choice == 'P' and AI_Choice == 'R':
            print(f"{user_name} wins! Paper beats Rock.")
            user_score += 1
        elif user_choice == 'S' and AI_Choice == 'P':
            print(f"{user_name} wins! Scissors beats Paper.")
            user_score += 1

        elif user_choice == 'R' and AI_Choice == 'P':
            print("AI wins! Paper beats Rock.")
            AI_score += 1
        elif user_choice == 'P' and AI_Choice == 'S':
            print("AI wins! Scissors beats Paper.")
            AI_score += 1
        elif user_choice == 'S' and AI_Choice == 'R':
            print("AI wins! Rock beats Scissors.")
            AI_score += 1


        print(f"{user_name}: {user_score} | AI: {AI_score}")

        if user_score == 2 or AI_score == 2:
            game_over = True

    # Display the final result
    if user_score > AI_score:
        print(f"{user_name} wins the game!")
    elif AI_score > user_score:
        print("AI wins the game!")
    else:
        print("It's a tie in the end!")

play_game()
        
#This pygame is implementing the AI_Game.py script 
#it displays the results as text in a game window

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors") #sets the name of the window

# Set up fonts
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    user_name = input("Let's play a game of Rock Paper Scissors. To begin, please enter player's name: ")

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw background
        screen.fill(WHITE)

        # Display rules
        draw_text("RULES:", WIDTH // 2, 50)
        draw_text("1. Choose Rock (R), Paper (P), or Scissors (S)", WIDTH // 2, 100)
        draw_text("2. AI will make a random choice", WIDTH // 2, 140)
        draw_text("3. Results will be displayed", WIDTH // 2, 180)
        draw_text("4. First to 2 wins (Ties don't count)", WIDTH // 2, 220)
        draw_text("Good Luck, " + user_name + "!", WIDTH // 2, 300)

        pygame.display.flip()

        # Wait for user to press a key to start the game
        pygame.time.delay(1000)
        pygame.event.clear()
        pygame.event.wait()

        # Start the game
        user_score = 0
        ai_score = 0
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Get user choice
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                user_choice = 'R'
            elif keys[pygame.K_p]:
                user_choice = 'P'
            elif keys[pygame.K_s]:
                user_choice = 'S'
            else:
                continue

            # Get AI choice
            ai_choice = random.choice(['R', 'P', 'S'])

            # Determine winner
            if user_choice == ai_choice:
                result = "It's a tie!"
            elif (user_choice == 'R' and ai_choice == 'S') or \
                 (user_choice == 'P' and ai_choice == 'R') or \
                 (user_choice == 'S' and ai_choice == 'P'):
                result = f"{user_name} wins! {user_choice} beats {ai_choice}."
                user_score += 1
            else:
                result = f"AI wins! {ai_choice} beats {user_choice}."
                ai_score += 1

            # Display result
            screen.fill(WHITE)
            draw_text(result, WIDTH // 2, HEIGHT // 2)
            draw_text(f"{user_name}: {user_score} | AI: {ai_score}", WIDTH // 2, HEIGHT // 2 + 50)

            pygame.display.flip()
            pygame.time.delay(2000)

            # Check for game over
            if user_score == 2 or ai_score == 2:
                game_over = True

        # Display final result
        screen.fill(WHITE)
        if user_score > ai_score:
            draw_text(f"{user_name} wins the game!", WIDTH // 2, HEIGHT // 2)
        elif ai_score > user_score:
            draw_text("AI wins the game!", WIDTH // 2, HEIGHT // 2)
        else:
            draw_text("It's a tie in the end!", WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()
        pygame.time.delay(3000)

if __name__ == "__main__":
    main()

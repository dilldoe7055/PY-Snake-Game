import pygame
import sys
import time
import random
import csv
import matplotlib.pyplot as plt

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont(None, 30)

def show_start_screen():
    window.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    title_rect = title_text.get_rect(center=(window_width/2, window_height/4))
    window.blit(title_text, title_rect)

    inst_text1 = font.render("Use arrow keys to move the snake", True, WHITE)
    inst_rect1 = inst_text1.get_rect(center=(window_width/2, window_height/2))
    window.blit(inst_text1, inst_rect1)
   
    inst_text2 = font.render("Avoid hitting the walls or yourself", True, WHITE)
    inst_rect2 = inst_text2.get_rect(center=(window_width/2, window_height/2 + 30))
    window.blit(inst_text2, inst_rect2)
   
    inst_text3 = font.render("Eat green fruits to grow and score points", True, WHITE)
    inst_rect3 = inst_text3.get_rect(center=(window_width/2, window_height/2 + 60))
    window.blit(inst_text3, inst_rect3)
   
    inst_text4 = font.render("Avoid blue fruits, they are poisonous!", True, WHITE)
    inst_rect4 = inst_text4.get_rect(center=(window_width/2, window_height/2 + 90))
    window.blit(inst_text4, inst_rect4)
   
    start_button = pygame.Rect(window_width/2 - 100, window_height/2 + 150, 200, 50)
    pygame.draw.rect(window, GREEN, start_button)
    start_button_text = font.render("Start Game", True, BLACK)
    start_button_text_rect = start_button_text.get_rect(center=start_button.center)
    window.blit(start_button_text, start_button_text_rect)

    exit_button = pygame.Rect(window_width/2 - 100, window_height/2 + 220, 200, 50)
    pygame.draw.rect(window, RED, exit_button)
    exit_button_text = font.render("Exit", True, BLACK)
    exit_button_text_rect = exit_button_text.get_rect(center=exit_button.center)
    window.blit(exit_button_text, exit_button_text_rect)

    pygame.display.update()

def start_game():
    snake_speed = 10
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_pos = [random.randrange(1, (window_width//10)) * 10, random.randrange(1, (window_height//10)) * 10]
    dangerous_fruit_pos = [random.randrange(1, (window_width//10)) * 10, random.randrange(1, (window_height//10)) * 10]
    fruit_spawn = True
    dangerous_fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == fruit_pos[0] and snake_pos[1] == fruit_pos[1]:
            score += 1
            snake_speed += 1
            fruit_spawn = False
        else:
            snake_body.pop()
      
        if not fruit_spawn:
            fruit_pos = [random.randrange(1, (window_width//10)) * 10, 
                            random.randrange(1, (window_height//10)) * 10]
            fruit_spawn = True
            dangerous_fruit_pos = [random.randrange(1, (window_width//10)) * 10, random.randrange(1, (window_height//10)) * 10]
            dangerous_fruit_pos = dangerous_fruit_pos*score
            dangerous_fruit_spawn = True
        if not dangerous_fruit_spawn:
            dangerous_fruit_pos = [random.randrange(1, (window_width//10)) * 10, 
                            random.randrange(1, (window_height//10)) * 10]
            dangerous_fruit_spawn = True

        window.fill(BLACK)
        pygame.draw.rect(window, GREEN, pygame.Rect(snake_pos[0], snake_pos[1], 10, 10))
        for pos in snake_body[1:]:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(window, GREEN, pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))
        pygame.draw.rect(window, BLUE, pygame.Rect(dangerous_fruit_pos[0], dangerous_fruit_pos[1], 10, 10))

        if (snake_pos[0] < 0 or snake_pos[0] > window_width-10 or
            snake_pos[1] < 0 or snake_pos[1] > window_height-10):
            game_over(score)

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)

        if snake_pos[0] == dangerous_fruit_pos[0] and snake_pos[1] == dangerous_fruit_pos[1]:
            game_over(score)

        show_score(score, snake_speed)

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

def game_over(score):
    window.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(window_width/2, window_height/4))
    window.blit(game_over_text, game_over_rect)
    score_text = font.render(f"Your Score is: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(window_width/2, window_height/2))
    window.blit(score_text, score_rect)
   
    retry_button = pygame.Rect(window_width/2 - 100, window_height/2 + 100, 200, 50)
    pygame.draw.rect(window, GREEN, retry_button)
    retry_button_text = font.render("Retry", True, BLACK)
    retry_button_text_rect = retry_button_text.get_rect(center=retry_button.center)
    window.blit(retry_button_text, retry_button_text_rect)
   
    show_scoreboard_button = pygame.Rect(window_width/2 - 100, window_height/2 + 170, 200, 50)
    pygame.draw.rect(window, BLUE, show_scoreboard_button)
    show_scoreboard_text = font.render("Show Scoreboard", True, WHITE)
    show_scoreboard_text_rect = show_scoreboard_text.get_rect(center=show_scoreboard_button.center)
    window.blit(show_scoreboard_text, show_scoreboard_text_rect)
   
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse_pos):
                    start_game()
                elif show_scoreboard_button.collidepoint(mouse_pos):
                    show_scoreboard()

def show_score(score, snake_speed):
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))
    speed_text = font.render("Speed: " + str(snake_speed), True, WHITE)
    window.blit(speed_text, (100, 10))

def save_score(name, score):
    try:
        with open("scores.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, score])
        print("Score saved successfully.")
    except Exception as e:
        print("An error occurred while saving the score:", e)


def load_scores():
    try:
        with open("scores.csv", "r") as file:
            reader = csv.reader(file)
            scores = {row[0]: int(row[1]) for row in reader if len(row) == 2}
        return scores
    except FileNotFoundError:
        print("The scores file was not found.")
        return {}
    except Exception as e:
        print("An error occurred while loading the scores:", e)
        return {}

def show_scoreboard():
    scores = load_scores()
    if scores:
        plt.figure(figsize=(8, 6))
        names = list(scores.keys())
        scores_values = list(scores.values())
        plt.barh(names, scores_values, color='green')
        plt.xlabel('Scores')
        plt.ylabel('Players')
        plt.title('Scoreboard')
        plt.tight_layout()
        plt.show()
    else:
        window.fill(BLACK)
        no_scores_text = font.render("No scores yet!", True, WHITE)
        no_scores_rect = no_scores_text.get_rect(center=(window_width/2, window_height/2))
        window.blit(no_scores_text, no_scores_rect)
        pygame.display.update()
        time.sleep(2)
        show_start_screen()

def main():
    show_start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                start_button = pygame.Rect(window_width/2 - 100, window_height/2 + 150, 200, 50)
                exit_button = pygame.Rect(window_width/2 - 100, window_height/2 + 220, 200, 50)
                if start_button.collidepoint(mouse_pos):
                    player_name = input_player_name()
                    start_game()
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def input_player_name():
    player_name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    return player_name
                else:
                    player_name += event.unicode
        window.fill(BLACK)
        name_text = font.render("Enter your name:", True, WHITE)
        window.blit(name_text, (window_width/2 - 100, window_height/2))
        name_input_rect = pygame.Rect(window_width/2 - 100, window_height/2 + 30, 200, 30)
        pygame.draw.rect(window, WHITE, name_input_rect, 2)
        name_input_text = font.render(player_name, True, WHITE)
        window.blit(name_input_text, (name_input_rect.x + 5, name_input_rect.y + 5))
        pygame.display.update()

if __name__ == "__main__":
    main()

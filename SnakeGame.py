import sys

import pygame, random
from pygame.math import Vector2
pygame.init()

game_not_started = True
title_font = pygame.font.Font(None, 50)
start_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

OFFSET = 75


class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x*cell_size,OFFSET + self.position.y*cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, 24)
        y = random.randint(0, 24)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        global game_not_started
        position = self.generate_random_cell()
        if game_not_started:
            while 4 < position.x < 13 and 9 < position.y < 15:
                print("POS CHANGED")
                position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position


class Snake:
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(0,0)
        self.eat_sound = pygame.mixer.Sound("Sounds/Pop Bubbles 2.mp3")
        self.lose_sound = pygame.mixer.Sound("Sounds/Lose.mp3")

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x*cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        if self.direction != Vector2(0, 0):
            self.body = self.body[:-1]
            self.body.insert(0, self.body[0] + self.direction)

    def elongate(self):
        self.body.append(self.body[-1] - self.direction)

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(0, 0)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.highscore = 0
        self.change_select_sound_file = pygame.mixer.Sound("Sounds/ChangeSelection.mp3")
        self.select_sound_file = pygame.mixer.Sound("Sounds/Select.mp3")

    def select_sound(self):
        self.select_sound_file.play()

    def change_select_sound(self):
        self.change_select_sound_file.play()

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        self.snake.update()
        self.check_food_collision()
        self.check_body_collision()
        self.check_edge_collision()

    def elongate(self):
        self.snake.elongate()

    def check_food_collision(self):
        global sound
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.score += 1
            if self.score > self.highscore:
                self.highscore = self.score
            self.snake.elongate()
            if sound != "muted":
                self.snake.eat_sound.play()

    def check_body_collision(self):
        global game_not_started
        for segment in range(1, len(self.snake.body)):
            if self.snake.body[0] == self.snake.body[segment]:
                self.game_over()
                break

    def check_edge_collision(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        global game_not_started, sound
        if not game_not_started:
            self.score = 0
            self.snake.reset()
            self.food.position = self.food.generate_random_pos(self.snake.body)
            game_not_started = True
            if sound != "muted":
                self.snake.lose_sound.play()

sound = ""
game = Game()
food_surface = pygame.image.load("Images/Apple2.jpg.png")
selected_speed = 1
screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("Snake Game")
speed_snake_ms = 100
clock = pygame.time.Clock()
start_screen = True
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, speed_snake_ms)


#GAME LOOP
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and (game_not_started or start_screen)):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not start_screen and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                    game_not_started = False
            if event.key == pygame.K_DOWN:
                if not start_screen and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                    game_not_started = False
            if event.key == pygame.K_RIGHT:
                if not start_screen and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)
                    game_not_started = False
                if start_screen:
                    if selected_speed != 3:
                        selected_speed += 1
                        if sound != "muted":
                            game.change_select_sound()
            if event.key == pygame.K_LEFT:
                if not start_screen and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if start_screen:
                    if selected_speed != 1:
                        selected_speed -= 1
                        if sound != "muted":
                            game.change_select_sound()
            if event.key == pygame.K_KP_ENTER or event.key == pygame.KSCAN_KP_ENTER:
                if selected_speed == 1:
                    speed_snake_ms = 210
                elif selected_speed == 2:
                    speed_snake_ms = 140
                elif selected_speed == 3:
                    speed_snake_ms = 80
                if sound != "muted":
                    game.select_sound()
                pygame.time.set_timer(SNAKE_UPDATE, speed_snake_ms)
                start_screen = False
            if event.key == pygame.K_e and game_not_started:
                start_screen = True
            if event.key == pygame.K_m:
                if sound == "":
                    sound = "muted"
                elif sound == "muted":
                    sound = "unmuted"
                elif sound == "unmuted":
                    sound = "muted"




    # 3. Drawing Objects
    screen.fill(GREEN)
    if not start_screen:
        pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size*number_of_cells + 10, cell_size*number_of_cells + 10), 5)
        game.draw()
        hiscore_surface = score_font.render("Highscore: " + str(game.highscore), True, DARK_GREEN)
        screen.blit(hiscore_surface, (OFFSET + cell_size * number_of_cells - 170, 844))
    elif start_screen:
        start_prompt_surface = start_font.render("Select Game Speed:", True, DARK_GREEN)
        screen.blit(start_prompt_surface, (255, 300))
        slow_rect = pygame.Rect((200, 400, 1, 1))
        medium_rect = pygame.Rect((385, 400, 1, 1))
        fast_rect = pygame.Rect((570, 400, 1, 1))
        slow_rect_off_image = pygame.image.load("Images/ButtonSlowOff.png")
        slow_rect_on_image = pygame.image.load("Images/ButtonSlowOn.png")
        medium_rect_off_image = pygame.image.load("Images/ButtonMediumOff.png")
        medium_rect_on_image = pygame.image.load("Images/ButtonMediumOn.png")
        fast_rect_off_image = pygame.image.load("Images/ButtonFastOff.png")
        fast_rect_on_image = pygame.image.load("Images/ButtonFastOn.png")
        if selected_speed == 1:
            screen.blit(slow_rect_on_image, slow_rect)
        else:
            screen.blit(slow_rect_off_image, slow_rect)
        if selected_speed == 2:
            screen.blit(medium_rect_on_image, medium_rect)
        else:
            screen.blit(medium_rect_off_image, medium_rect)
        if selected_speed == 3:
            screen.blit(fast_rect_on_image, fast_rect)
        else:
            screen.blit(fast_rect_off_image, fast_rect)


    title_surface = title_font.render("Adam's Retro Snake", True, DARK_GREEN)
    screen.blit(title_surface, (15, 28))
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    screen.blit(score_surface, (OFFSET + cell_size*number_of_cells/2 +5, 30))
    escape_surface = score_font.render("Press Esc to Quit Game.", True, DARK_GREEN)
    if game_not_started or start_screen:
        screen.blit(escape_surface, (15, 844))
    sound_rect = pygame.Rect((OFFSET + 750 - 60 + 13, 20, 1, 1))
    sound_on_surface = pygame.image.load("Images/SoundOn.png")
    sound_off_surface = pygame.image.load("Images/SoundOff.png")
    if sound == "":
        screen.blit(sound_on_surface, sound_rect)
    if sound == "muted":
        screen.blit(sound_off_surface, sound_rect)
    elif sound == "unmuted":
        screen.blit(sound_on_surface, sound_rect)

    if game_not_started and not start_screen:
        start_rect = pygame.Rect((200, 400, 1, 1))
        start_surface = pygame.image.load("Images/Play.png")
        prompt_rect = pygame.Rect((200, 485, 1, 1))
        prompt_surface = pygame.image.load("Images/Prompt.png")
        screen.blit(prompt_surface, prompt_rect)
        screen.blit(start_surface, start_rect)
        exit_rect = pygame.Rect((200, 505, 1, 1))
        exit_surface = pygame.image.load("Images/Prompt Exit.png")
        screen.blit(exit_surface, exit_rect)
    pygame.display.update()
    clock.tick(60)
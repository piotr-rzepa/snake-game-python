import collections
import sys
import pygame
import random
import math
from objects import *
from optionsGUI import chosen_options


class Grid:
    def __init__(self, win_width, win_height, block_size):
        self.win_width = win_width
        self.win_height = win_height
        self.block_size = block_size
        self.game_over = False
        self.end_screen = False
        self.display = None
        self.block_width = math.floor(win_width / block_size)
        self.block_height = math.floor(win_height / block_size)
        self.snake = Snake()
        self.apple = Apple(self.block_width, self.block_height, self.block_size)
        self.speedup = SpeedUp(self.block_width, self.block_height, self.block_size)
        self.score = 0
        self.obstacles = []  # lista przechowująca obiekt typu przeszkoda statyczna
        self.obstacles_mov = Obstacle_moving(self.block_size)  # lista przechowująca obiekt typu przeszkoda dynamiczna
        self.obstacles_pos = []  # x,y statycznych przeszkód
        self.custom_opt = None
        self.obst_num = random.randint(5, 15)  # Liczba przeszkód, domyslnie losowana

    # Główny loop gry
    def setup(self):
        self.game_over = False
        self.end_screen = False
        pygame.init()
        pygame.display.set_caption("Snake game by Piotr Rzepkowski")
        self.display = pygame.display.set_mode((self.win_width, self.win_height))

        self.custom_opt = {"Speed up": self.speedup.draw_object, "Grid": self.drawGrid,
                           "Static obstacles": [self.initialize_obst, self.create_obstacles],
                           "Dynamic obstacles": [self.obstacles_mov.draw_snake, self.obstacles_mov.snake_tail,
                                                 self.move_obst]}

        optionList = set(chosen_options).intersection(set(self.custom_opt.keys()))

        # Jezeli w ustawieniach wybralismy liczbe przeszkod, wykrywamy to i sortujemy by byla ostatnia
        if any(str(item).isdigit() for item in chosen_options):
            chosen_options.sort(key=lambda x: str(x).isdigit())
            self.obst_num = chosen_options[-1]  # Ustawiamy liczbe przeszkod
            print(self.obst_num)

        self.snake.head_posx = math.floor(
            random.randint(self.block_width // 3, self.block_width // 2) * self.block_size)
        self.snake.head_posy = math.floor(
            random.randint(self.block_height // 3, self.block_height // 2) * self.block_size)

        self.obstacles_mov.head_posx = 400
        self.obstacles_mov.head_posy = 400

        pygame.display.flip()
        clock = pygame.time.Clock()  # Manipulowanie prędkością węża
        self.snake.velocity = 10

        while not self.game_over:
            while self.end_screen is True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.end_screen = False
                        if event.key == pygame.K_c:
                            self.clear()
                            self.setup()
            if self.game_over is True:
                break
            while self.snake.direction == "LEFT":
                self.update_direction()
                self.snake.head_posx -= self.block_size
                if self.check_collision() or self.check_snks_collision():
                    break
                self.snake.snake_tail()
                self.display.fill((0, 0, 0))
                self.chosen_options(optionList)
                self.eat_powerup(self.snake)
                self.snake.draw_snake(self.display, self.block_size)
                self.check_btwnObj_collision()
                self.apple.draw_object(self.display, self.block_size)
                if "Speed up" in optionList:
                    self.speedup.draw_object(self.display, self.block_size)
                self.display_score()
                pygame.display.update()
                clock.tick(self.snake.velocity)

            while self.snake.direction == "RIGHT":
                self.update_direction()
                self.snake.head_posx += self.block_size
                if self.check_collision() or self.check_snks_collision():
                    break
                self.snake.snake_tail()
                self.display.fill((0, 0, 0))
                self.chosen_options(optionList)
                self.eat_powerup(self.snake)
                self.snake.draw_snake(self.display, self.block_size)
                self.check_btwnObj_collision()
                self.apple.draw_object(self.display, self.block_size)
                if "Speed up" in optionList:
                    self.speedup.draw_object(self.display, self.block_size)
                self.display_score()
                pygame.display.update()
                clock.tick(self.snake.velocity)

            while self.snake.direction == "UP":
                self.update_direction()
                self.snake.head_posy -= self.block_size
                if self.check_collision() or self.check_snks_collision():
                    break
                self.snake.snake_tail()
                self.display.fill((0, 0, 0))
                self.chosen_options(optionList)
                self.eat_powerup(self.snake)
                self.snake.draw_snake(self.display, self.block_size)
                self.check_btwnObj_collision()
                self.apple.draw_object(self.display, self.block_size)
                if "Speed up" in optionList:
                    self.speedup.draw_object(self.display, self.block_size)
                self.display_score()
                pygame.display.update()
                clock.tick(self.snake.velocity)

            while self.snake.direction == "DOWN":
                self.update_direction()
                self.snake.head_posy += self.block_size
                if self.check_collision() or self.check_snks_collision():
                    break
                self.snake.snake_tail()
                self.display.fill((0, 0, 0))
                self.chosen_options(optionList)
                self.eat_powerup(self.snake)
                self.snake.draw_snake(self.display, self.block_size)
                self.check_btwnObj_collision()
                self.apple.draw_object(self.display, self.block_size)
                if "Speed up" in optionList:
                    self.speedup.draw_object(self.display, self.block_size)
                self.display_score()
                pygame.display.update()
                clock.tick(self.snake.velocity)

        pygame.quit()
        quit()

    # Siatka pomocnicza (jedna z opcji ustawień)
    def drawGrid(self):
        for x in range(0, self.win_width, self.block_size):  # draw vertical lines
            pygame.draw.line(self.display, (220, 220, 220), (x, 0), (x, self.win_height))
            for y in range(0, self.win_height, self.block_size):  # draw horizontal lines
                pygame.draw.line(self.display, (220, 220, 220), (0, y), (self.win_width, y))

    def initialize_obst(self):
        for i in range(self.obst_num):
            self.obstacles.append(Obstacle_static(self.block_width, self.block_height, self.block_size))
            self.obstacles[i].draw_object(self.display, self.block_size)
            self.obstacles_pos.append([self.obstacles[i].posx, self.obstacles[i].posy])

    # Zmiana kierunku za każdym razem gdy użytkownik kliknie klawisz kierunku
    def update_direction(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    self.snake.direction = "RIGHT"
                elif event.key == pygame.K_UP:
                    self.snake.direction = "UP"
                elif event.key == pygame.K_DOWN:
                    self.snake.direction = "DOWN"

    # Jeżeli koordynaty x,y jabłka == x,y węża, dodajemy punkt, tworzymy kolejne jabłko, wydłużamy węża
    def eat_powerup(self, obj):
        if obj.head_posx == self.apple.posx and obj.head_posy == self.apple.posy:
            obj.length = obj.length + 1
            self.score = self.score + 1
            self.obstacles_mov.length = self.obstacles_mov.length + 1
            self.apple = Apple(self.block_width, self.block_height, self.block_size)
            self.apple.draw_object(self.display, self.block_size)

        if obj.head_posx == self.speedup.posx and obj.head_posy == self.speedup.posy:
            obj.velocity = obj.velocity * 1.1
            self.score = self.score + 5
            self.speedup = SpeedUp(self.block_width, self.block_height, self.block_size)
            self.speedup.draw_object(self.display, self.block_size)

    # Tworzenie statycznych przeszkód
    def create_obstacles(self):
        for i in range(self.obst_num):
            self.obstacles[i].draw_object(self.display, self.block_size)

    # Wyświetlenie wyniku (Lewy górny róg)
    def display_score(self):
        background = pygame.Surface(self.display.get_size())
        font = pygame.font.Font(None, 36)
        text = font.render("Your score: " + str(self.score), 1, (255, 255, 255))
        textpos = text.get_rect()
        self.display.blit(text, textpos)

    def check_collision(self):
        # Sprawdzanie, czy dotarliśmy do jednego z brzegów ekranu
        if self.snake.head_posx >= self.win_width - 1 or self.snake.head_posx < 0 or self.snake.head_posy >= self.win_height - 1 or self.snake.head_posy < 0:
            self.end_screen = True
            return True
        else:
            # Jeżeli wąż dotknie głową swojego ciała, nastepuje koniec gry
            coll = any(self.snake.snakeList.count(element) > 1 for element in self.snake.snakeList)
            if coll is True:
                self.end_screen = True
                return True
            else:
                # Jeżeli wąż trafi w przeszkodę
                if [self.snake.head_posx, self.snake.head_posy] in self.obstacles_pos:
                    self.end_screen = True
                    return True
                else:
                    return False

    # Sprawdzanie, czy powerUp lub przeszkodza zostały wylosowane na tym samym bloku
    def check_btwnObj_collision(self):
        if [self.apple.posx, self.apple.posy] in self.obstacles_pos:
            self.apple = Apple(self.block_width, self.block_height, self.block_size)
            self.check_btwnObj_collision()
        if [self.speedup.posx, self.speedup.posy] in self.obstacles_pos:
            self.speedup = SpeedUp(self.block_width, self.block_height, self.block_size)
            self.check_btwnObj_collision()
        return

    # Poruszanie sie dynamicznej przeszkody
    def move_obst(self):
        if self.obstacles_mov.direction == "LEFT":
            if self.obstacles_mov.head_posx - 1 < 0 or self.obstacles_mov.head_posy + 1 >= self.win_height - 1 or self.obstacles_mov.head_posy - 1 < 0 or \
                    [self.obstacles_mov.head_posx - self.block_size,
                     self.obstacles_mov.head_posy] in self.obstacles_pos:
                self.obstacles_mov.direction = random.choice(["RIGHT", "UP", "DOWN"])
            else:
                self.obstacles_mov.head_posx -= self.block_size
                self.obstacles_mov.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

        if self.obstacles_mov.direction == "RIGHT":
            if self.obstacles_mov.head_posx + 1 >= self.win_width - 1 or self.obstacles_mov.head_posy + 1 >= self.win_height - 1 or self.obstacles_mov.head_posy - 1 < 0 or \
                    [self.obstacles_mov.head_posx + self.block_size,
                     self.obstacles_mov.head_posy] in self.obstacles_pos:
                self.obstacles_mov.direction = random.choice(["LEFT", "UP", "DOWN"])
            else:
                self.obstacles_mov.head_posx += self.block_size
                self.obstacles_mov.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

        if self.obstacles_mov.direction == "UP":
            if self.obstacles_mov.head_posx + 1 >= self.win_width - 1 or self.obstacles_mov.head_posx - 1 < 0 or self.obstacles_mov.head_posy - 1 < 0 or \
                    [self.obstacles_mov.head_posx,
                     self.obstacles_mov.head_posy - self.block_size] in self.obstacles_pos:
                self.obstacles_mov.direction = random.choice(["LEFT", "RIGHT", "DOWN"])
            else:
                self.obstacles_mov.head_posy -= self.block_size
                self.obstacles_mov.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

        if self.obstacles_mov.direction == "DOWN":
            if self.obstacles_mov.head_posx + 1 >= self.win_width - 1 or self.obstacles_mov.head_posx - 1 < 0 or self.obstacles_mov.head_posy + 1 >= self.win_height or \
                    [self.obstacles_mov.head_posx,
                     self.obstacles_mov.head_posy + self.block_size] in self.obstacles_pos:
                self.obstacles_mov.direction = random.choice(["LEFT", "RIGHT", "UP"])
            else:
                self.obstacles_mov.head_posy += self.block_size
                self.obstacles_mov.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

    # Funkcja zarządzająca wybranymi ustawieniami
    def chosen_options(self, optionList):
        if "Grid" in optionList:
            self.custom_opt["Grid"]()
        if "Static obstacles" in optionList:
            self.custom_opt["Static obstacles"][0]()
            self.custom_opt["Static obstacles"][1]()
        if "Dynamic obstacles" in optionList:
            self.custom_opt["Dynamic obstacles"][0](self.display, self.block_size)
            self.custom_opt["Dynamic obstacles"][1]()
            self.custom_opt["Dynamic obstacles"][2]()

    # Sprawdzanie czy waz zderzyl sie z dynamiczna przeszkoda
    def check_snks_collision(self):
        check = any(item in self.snake.snakeList for item in self.obstacles_mov.snakeList)
        return check

    # Przygotowujemy do ponownej gry
    def clear(self):
        self.end_screen = False
        self.game_over = False
        self.snake.snakeList.clear()
        self.obstacles_mov.snakeList.clear()
        self.obstacles.clear()
        self.display = None
        self.snake = Snake()
        self.obstacles_mov = Obstacle_moving(self.block_size)
        self.apple = Apple(self.block_width, self.block_height, self.block_size)
        self.speedup = SpeedUp(self.block_width, self.block_height, self.block_size)
        self.score = 0
        self.obst_num = random.randint(5, 15)
        self.obstacles_pos.clear()
        self.custom_opt = None



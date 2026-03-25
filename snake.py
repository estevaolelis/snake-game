import pygame, sys, random
from pygame.math import Vector2

pygame.init()

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

class food:
    def __init__(self):
        self.position = self.generate_random_position()

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_position(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        position = Vector2(x, y)
        return position

screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells))
pygame.display.set_caption("Jogo da Cobrinha")

relogio = pygame.time.Clock()

food = food()
food_surface = pygame.image.load("graphics/food.png")

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(GREEN)
    food.draw()

    pygame.display.update()
    relogio.tick(60)
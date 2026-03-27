import random
import pygame
from pygame.math import Vector2

class Comida:
    def __init__(self, corpo_cobra, deslocamento, tamanho_celula, numero_de_celulas):
        self.deslocamento = deslocamento
        self.tamanho_celula = tamanho_celula
        self.numero_de_celulas = numero_de_celulas
        self.superficie_comida = pygame.image.load("Graphics/food.png")
        self.posicao = self.gerar_posicao_aleatoria(corpo_cobra)

    def desenhar(self, screen):
        retangulo_comida = pygame.Rect(
            self.deslocamento + self.posicao.x * self.tamanho_celula,
            self.deslocamento + self.posicao.y * self.tamanho_celula,
            self.tamanho_celula,
            self.tamanho_celula
        )
        screen.blit(self.superficie_comida, retangulo_comida)

    def gerar_celula_aleatoria(self):
        x = random.randint(0, self.numero_de_celulas - 1)
        y = random.randint(0, self.numero_de_celulas - 1)
        return Vector2(x, y)

    def gerar_posicao_aleatoria(self, corpo_cobra):
        posicao = self.gerar_celula_aleatoria()
        while posicao in corpo_cobra:
            posicao = self.gerar_celula_aleatoria()
        return posicao
import pygame
from pygame.math import Vector2

class Cobra:
    def __init__(self):
        self.corpo = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direcao = Vector2(1, 0)
        self.adicionar_segmento = False
        self.som_comer = pygame.mixer.Sound("Sounds/PowerUp2.wav")
        self.som_bater_parede = pygame.mixer.Sound("Sounds/wall.mp3")

    def desenhar(self, screen, deslocamento, tamanho_celula, cor):
        for indice, segmento in enumerate(self.corpo):
            retangulo_segmento = (
                deslocamento + segmento.x * tamanho_celula,
                deslocamento + segmento.y * tamanho_celula,
                tamanho_celula,
                tamanho_celula
            )
            
            if indice == 0:
                cor_cabeca = (53, 61, 34)
                pygame.draw.rect(screen, cor_cabeca, retangulo_segmento, 0, 12) 
            else:
                pygame.draw.rect(screen, cor, retangulo_segmento, 0, 7)

    def atualizar(self):
        self.corpo.insert(0, self.corpo[0] + self.direcao)
        if self.adicionar_segmento:
            self.adicionar_segmento = False
        else:
            self.corpo = self.corpo[:-1]

    def resetar(self):
        self.corpo = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direcao = Vector2(1, 0)
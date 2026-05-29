import random
import pygame
from pygame.math import Vector2

class Comida:
    def __init__(self, corpo_cobra, deslocamento, tamanho_celula, numero_de_celulas):
        """Inicializa a comida, carrega imagem e define posição inicial aleatória.

        Args:
            corpo_cobra: lista de `Vector2` representando o corpo da cobra (para evitar colisão).
            deslocamento: deslocamento (margem) em pixels para desenhar a comida.
            tamanho_celula: tamanho em pixels de cada célula.
            numero_de_celulas: número de células por dimensão do tabuleiro.
        """
        self.deslocamento = deslocamento
        self.tamanho_celula = tamanho_celula
        self.numero_de_celulas = numero_de_celulas
        self.superficie_comida = pygame.image.load("Graphics/food.png")
        self.posicao = self.gerar_posicao_aleatoria(corpo_cobra)

    def desenhar(self, screen):
        """Desenha a imagem da comida na `screen` na posição atual."""
        retangulo_comida = pygame.Rect(
            self.deslocamento + self.posicao.x * self.tamanho_celula,
            self.deslocamento + self.posicao.y * self.tamanho_celula,
            self.tamanho_celula,
            self.tamanho_celula
        )
        screen.blit(self.superficie_comida, retangulo_comida)

    def gerar_celula_aleatoria(self):
        """Gera e retorna uma célula aleatória dentro dos limites do tabuleiro."""
        x = random.randint(0, self.numero_de_celulas - 1)
        y = random.randint(0, self.numero_de_celulas - 1)
        return Vector2(x, y)

    def gerar_posicao_aleatoria(self, corpo_cobra):
        """Gera uma posição aleatória que não esteja ocupada pelo corpo da cobra.

        Args:
            corpo_cobra: lista de posições ocupadas pela cobra para evitar sobreposição.
        Returns:
            `Vector2` com a posição válida gerada.
        """
        posicao = self.gerar_celula_aleatoria()
        while posicao in corpo_cobra:
            posicao = self.gerar_celula_aleatoria()
        return posicao
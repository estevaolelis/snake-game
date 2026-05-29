import pygame
import random
from pygame.math import Vector2

class Buraco:
    def __init__(self, corpo_cobra, numero_de_celulas):
        """Inicializa um buraco/portal em posição aleatória não colidindo com a cobra.

        Args:
            corpo_cobra: lista de posições ocupadas pela cobra para evitar sobreposição.
            numero_de_celulas: número de células por dimensão do tabuleiro.
        """
        self.numero_de_celulas = numero_de_celulas
        self.posicao = self.gerar_posicao_aleatoria(corpo_cobra)

    def gerar_posicao_aleatoria(self, corpo_cobra):
        """Gera e retorna uma posição aleatória que não esteja ocupada pela cobra."""
        while True:
            x = random.randint(0, self.numero_de_celulas - 1)
            y = random.randint(0, self.numero_de_celulas - 1)
            posicao = Vector2(x, y)
            if posicao not in corpo_cobra:
                return posicao

    def desenhar(self, screen, deslocamento, tamanho_celula):
        """Desenha o buraco como uma elipse preta na posição atual."""
        retangulo = pygame.Rect(
            deslocamento + self.posicao.x * tamanho_celula,
            deslocamento + self.posicao.y * tamanho_celula,
            tamanho_celula, tamanho_celula
        )
        pygame.draw.ellipse(screen, (0, 0, 0), retangulo)
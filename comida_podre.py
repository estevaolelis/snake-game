import random
import pygame
from pygame.math import Vector2
import random

class ComidaPodre:
    def __init__(self, corpo_cobra, posicao_comida_boa, posicoes_comidas_podres, deslocamento, tamanho_celula, numero_de_celulas):
        """Inicializa o estado da comida podre e define sua posição inicial segura.

        Args:
            corpo_cobra: lista de Vector2 representando o corpo atual da cobra.
            posicao_comida_boa: Vector2 indicando onde a comida normal está posicionada.
            posicoes_comidas_podres: lista de Vector2 indicando onde as comidas podres já estão posicionadas.
            deslocamento: margem em pixels para o desenho no tabuleiro.
            tamanho_celula: tamanho em pixels de cada célula.
            numero_de_celulas: número de células por dimensão do tabuleiro.
        """
        self.deslocamento = deslocamento
        self.tamanho_celula = tamanho_celula
        self.numero_de_celulas = numero_de_celulas
        
        opcoes_de_imagem = [
            "Graphics/poison1.png",
            "Graphics/poison2.png",
            "Graphics/poison3.png"
        ]
        
        imagem_sorteada = random.choice(opcoes_de_imagem)
        
        imagem_original = pygame.image.load(imagem_sorteada).convert_alpha()
        
        self.superficie_comida = pygame.transform.scale(imagem_original, (32, 32))
        
        self.posicao = self.gerar_posicao_aleatoria(corpo_cobra, posicao_comida_boa, posicoes_comidas_podres)

    def desenhar(self, screen):
        """Desenha a imagem da comida podre na tela.

        Args:
            screen: superfície Pygame onde o elemento será renderizado.
        """
        pos_x = self.deslocamento + self.posicao.x * self.tamanho_celula
        pos_y = self.deslocamento + self.posicao.y * self.tamanho_celula
        
        retangulo_comida = pygame.Rect(pos_x, pos_y, self.tamanho_celula, self.tamanho_celula)
        
        screen.blit(self.superficie_comida, retangulo_comida)

    def gerar_celula_aleatoria(self):
        """Gera uma coordenada Vector2 aleatória dentro dos limites do tabuleiro.

        Returns:
            Vector2: Uma posição aleatória baseada no número de células.
        """
        x = random.randint(0, self.numero_de_celulas - 1)
        y = random.randint(0, self.numero_de_celulas - 1)
        return Vector2(x, y)

    def gerar_posicao_aleatoria(self, corpo_cobra, posicao_comida_boa, posicoes_comidas_podres):
        """Gera uma posição válida que não colida com a cobra nem com a comida boa.

        Args:
            corpo_cobra: lista de Vector2 com os segmentos da cobra.
            posicao_comida_boa: Vector2 da posição atual da comida normal.
            posicoes_comidas_podres: lista de Vector2 das posições atuais das comidas podres.

        Returns:
            Vector2: Uma coordenada segura para posicionar a comida podre.
        """
        posicao = self.gerar_celula_aleatoria()
        while posicao in corpo_cobra or posicao == posicao_comida_boa or posicao in posicoes_comidas_podres:
            posicao = self.gerar_celula_aleatoria()
        return posicao
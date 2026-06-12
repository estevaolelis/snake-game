import pygame
from pygame.math import Vector2

class Cobra:
    def __init__(self, tamanho_celula):
        """Inicializa a cobra com imagens, sons e posição padrão.

        Args:
            tamanho_celula: tamanho em pixels usado para redimensionar as imagens da cobra.
        """
        self.corpo = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direcao = Vector2(1, 0)
        self.adicionar_segmento = False
        self.imagem_cabeca = pygame.image.load("Graphics/Snake_Head.png").convert_alpha()
        self.imagem_corpo = pygame.image.load("Graphics/Snake_Body_Outlined.png").convert_alpha()
        self.imagem_cabeca = pygame.transform.scale(self.imagem_cabeca, (tamanho_celula, tamanho_celula))
        self.imagem_corpo = pygame.transform.scale(self.imagem_corpo, (tamanho_celula, tamanho_celula))
        self.som_comer = pygame.mixer.Sound("Sounds/PowerUp2.wav")
        self.som_bater_parede = pygame.mixer.Sound("Sounds/wall.mp3")
        self.som_comida_podre = pygame.mixer.Sound("Sounds/podre.mp3")
        self.rotacoes = {
            (1, 0): -90,
            (-1, 0): 90,
            (0, 1): 180,
            (0, -1): 0 
        }

    def desenhar(self, screen, deslocamento, tamanho_celula, cor):
        """Desenha a cobra na tela, rotacionando a cabeça conforme direção.

        Args:
            screen: superfície Pygame onde desenhar.
            deslocamento: margem usada para posicionamento.
            tamanho_celula: tamanho em pixels de cada célula.
            cor: cor opcional (não usada diretamente aqui).
        """
        for indice, segmento in enumerate(self.corpo):
            pos_x = deslocamento + segmento.x * tamanho_celula
            pos_y = deslocamento + segmento.y * tamanho_celula
            
            if indice == 0:
                direcao_tupla = (int(self.direcao.x), int(self.direcao.y))
                angulo = self.rotacoes.get(direcao_tupla, 0)
                
                cabeca_rotacionada = pygame.transform.rotate(self.imagem_cabeca, angulo)
                screen.blit(cabeca_rotacionada, (pos_x, pos_y))
            else:
                screen.blit(self.imagem_corpo, (pos_x, pos_y))

    def atualizar(self):
        """Move a cobra na direção atual e gerencia o crescimento.

        Insere uma nova cabeça e remove a cauda a menos que `adicionar_segmento` seja True.
        """
        self.corpo.insert(0, self.corpo[0] + self.direcao)
        if self.adicionar_segmento:
            self.adicionar_segmento = False
        else:
            self.corpo = self.corpo[:-1]

    def resetar(self):
        """Reseta a posição e direção da cobra ao estado inicial."""
        self.corpo = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direcao = Vector2(1, 0)

    def teletransportar(self, nova_posicao):
        """Teletransporta a cobra por um deslocamento preservando sua forma.

        Args:
            nova_posicao: `Vector2` target para a nova posição da cabeça.
        """
        deslocamento = nova_posicao - self.corpo[0]
    
        for i in range(len(self.corpo)):
            self.corpo[i] = self.corpo[i] + deslocamento
import pygame
import sys

class MenuPrincipal:
    def __init__(self, screen):
        """Inicializa o menu principal com os elementos visuais."""
        self.screen = screen
        self.rodando = True
        self.largura = screen.get_width()
        self.altura = screen.get_height()

        try:
            self.fundo = pygame.image.load("Graphics/menu_bg.png").convert()
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
        except FileNotFoundError:
            self.fundo = pygame.Surface((self.largura, self.altura))
            self.fundo.fill((40, 40, 50))

        try:
            imagem_original = pygame.image.load("Graphics/btn_iniciar.png").convert_alpha()
            self.imagem_botao = pygame.transform.smoothscale(imagem_original, (400, 152))
        except FileNotFoundError:
            self.imagem_botao = pygame.Surface((400, 152))
            self.imagem_botao.fill((0, 200, 50))

        pos_x = (self.largura - self.imagem_botao.get_width()) // 2
        pos_y = (self.altura - self.imagem_botao.get_height()) // 2
        self.rect_botao = self.imagem_botao.get_rect(topleft=(pos_x, pos_y))

    def desenhar(self):
        """Renderiza o fundo e o botão na tela."""
        self.screen.blit(self.fundo, (0, 0))
        self.screen.blit(self.imagem_botao, self.rect_botao.topleft)
        pygame.display.update()

    def executar(self):
        """Inicia o loop do menu, aguardando a interação do jogador."""
        clock = pygame.time.Clock()
        
        while self.rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.rect_botao.collidepoint(event.pos):
                            self.rodando = False

            self.desenhar()
            clock.tick(60)
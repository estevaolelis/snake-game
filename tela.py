import pygame

class Tela:
    def __init__(self, screen, tamanho_celula, numero_de_celulas, deslocamento, cor_borda):
        self.screen = screen
        self.tamanho_celula = tamanho_celula
        self.numero_de_celulas = numero_de_celulas
        self.deslocamento = deslocamento
        self.cor_borda = cor_borda
        self.fonte_titulo = pygame.font.Font(None, 60)
        self.fonte_pontuacao = pygame.font.Font(None, 40)

    def desenhar_tabuleiro(self, cor_fase):
        self.screen.fill(cor_fase)

        cor_xadrez = (
            max(0, cor_fase[0] - 10),
            max(0, cor_fase[1] - 10),
            max(0, cor_fase[2] - 10)
        )

        for linha in range(self.numero_de_celulas):
            for coluna in range(self.numero_de_celulas):
                if (linha + coluna) % 2 == 0:
                    retangulo_xadrez = pygame.Rect(
                        self.deslocamento + coluna * self.tamanho_celula,
                        self.deslocamento + linha * self.tamanho_celula,
                        self.tamanho_celula,
                        self.tamanho_celula
                    )
                    pygame.draw.rect(self.screen, cor_xadrez, retangulo_xadrez)

    def desenhar(self, jogo):
        cor_fase = jogo.cores_fases[jogo.fase_atual % len(jogo.cores_fases)]
        self.desenhar_tabuleiro(cor_fase)

        pygame.draw.rect(
            self.screen,
            self.cor_borda,
            (
                self.deslocamento - 5,
                self.deslocamento - 5,
                self.tamanho_celula * self.numero_de_celulas + 10,
                self.tamanho_celula * self.numero_de_celulas + 10,
            ),
            5,
        )

        jogo.desenhar(self.screen, self.deslocamento, self.tamanho_celula, self.cor_borda)

        superficie_titulo = self.fonte_titulo.render("Jogo da Cobrinha", True, self.cor_borda)
        texto_pontuacao = f"Pontuação: {jogo.pontuacao}"
        superficie_pontuacao = self.fonte_pontuacao.render(texto_pontuacao, True, self.cor_borda)

        self.screen.blit(superficie_titulo, (self.deslocamento - 5, 20))
        pos_x_pontuacao = (self.deslocamento + self.tamanho_celula * self.numero_de_celulas) - superficie_pontuacao.get_width()
        self.screen.blit(superficie_pontuacao, (pos_x_pontuacao, 30))
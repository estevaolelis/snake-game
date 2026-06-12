import pygame

class Tela:
    def __init__(self, screen, tamanho_celula, numero_de_celulas, deslocamento, cor_borda):
        """Inicializa a tela do jogo e carrega as fontes arcade."""
        self.screen = screen
        self.tamanho_celula = tamanho_celula
        self.numero_de_celulas = numero_de_celulas
        self.deslocamento = deslocamento
        self.cor_borda = cor_borda
        
        caminho_fonte = "Graphics/arcade.ttf"
        try:
            self.fonte_titulo = pygame.font.Font(caminho_fonte, 60)
            self.fonte_pontuacao = pygame.font.Font(caminho_fonte, 40)
            self.caminho_fonte_popup = caminho_fonte
        except FileNotFoundError:
            self.fonte_titulo = pygame.font.Font(None, 60)
            self.fonte_pontuacao = pygame.font.Font(None, 40)
            self.caminho_fonte_popup = None

    def desenhar_tabuleiro(self, cor_fase):
        """Desenha o tabuleiro quadriculado preenchendo o fundo com a cor da fase."""
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
        """Desenha toda a tela do jogo incluindo tabuleiro, borda e HUD."""
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

        superficie_titulo = self.fonte_titulo.render("Snake Elite", True, self.cor_borda)
        
        texto_pontuacao = f"Pontuacao: {jogo.pontuacao}"
        superficie_pontuacao = self.fonte_pontuacao.render(texto_pontuacao, True, self.cor_borda)
        
        self.screen.blit(superficie_titulo, (self.deslocamento - 5, 25))
        canto_direito = (self.deslocamento + self.tamanho_celula * self.numero_de_celulas)
        pos_x_pontuacao = canto_direito - superficie_pontuacao.get_width()
        self.screen.blit(superficie_pontuacao, (pos_x_pontuacao, 25))
        
        if jogo.estado == "GAME_OVER":
            self.desenhar_popup_recordes(jogo)
        
    def desenhar_popup_recordes(self, jogo):
        """Desenha a tela de fim de jogo e o placar de recordes por cima do tabuleiro."""
        camada_escura = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        camada_escura.fill((0, 0, 0, 210))
        self.screen.blit(camada_escura, (0, 0))

        try:
            fonte_titulo = pygame.font.Font(self.caminho_fonte_popup, 74)
            fonte_normal = pygame.font.Font(self.caminho_fonte_popup, 40)
        except (FileNotFoundError, TypeError):
            fonte_titulo = pygame.font.Font(None, 74)
            fonte_normal = pygame.font.Font(None, 40)
        
        centro_x = self.screen.get_width() // 2
        
        texto_game_over = fonte_titulo.render("GAME OVER!", True, (255, 80, 80))
        retangulo_titulo = texto_game_over.get_rect(center=(centro_x, 150))
        self.screen.blit(texto_game_over, retangulo_titulo)

        y_offset = 260
        texto_recordes = fonte_normal.render("*** MAIORES PONTUACOES ***", True, (255, 215, 0))
        retangulo_recordes = texto_recordes.get_rect(center=(centro_x, y_offset))
        self.screen.blit(texto_recordes, retangulo_recordes)
        
        y_offset += 70
        for i, recorde in enumerate(jogo.gerenciador_recordes.recordes):
            linha = f"{i + 1} . {recorde['nome']} ...... {recorde['pontuacao']}"
            texto_linha = fonte_normal.render(linha, True, (255, 255, 255))
            retangulo_linha = texto_linha.get_rect(center=(centro_x, y_offset))
            self.screen.blit(texto_linha, retangulo_linha)
            y_offset += 50

        if jogo.gerenciador_recordes.eh_novo_recorde(jogo.pontuacao):
            texto_aviso = fonte_normal.render("NOVO RECORDE! Digite seu nickname:", True, (100, 255, 100))
            retangulo_aviso = texto_aviso.get_rect(center=(centro_x, y_offset + 50))
            self.screen.blit(texto_aviso, retangulo_aviso)
            
            tempo = pygame.time.get_ticks()
            cursor = "_" if tempo % 1000 < 500 else " "
            texto_nome = fonte_titulo.render(jogo.nome_input + cursor, True, (255, 255, 255))
            retangulo_nome = texto_nome.get_rect(center=(centro_x, y_offset + 120))
            self.screen.blit(texto_nome, retangulo_nome)
        else:
            texto_aviso = fonte_normal.render("Aperte ENTER para tentar de novo", True, (200, 200, 200))
            retangulo_aviso = texto_aviso.get_rect(center=(centro_x, y_offset + 80))
            self.screen.blit(texto_aviso, retangulo_aviso)
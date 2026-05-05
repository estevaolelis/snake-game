import pygame
import sys
from pygame.math import Vector2
from jogo import Jogo

pygame.init()

fonte_titulo = pygame.font.Font(None, 60)
fonte_pontuacao = pygame.font.Font(None, 40)

VERDE_ESCURO = (43, 51, 24)

tamanho_celula = 30
numero_de_celulas = 25
DESLOCAMENTO = 75

screen = pygame.display.set_mode(
    (2 * DESLOCAMENTO + tamanho_celula * numero_de_celulas,
     2 * DESLOCAMENTO + tamanho_celula * numero_de_celulas)
)

pygame.display.set_caption("Jogo da Cobrinha")
clock = pygame.time.Clock()

jogo = Jogo(DESLOCAMENTO, tamanho_celula, numero_de_celulas)

ATUALIZAR_COBRA = pygame.USEREVENT
pygame.time.set_timer(ATUALIZAR_COBRA, 200)

while True:
    for event in pygame.event.get():
        if event.type == ATUALIZAR_COBRA:
            jogo.atualizar()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if jogo.estado == "PARADO":
                jogo.estado = "RODANDO"

            if event.key == pygame.K_UP and jogo.cobra.direcao != Vector2(0, 1):
                jogo.cobra.direcao = Vector2(0, -1)

            if event.key == pygame.K_DOWN and jogo.cobra.direcao != Vector2(0, -1):
                jogo.cobra.direcao = Vector2(0, 1)

            if event.key == pygame.K_LEFT and jogo.cobra.direcao != Vector2(1, 0):
                jogo.cobra.direcao = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT and jogo.cobra.direcao != Vector2(-1, 0):
                jogo.cobra.direcao = Vector2(1, 0)

    cor_fase = jogo.cores_fases[jogo.fase_atual % len(jogo.cores_fases)]
    screen.fill(cor_fase)

    cor_xadrez = (
        max(0, cor_fase[0] - 10),
        max(0, cor_fase[1] - 10),
        max(0, cor_fase[2] - 10)
    )

    for linha in range(numero_de_celulas):
        for coluna in range(numero_de_celulas):
            if (linha + coluna) % 2 == 0:
                retangulo_xadrez = pygame.Rect(
                    DESLOCAMENTO + coluna * tamanho_celula, 
                    DESLOCAMENTO + linha * tamanho_celula, 
                    tamanho_celula, 
                    tamanho_celula
                )
                pygame.draw.rect(screen, cor_xadrez, retangulo_xadrez)

    pygame.draw.rect(
        screen,
        VERDE_ESCURO,
        (DESLOCAMENTO - 5, DESLOCAMENTO - 5, tamanho_celula * numero_de_celulas + 10, tamanho_celula * numero_de_celulas + 10),
        5
    )

    jogo.desenhar(screen, DESLOCAMENTO, tamanho_celula, VERDE_ESCURO)

    superficie_titulo = fonte_titulo.render("Jogo da Cobrinha", True, VERDE_ESCURO)
    texto_pontuacao = f"Pontuação: {jogo.pontuacao}"
    superficie_pontuacao = fonte_pontuacao.render(texto_pontuacao, True, VERDE_ESCURO)

    screen.blit(superficie_titulo, (DESLOCAMENTO - 5, 20))
    pos_x_pontuacao = (DESLOCAMENTO + tamanho_celula * numero_de_celulas) - superficie_pontuacao.get_width()
    screen.blit(superficie_pontuacao, (pos_x_pontuacao, 30))

    pygame.display.update()
    clock.tick(60)
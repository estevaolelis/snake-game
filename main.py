import pygame
import sys
from pygame.math import Vector2
from jogo import Jogo

pygame.init()

fonte_titulo = pygame.font.Font(None, 60)
fonte_pontuacao = pygame.font.Font(None, 40)

VERDE = (173, 204, 96)
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

superficie_comida = pygame.image.load("Graphics/food.png")

jogo = Jogo(DESLOCAMENTO, tamanho_celula, numero_de_celulas, superficie_comida)

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

    screen.fill(VERDE)

    pygame.draw.rect(
        screen,
        VERDE_ESCURO,
        (DESLOCAMENTO - 5, DESLOCAMENTO - 5, tamanho_celula * numero_de_celulas + 10, tamanho_celula * numero_de_celulas + 10),
        5
    )

    jogo.desenhar(screen, DESLOCAMENTO, tamanho_celula, VERDE_ESCURO)

    superficie_titulo = fonte_titulo.render("Jogo da Cobrinha", True, VERDE_ESCURO)
    superficie_pontuacao = fonte_pontuacao.render(str(jogo.pontuacao), True, VERDE_ESCURO)

    screen.blit(superficie_titulo, (DESLOCAMENTO - 5, 20))
    screen.blit(superficie_pontuacao, (DESLOCAMENTO - 5, DESLOCAMENTO + tamanho_celula * numero_de_celulas + 10))

    pygame.display.update()
    clock.tick(60)
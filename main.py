import pygame
import sys
from pygame.math import Vector2
from jogo import Jogo
from tela import Tela
from menu import MenuPrincipal

pygame.init()

VERDE_ESCURO = (43, 51, 24)

tamanho_celula = 30
numero_de_celulas = 25
DESLOCAMENTO = 75

screen = pygame.display.set_mode(
    (2 * DESLOCAMENTO + tamanho_celula * numero_de_celulas,
     2 * DESLOCAMENTO + tamanho_celula * numero_de_celulas)
)

pygame.display.set_caption("Snake Elite")
menu = MenuPrincipal(screen)
menu.executar()
clock = pygame.time.Clock()

jogo = Jogo(DESLOCAMENTO, tamanho_celula, numero_de_celulas)
tela = Tela(screen, tamanho_celula, numero_de_celulas, DESLOCAMENTO, VERDE_ESCURO)

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
            
            if jogo.estado == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    if jogo.gerenciador_recordes.eh_novo_recorde(jogo.pontuacao):
                        nome_final = jogo.nome_input.ljust(3)[:3].upper()
                        if nome_final.strip() == "":
                            nome_final = "AAA"
                            
                        jogo.gerenciador_recordes.adicionar_recorde(nome_final, jogo.pontuacao)
                    jogo.reiniciar_jogo()
                    
                elif event.key == pygame.K_BACKSPACE:
                    jogo.nome_input = jogo.nome_input[:-1]
                    
                else:
                    if len(jogo.nome_input) < 3 and event.unicode.isalpha():
                        jogo.nome_input += event.unicode.upper()

            else:
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

    tela.desenhar(jogo)

    pygame.display.update()
    clock.tick(60)
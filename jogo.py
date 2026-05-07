import pygame
from cobra import Cobra
from comida import Comida
from buraco import Buraco
from pygame.math import Vector2

class Jogo:
    def __init__(self, deslocamento, tamanho_celula, numero_de_celulas):
        self.cobra = Cobra(tamanho_celula)
        self.comida = Comida(self.cobra.corpo, deslocamento, tamanho_celula, numero_de_celulas)
        self.estado = "RODANDO"
        self.pontuacao = 0
        self.pontuacao_fase = 0
        self.numero_de_celulas = numero_de_celulas
        self.intervalo_atualizacao = 200
        
        self.fase_atual = 0
        self.buraco = None
        self.meta_pontos = 5
        self.cores_fases = [
            (173, 204, 96),
            (75, 139, 190),
            (255, 183, 128),
            (106, 13, 173)
        ]

    def desenhar(self, screen, deslocamento, tamanho_celula, cor_corpo):
        self.comida.desenhar(screen)
        if self.buraco:
            self.buraco.desenhar(screen, deslocamento, tamanho_celula)
            
        self.cobra.desenhar(screen, deslocamento, tamanho_celula, cor_corpo)

    def atualizar(self):
        if self.estado == "RODANDO":
            self.cobra.atualizar()
            self.verificar_colisao_com_comida()
            self.verificar_colisao_com_bordas()
            self.verificar_colisao_com_cauda()
            self.verificar_colisao_com_buraco()

    def verificar_colisao_com_comida(self):
        if self.cobra.corpo[0] == self.comida.posicao:
            self.comida.posicao = self.comida.gerar_posicao_aleatoria(self.cobra.corpo)
            self.cobra.adicionar_segmento = True
            self.pontuacao += 1
            self.pontuacao_fase += 1
            self.cobra.som_comer.play()

            if self.pontuacao_fase >= self.meta_pontos and not self.buraco:
                self.buraco = Buraco(self.cobra.corpo, self.numero_de_celulas)
            self.intervalo_atualizacao = max(60, int(self.intervalo_atualizacao * 0.95))
            pygame.time.set_timer(pygame.USEREVENT, self.intervalo_atualizacao)

    def verificar_colisao_com_buraco(self):
        if self.buraco and self.cobra.corpo[0] == self.buraco.posicao:
            candidatos = []
            origem = self.buraco.posicao
            candidatos.append(origem)

            for r in range(1, 4):
                for dx in range(-r, r + 1):
                    dy = r - abs(dx)
                    candidatos.append(Vector2(origem.x + dx, origem.y + dy))
                    if dy != 0:
                        candidatos.append(Vector2(origem.x + dx, origem.y - dy))

            tentativa = 0
            ultima_candidata = None
            nova_posicao = None
            while tentativa < 300:
                if tentativa < len(candidatos):
                    candidata = candidatos[tentativa]
                else:
                    candidata = self.comida.gerar_celula_aleatoria()

                tentativa += 1
                ultima_candidata = candidata

                if not (0 <= candidata.x < self.numero_de_celulas and 0 <= candidata.y < self.numero_de_celulas):
                    continue

                deslocamento = candidata - self.cobra.corpo[0]
                possiveis = [seg + deslocamento for seg in self.cobra.corpo]

                dentro = all(0 <= p.x < self.numero_de_celulas and 0 <= p.y < self.numero_de_celulas for p in possiveis)
                if not dentro:
                    continue

                proxima_cabeca = possiveis[0] + self.cobra.direcao
                if not (0 <= proxima_cabeca.x < self.numero_de_celulas and 0 <= proxima_cabeca.y < self.numero_de_celulas):
                    continue

                nova_posicao = candidata
                break

            if nova_posicao is None:
                nova_posicao = ultima_candidata if ultima_candidata is not None else origem

            self.cobra.teletransportar(nova_posicao)

            self.fase_atual += 1
            self.buraco = None
            self.pontuacao_fase = 0
            self.comida.posicao = self.comida.gerar_posicao_aleatoria(self.cobra.corpo)

    def avancar_fase(self):
        posicao_nascimento = Vector2(12, 12)
        tamanho_atual = len(self.cobra.corpo)

        novo_corpo = []
        for i in range(tamanho_atual):
            novo_corpo.append(Vector2(posicao_nascimento.x - i, posicao_nascimento.y))

        self.cobra.corpo = novo_corpo
        self.cobra.direcao = Vector2(1, 0)
        self.comida.posicao = self.comida.gerar_posicao_aleatoria(self.cobra.corpo)

    def verificar_colisao_com_bordas(self):
        if self.cobra.corpo[0].x == self.numero_de_celulas or self.cobra.corpo[0].x == -1:
            self.fim_de_jogo()
        if self.cobra.corpo[0].y == self.numero_de_celulas or self.cobra.corpo[0].y == -1:
            self.fim_de_jogo()

    def fim_de_jogo(self):
        self.fase_atual = 0
        self.buraco = None
        self.pontuacao_fase = 0
        self.cobra.resetar()
        self.comida.posicao = self.comida.gerar_posicao_aleatoria(self.cobra.corpo)
        self.estado = "PARADO"
        self.pontuacao = 0
        self.cobra.som_bater_parede.play()
        self.intervalo_atualizacao = 200
        pygame.time.set_timer(pygame.USEREVENT, self.intervalo_atualizacao)

    def verificar_colisao_com_cauda(self):
        corpo_sem_cabeca = self.cobra.corpo[1:]
        if self.cobra.corpo[0] in corpo_sem_cabeca:
            self.fim_de_jogo()
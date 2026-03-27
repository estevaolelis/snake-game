from cobra import Cobra
from comida import Comida

class Jogo:
    def __init__(self, deslocamento, tamanho_celula, numero_de_celulas):
        self.cobra = Cobra()
        self.comida = Comida(self.cobra.corpo, deslocamento, tamanho_celula, numero_de_celulas)
        self.estado = "RODANDO"
        self.pontuacao = 0
        self.numero_de_celulas = numero_de_celulas

    def desenhar(self, screen, deslocamento, tamanho_celula, cor):
        self.comida.desenhar(screen)
        self.cobra.desenhar(screen, deslocamento, tamanho_celula, cor)

    def atualizar(self):
        if self.estado == "RODANDO":
            self.cobra.atualizar()
            self.verificar_colisao_com_comida()
            self.verificar_colisao_com_bordas()
            self.verificar_colisao_com_cauda()

    def verificar_colisao_com_comida(self):
        if self.cobra.corpo[0] == self.comida.posicao:
            self.comida.posicao = self.comida.gerar_posicao_aleatoria(self.cobra.corpo)
            self.cobra.adicionar_segmento = True
            self.pontuacao += 1
            self.cobra.som_comer.play()

    def verificar_colisao_com_bordas(self):
        if self.cobra.corpo[0].x == self.numero_de_celulas or self.cobra.corpo[0].x == -1:
            self.fim_de_jogo()
        if self.cobra.corpo[0].y == self.numero_de_celulas or self.cobra.corpo[0].y == -1:
            self.fim_de_jogo()

    def fim_de_jogo(self):
        self.cobra.resetar()
        self.comida.posicao = self.comida.gerar_posicao_aleatoria(self.cobra.corpo)
        self.estado = "PARADO"
        self.pontuacao = 0
        self.cobra.som_bater_parede.play()

    def verificar_colisao_com_cauda(self):
        corpo_sem_cabeca = self.cobra.corpo[1:]
        if self.cobra.corpo[0] in corpo_sem_cabeca:
            self.fim_de_jogo()
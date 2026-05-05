from cobra import Cobra
from comida import Comida
from buraco import Buraco

class Jogo:
    def __init__(self, deslocamento, tamanho_celula, numero_de_celulas):
        self.cobra = Cobra(tamanho_celula)
        self.comida = Comida(self.cobra.corpo, deslocamento, tamanho_celula, numero_de_celulas)
        self.estado = "RODANDO"
        self.pontuacao = 0
        self.pontuacao_fase = 0
        self.numero_de_celulas = numero_de_celulas
        
        self.fase_atual = 0
        self.buraco = None
        self.meta_pontos = 5
        self.cores_fases = [
            (173, 204, 96),
            (75, 139, 190),
            (255, 140, 0),
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

    def verificar_colisao_com_buraco(self):
        if self.buraco and self.cobra.corpo[0] == self.buraco.posicao:
            self.avancar_fase()

    def avancar_fase(self):
        self.fase_atual += 1
        self.pontuacao_fase = 0
        self.buraco = None
        self.cobra.resetar()
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

    def verificar_colisao_com_cauda(self):
        corpo_sem_cabeca = self.cobra.corpo[1:]
        if self.cobra.corpo[0] in corpo_sem_cabeca:
            self.fim_de_jogo()
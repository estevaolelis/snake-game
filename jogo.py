import pygame
from cobra import Cobra
from comida import Comida
from buraco import Buraco
from comida_podre import ComidaPodre
from pygame.math import Vector2

class Jogo:
    def __init__(self, deslocamento, tamanho_celula, numero_de_celulas):
        """Inicializa o estado do jogo e seus componentes.

        Args:
            deslocamento: deslocamento (margem) em pixels para desenhar o tabuleiro.
            tamanho_celula: tamanho em pixels de cada célula.
            numero_de_celulas: número de células por dimensão do tabuleiro.
        """
        self.cobra = Cobra(tamanho_celula)
        self.comida = Comida(self.cobra.corpo, deslocamento, tamanho_celula, numero_de_celulas)
        self.comidas_podres = []
        self.estado = "PARADO"
        self.pontuacao = 0
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
        self.comida.posicao = self._gerar_posicao_livre()

    def desenhar(self, screen, deslocamento, tamanho_celula, cor_corpo):
        """Desenha os elementos do jogo (comidas, buraco e cobra) na `screen`.

        Args:
            screen: superfície Pygame onde desenhar.
            deslocamento: margem usada para posição dos elementos.
            tamanho_celula: tamanho em pixels de cada célula.
            cor_corpo: cor usada para desenhar o corpo/borda.
        """
        self.comida.desenhar(screen)

        for comida_podre in self.comidas_podres:
            comida_podre.desenhar(screen)
            
        if self.buraco:
            self.buraco.desenhar(screen, deslocamento, tamanho_celula)
            
        self.cobra.desenhar(screen, deslocamento, tamanho_celula, cor_corpo)

    def atualizar(self):
        """Atualiza a lógica do jogo apenas quando o estado é `RODANDO`."""
        if self.estado == "RODANDO":
            self.cobra.atualizar()
            self.verificar_colisao_com_comida()
            self.verificar_colisao_com_comida_podre()
            self.verificar_colisao_com_bordas()
            self.verificar_colisao_com_cauda()
            self.verificar_colisao_com_buraco()

    def verificar_colisao_com_comida(self):
        """Verifica se a cabeça da cobra colidiu com alguma fruta e aplica os efeitos.

        A cada fruta comida, a pontuação sobe e uma fruta extra é adicionada ao mapa.
        """
        if self.cobra.corpo[0] == self.comida.posicao:
            self.cobra.adicionar_segmento = True
            self.pontuacao += 1
            self.cobra.som_comer.play()

            self.comida.posicao = self._gerar_posicao_livre()
            if self.fase_atual >= 1:
                self.comidas_podres.append(
                    ComidaPodre(
                        self.cobra.corpo,
                        self.comida.posicao,
                        [comida_podre.posicao for comida_podre in self.comidas_podres],
                        self.comida.deslocamento,
                        self.comida.tamanho_celula,
                        self.numero_de_celulas,
                    )
                )

            if self.pontuacao % self.meta_pontos == 0 and not self.buraco:
                self.buraco = Buraco(self.cobra.corpo, self.numero_de_celulas)
            self.intervalo_atualizacao = max(60, int(self.intervalo_atualizacao * 0.95))
            pygame.time.set_timer(pygame.USEREVENT, self.intervalo_atualizacao)
            return

    def verificar_colisao_com_comida_podre(self):
        """Verifica se a cobra colidiu com a comida podre e reinicia o jogo."""
        if any(self.cobra.corpo[0] == comida_podre.posicao for comida_podre in self.comidas_podres):
            self.reiniciar_jogo()
            return

    def reiniciar_jogo(self):
        """Volta o jogo para o estado inicial, mantendo o fluxo de início por tecla."""
        self.fase_atual = 0
        self.buraco = None
        self.comidas_podres = []
        self.pontuacao = 0
        self.intervalo_atualizacao = 200
        self.cobra.resetar()
        self.estado = "PARADO"
        self.comida.posicao = self._gerar_posicao_livre()
        pygame.time.set_timer(pygame.USEREVENT, self.intervalo_atualizacao)

    def verificar_colisao_com_buraco(self):
        """Verifica se a cobra entrou no buraco e teletransporta para a nova fase.

        Incrementa a fase atual, limpa a comida podre e prepara o novo cenário.
        """
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
            self.comidas_podres = []

    def avancar_fase(self):
        """Prepara o próximo nível/fase resetando a posição da cobra e limpando elementos obsoletos."""
        posicao_nascimento = Vector2(12, 12)
        tamanho_atual = len(self.cobra.corpo)

        novo_corpo = []
        for i in range(tamanho_atual):
            novo_corpo.append(Vector2(posicao_nascimento.x - i, posicao_nascimento.y))

        self.cobra.corpo = novo_corpo
        self.cobra.direcao = Vector2(1, 0)
        self.comidas_podres = []

    def verificar_colisao_com_bordas(self):
        """Verifica se a cabeça da cobra saiu dos limites do tabuleiro."""
        if self.cobra.corpo[0].x == self.numero_de_celulas or self.cobra.corpo[0].x == -1:
            self.reiniciar_jogo()
        elif self.cobra.corpo[0].y == self.numero_de_celulas or self.cobra.corpo[0].y == -1:
            self.reiniciar_jogo()

    def verificar_colisao_com_cauda(self):
        """Verifica se a cabeça colidiu com a própria cauda."""
        corpo_sem_cabeca = self.cobra.corpo[1:]
        if self.cobra.corpo[0] in corpo_sem_cabeca:
            self.reiniciar_jogo()

    def fim_de_jogo(self):
        """Mantém compatibilidade com a versão anterior e reinicia o jogo."""
        self.reiniciar_jogo()

    def _posicao_ocupada(self, posicao, posicoes_ignoradas=None):
        """Retorna True quando a posição já está ocupada por cobra, frutas ou elementos especiais."""
        if posicao in self.cobra.corpo:
            return True

        if posicoes_ignoradas:
            for outra_posicao in posicoes_ignoradas:
                if posicao == outra_posicao:
                    return True

        if self.buraco and posicao == self.buraco.posicao:
            return True

        for comida_podre in self.comidas_podres:
            if posicao == comida_podre.posicao:
                return True

        return False

    def _gerar_posicao_livre(self, posicoes_ignoradas=None):
        """Gera uma posição aleatória livre no tabuleiro."""
        posicao = self.comida.gerar_celula_aleatoria()
        while self._posicao_ocupada(posicao, posicoes_ignoradas):
            posicao = self.comida.gerar_celula_aleatoria()
        return posicao
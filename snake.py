import pygame, sys, random
from pygame.math import Vector2

pygame.init()

fonte_titulo = pygame.font.Font(None, 60)
fonte_pontuacao = pygame.font.Font(None, 40)

# Cores
VERDE = (173, 204, 96)
VERDE_ESCURO = (43, 51, 24)

# Tamanho de cada quadrado no grid
tamanho_celula = 30
numero_de_celulas = 25

# Espaçamento da borda
DESLOCAMENTO = 75

# Classe responsável por tudo da comida
class Comida:
	def __init__(self, corpo_cobra):
		self.posicao = self.gerar_posicao_aleatoria(corpo_cobra)

	def desenhar(self):
		retangulo_comida = pygame.Rect(
			DESLOCAMENTO + self.posicao.x * tamanho_celula,
			DESLOCAMENTO + self.posicao.y * tamanho_celula,
			tamanho_celula,
			tamanho_celula
		)
		screen.blit(superficie_comida, retangulo_comida)

	def gerar_celula_aleatoria(self):
		x = random.randint(0, numero_de_celulas - 1)
		y = random.randint(0, numero_de_celulas - 1)
		return Vector2(x, y)

	def gerar_posicao_aleatoria(self, corpo_cobra):
		posicao = self.gerar_celula_aleatoria()
		while posicao in corpo_cobra:
			posicao = self.gerar_celula_aleatoria()
		return posicao

# Classe responsável por tudo da cobra
class Cobra:
	def __init__(self):
		self.corpo = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
		self.direcao = Vector2(1, 0)
		self.adicionar_segmento = False
		self.som_comer = pygame.mixer.Sound("Sounds/eat.mp3")
		self.som_bater_parede = pygame.mixer.Sound("Sounds/wall.mp3")

	def desenhar(self):
		for segmento in self.corpo:
			retangulo_segmento = (
				DESLOCAMENTO + segmento.x * tamanho_celula,
				DESLOCAMENTO + segmento.y * tamanho_celula,
				tamanho_celula,
				tamanho_celula
			)
			pygame.draw.rect(screen, VERDE_ESCURO, retangulo_segmento, 0, 7)

	def atualizar(self):
		self.corpo.insert(0, self.corpo[0] + self.direcao)
		if self.adicionar_segmento == True:
			self.adicionar_segmento = False
		else:
			self.corpo = self.corpo[:-1]

	def resetar(self):
		self.corpo = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
		self.direcao = Vector2(1, 0)

# Classe de validações do jogo
class Jogo:
	def __init__(self):
		self.cobra = Cobra()
		self.comida = Comida(self.cobra.corpo)
		self.estado = "RODANDO"
		self.pontuacao = 0

	def desenhar(self):
		self.comida.desenhar()
		self.cobra.desenhar()

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
		if self.cobra.corpo[0].x == numero_de_celulas or self.cobra.corpo[0].x == -1:
			self.fim_de_jogo()
		if self.cobra.corpo[0].y == numero_de_celulas or self.cobra.corpo[0].y == -1:
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

screen = pygame.display.set_mode(
	(2 * DESLOCAMENTO + tamanho_celula * numero_de_celulas,
	 2 * DESLOCAMENTO + tamanho_celula * numero_de_celulas)
)

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

# Criar o jogo
jogo = Jogo()

# Carregar a sprite da comida/maçã
superficie_comida = pygame.image.load("Graphics/food.png")

ATUALIZAR_COBRA = pygame.USEREVENT
pygame.time.set_timer(ATUALIZAR_COBRA, 200)

# Loop para iniciar o jogo, movimentação da cobra e fechar o jogo
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

	jogo.desenhar()

	superficie_titulo = fonte_titulo.render("Retro Snake", True, VERDE_ESCURO)
	superficie_pontuacao = fonte_pontuacao.render(str(jogo.pontuacao), True, VERDE_ESCURO)

	screen.blit(superficie_titulo, (DESLOCAMENTO - 5, 20))
	screen.blit(superficie_pontuacao, (DESLOCAMENTO - 5, DESLOCAMENTO + tamanho_celula * numero_de_celulas + 10))

	pygame.display.update()
	clock.tick(60)
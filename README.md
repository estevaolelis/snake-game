# Snake Game

Projeto de faculdade desenvolvido em Python com Programação Orientada a Objetos e interface feita com `pygame-ce`.

## Sobre o jogo

Este é um jogo da cobrinha clássico, com:

- movimentação em grade;
- mapa em estilo xadrez;
- pontuação exibida no topo;
- som ao comer a comida;
- som ao bater na parede;
- reinício automático quando a cobra morre.

O jogo começa em estado de pausa e inicia quando você pressiona qualquer tecla de direção.

## Requisitos

Este projeto foi pensado para o Python 3.14, por isso utiliza `pygame-ce` em vez da versão tradicional do `pygame`.

### Instalação do Python

Baixe e instale o Python 3.14 em:

https://www.python.org/downloads/

Durante a instalação, marque a opção para adicionar o Python ao `PATH`.

### Instalação do pygame-ce

No terminal, dentro da pasta do projeto, execute:

```bash
python -m pip install pygame-ce
```

Se o seu sistema usar mais de uma versão do Python, você também pode instalar assim:

```bash
py -3.14 -m pip install pygame-ce
```

Se quiser remover a versão antiga do pacote, use:

```bash
python -m pip uninstall pygame
```

> O `pygame-ce` mantém compatibilidade com `import pygame`, então o código do jogo continua usando `pygame` normalmente.

## Como executar

Depois de instalar a dependência, rode o jogo com:

```bash
python main.py
```

Se necessário, use o Python 3.14 explicitamente:

```bash
py -3.14 main.py
```

## Controles

- `Seta para cima`: move a cobra para cima.
- `Seta para baixo`: move a cobra para baixo.
- `Seta para a esquerda`: move a cobra para a esquerda.
- `Seta para a direita`: move a cobra para a direita.

Qualquer tecla de direção também inicia a partida quando o jogo estiver parado.

## Regras

- Coma a comida para ganhar 1 ponto e crescer.
- Bater na parede reinicia a partida.
- Colidir com o próprio corpo também reinicia a partida.

## Estrutura do projeto

- `main.py`: cria a janela, desenha o cenário e controla o loop principal.
- `jogo.py`: controla o estado do jogo, colisões e pontuação.
- `cobra.py`: controla movimento, desenho e sons da cobra.
- `comida.py`: gera a comida em posições aleatórias.
- `Graphics/`: imagens usadas no jogo.
- `Sounds/`: arquivos de som do jogo.

## Ideias futuras

- adicionar alimentos diferentes da maçã, como itens que dão dano ou aumentam a velocidade;
- criar troca de fase com mudança de cores e de itens;
- expandir o mapa ou criar novos cenários.

## Observações

O arquivo `main.py` usa um tabuleiro 25x25 com células de 30 pixels e um deslocamento de 75 pixels para posicionar a área jogável. A pontuação aparece no topo da janela, perto do título.
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

### Instalação de dependências no Linux

#### 1. Criar o ambiente virtual

No terminal, dentro da pasta do projeto, execute:

```bash
python3 -m venv venv
```

#### 2. Ativar o ambiente virtual

```bash
source venv/bin/activate
```

Após ativar, você verá o nome do ambiente (`venv`) entre parênteses no início da linha do terminal.

#### 3. Instalar as dependências

Com o ambiente virtual ativado, instale todas as dependências usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Para desativar o ambiente

Quando terminar de trabalhar, desative o ambiente com:

```bash
deactivate
```

> O `pygame-ce` mantém compatibilidade com `import pygame`, então o código do jogo continua usando `pygame` normalmente.

### Instalação de dependências no Windows

#### 1. Criar o ambiente virtual

No PowerShell ou Prompt de Comando, dentro da pasta do projeto, execute:

```bash
python -m venv venv
```

#### 2. Ativar o ambiente virtual

**PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

**Prompt de Comando (cmd):**
```bash
venv\Scripts\activate.bat
```

Após ativar, você verá o nome do ambiente (`venv`) entre parênteses no início da linha.

#### 3. Instalar as dependências

Com o ambiente virtual ativado, instale todas as dependências usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Para desativar o ambiente

Quando terminar de trabalhar, desative o ambiente com:

```bash
deactivate
```

> O `pygame-ce` mantém compatibilidade com `import pygame`, então o código do jogo continua usando `pygame` normalmente.

## Como executar

Com o ambiente virtual **ativado**, rode o jogo com:

```bash
python main.py
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

## Observações

O arquivo `main.py` usa um tabuleiro 25x25 com células de 30 pixels e um deslocamento de 75 pixels para posicionar a área jogável. A pontuação aparece no topo da janela, perto do título.
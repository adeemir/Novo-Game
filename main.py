import pygame
import sys
from fase import desenhar_fase, fundo_fase, PLATAFORMAS
from personagem import Personagem

pygame.init()

# Tamanho da janela
LARGURA = 800
ALTURA = 600

# Criar a janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Robin Hod")

# Carregar imagem de fundo do menu
fundo_menu = pygame.image.load(
    "assets/Backgrounds/Castelo3.png"
).convert()

# Ajustar imagem ao tamanho da janela
fundo_menu = pygame.transform.scale(
    fundo_menu, (LARGURA, ALTURA)
)

relogio = pygame.time.Clock()

# Cores
PRETO = (20, 20, 30)
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 0)
VERDE = (50, 180, 70)
CINZA = (80, 80, 95)

# Fontes
fonte_titulo = pygame.font.SysFont("Cinzel", 100, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 32)
fonte_pequena = pygame.font.SysFont("Arial", 22)

# Estado atual da tela
tela_atual = "menu"
jogador = Personagem(100, 400)

# Botões do menu
botao_jogar = pygame.Rect(280, 290, 240, 55)
botao_opcoes = pygame.Rect(280, 365, 240, 55)
botao_sair = pygame.Rect(280, 440, 240, 55)



def desenhar_botao(texto, retangulo):
    pos_mouse = pygame.mouse.get_pos()

    # Definir a cor do texto
    if retangulo.collidepoint(pos_mouse):
        cor_texto = (0, 255, 0)  # Verde ao passar o mouse
    else:
        cor_texto = (255, 255, 255)  # Branco normal

    # Criar o texto
    texto_renderizado = fonte_menu.render(
        texto, True, cor_texto
    )

    # Centralizar o texto
    texto_rect = texto_renderizado.get_rect(
        center=retangulo.center
    )

    # Desenhar somente as letras, sem a caixa
    tela.blit(texto_renderizado, texto_rect)


def desenhar_titulo(texto, centro):
    espacamento = 3

    # Calcular a largura total do título
    larguras = [
        fonte_titulo.size(letra)[0]
        for letra in texto
    ]

    largura_total = sum(larguras) + espacamento * (len(texto) - 1)

    # Posição inicial para centralizar o título
    x = centro[0] - largura_total // 2

    for letra in texto:
        # Criar a sombra
        sombra = fonte_titulo.render(
            letra, True, (255, 255, 255)
        )

        # Criar a letra dourada
        titulo = fonte_titulo.render(
            letra, True, (0, 0, 0)
        )

        # Desenhar a sombra
        tela.blit(
            sombra,
            (x + 4, centro[1] - sombra.get_height() // 2 + 4)
        )

        # Desenhar a letra
        tela.blit(
            titulo,
            (x, centro[1] - titulo.get_height() // 2)
        )

        # Avançar para a próxima letra
        x += fonte_titulo.size(letra)[0] + espacamento


# Loop principal do jogo

while True:
    relogio.tick(60)

    # Eventos do jogo
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Tecla ESC
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if tela_atual != "menu":
                    tela_atual = "menu"
                else:
                    pygame.quit()
                    sys.exit()

        # Cliques do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if tela_atual == "menu":

                    if botao_jogar.collidepoint(evento.pos):
                        print("Botão JOGAR clicado!")
                        tela_atual = "jogo"

                    elif botao_opcoes.collidepoint(evento.pos):
                        tela_atual = "opcoes"

                    elif botao_sair.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

    # Desenhar o fundo conforme a tela atual
    if tela_atual == "menu" or tela_atual == "opcoes":
        tela.blit(fundo_menu, (0, 0))

    # Menu principal
    if tela_atual == "menu":
        desenhar_titulo("Robin Hod", (400, 180))
        desenhar_botao("JOGAR", botao_jogar)
        desenhar_botao("OPCOES", botao_opcoes)
        desenhar_botao("SAIR", botao_sair)

    # Tela do jogo
    elif tela_atual == "jogo":
        desenhar_fase(tela, fundo_fase)

        teclas = pygame.key.get_pressed()
        jogador.atualizar(teclas, PLATAFORMAS)
        jogador.desenhar(tela)

    # Tela de opções
    elif tela_atual == "opcoes":
        titulo = fonte_titulo.render(
            "OPCOES", True, AMARELO
        )

        tela.blit(
            titulo,
            titulo.get_rect(center=(400, 220))
        )

        instrucao = fonte_pequena.render(
            "Pressione ESC para voltar",
            True, BRANCO
        )

        tela.blit(
            instrucao,
            instrucao.get_rect(center=(400, 330))
        )

    # Atualizar a tela continuamente
    pygame.display.flip()
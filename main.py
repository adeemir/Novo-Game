import pygame
import sys
from fase import desenhar_fase, fundo_fase, PLATAFORMAS
from personagem import Personagem
from inimigo import Inimigo

pygame.init()

# Tamanho da janela
LARGURA = 800
ALTURA = 600

# Criar a janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Demo - Pega Pega")

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

# Fonte do tempo e da pontuação
fonte_hud = pygame.font.SysFont("Arial", 24, bold=True)
fonte_derrota = pygame.font.SysFont("Arial", 48, bold=True)

# Dados da partida
inicio_partida = 0
tempo_sobrevivido = 0
pontuacao = 0

# Estado atual da tela
tela_atual = "menu"
jogador = Personagem(100, 400)
inimigo = Inimigo(500, 414)
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
                        jogador = Personagem(100, 400)
                        inimigo = Inimigo(500, 414)

                        # Permitir que o inimigo chegue até o jogador
                        inimigo.distancia_parar = 0

                        # Reiniciar o cronômetro e a pontuação
                        inicio_partida = pygame.time.get_ticks()
                        tempo_sobrevivido = 0
                        pontuacao = 0

                        tela_atual = "jogo"

                    elif botao_opcoes.collidepoint(evento.pos):
                        tela_atual = "opcoes"

                    elif botao_sair.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

    # Desenhar o fundo conforme a tela atual
    if tela_atual in ("menu", "opcoes", "como_jogar"):
        tela.blit(fundo_menu, (0, 0))

    # Menu principal
    if tela_atual == "menu":
        desenhar_titulo("Pega Pega", (400, 180))
        desenhar_botao("JOGAR", botao_jogar)
        desenhar_botao("COMO JOGAR", botao_opcoes)
        desenhar_botao("SAIR", botao_sair)


    # Tela do jogo
    elif tela_atual == "jogo":
        desenhar_fase(tela, fundo_fase)

        # Calcular o tempo de sobrevivência
        tempo_sobrevivido = (
                                    pygame.time.get_ticks() - inicio_partida
                            ) // 1000

        # Aumentar a velocidade a cada 10 segundos
        inimigo.velocidade = min(3 + tempo_sobrevivido // 5, 10)

        # Atualizar o jogador e o inimigo
        teclas = pygame.key.get_pressed()
        jogador.atualizar(teclas, PLATAFORMAS)
        inimigo.atualizar(relogio.get_time(), jogador, PLATAFORMAS)

        # Verificar se o inimigo encostou no jogador
        area_jogador = jogador.rect.inflate(-40, -30)
        area_inimigo = inimigo.rect.inflate(-40, -30)

        if area_jogador.colliderect(area_inimigo):
            pontuacao = tempo_sobrevivido * 10
            tela_atual = "derrota"

        # Desenhar personagens
        jogador.desenhar(tela)
        inimigo.desenhar(tela)

        # Calcular a pontuação durante a partida
        pontuacao = tempo_sobrevivido * 10

        # Mostrar tempo e score
        texto_tempo = fonte_hud.render(
            f"Tempo: {tempo_sobrevivido}s", True, BRANCO
        )

        texto_score = fonte_hud.render(
            f"Score: {pontuacao}", True, AMARELO
        )

        tela.blit(texto_tempo, (20, 20))
        tela.blit(texto_score, (20, 55))


    # Tela Como Jogar
    elif tela_atual == "opcoes":
        titulo = fonte_titulo.render(
            "COMO JOGAR", True, AMARELO
        )

        tela.blit(
            titulo,
            titulo.get_rect(center=(400, 160))
        )

        comandos = [
            "SETAS ESQUERDA / DIREITA - Mover",
            "ESPACO - Pular",
            "OBJETIVO - Sobreviva sem ser pego!",
            "PONTUACAO - Ganhe 10 pontos por segundo",
        ]

        y = 260

        for texto in comandos:
            linha = fonte_pequena.render(
                texto, True, BRANCO
            )

            tela.blit(
                linha,
                linha.get_rect(center=(400, y))
            )

            y += 45

        instrucao = fonte_pequena.render(
            "Pressione ESC para voltar ao menu",
            True, AMARELO
        )

        tela.blit(
            instrucao,
            instrucao.get_rect(center=(400, 500))
        )

        # Tela de derrota
    elif tela_atual == "derrota":
        titulo = fonte_derrota.render(
            "VOCE FOI PEGO!", True, AMARELO
        )

        tela.blit(
            titulo,
            titulo.get_rect(center=(400, 220))
        )

        texto_tempo = fonte_menu.render(
            f"Tempo sobrevivido: {tempo_sobrevivido} segundos",
            True, BRANCO
        )

        tela.blit(
            texto_tempo,
            texto_tempo.get_rect(center=(400, 300))
        )

        texto_score = fonte_menu.render(
            f"Pontuacao final: {pontuacao}",
            True, AMARELO
        )

        tela.blit(
            texto_score,
            texto_score.get_rect(center=(400, 350))
        )

        instrucao = fonte_pequena.render(
            "Pressione ESC para voltar ao menu e tentar novamente",
            True, BRANCO
        )

        tela.blit(
            instrucao,
            instrucao.get_rect(center=(400, 430))
        )

    # Atualizar a tela continuamente
    pygame.display.flip()

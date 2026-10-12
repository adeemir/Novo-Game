
import pygame

# Carregar o fundo exclusivo da fase
fundo_fase = pygame.image.load(
    "assets/Backgrounds/Castelo2.png"
)

fundo_fase = pygame.transform.scale(
    fundo_fase, (800, 600)
)

# Cores do cenário
COR_CHAO = (75, 50, 35)
COR_GRAMA = (55, 150, 50)
COR_PLATAFORMA = (100, 70, 45)

# Plataformas onde o personagem pode pousar
PLATAFORMAS = [
    pygame.Rect(120, 400, 180, 20),
    pygame.Rect(450, 360, 160, 20)
]


def desenhar_fase(tela, fundo):
    # Desenhar o fundo da fase
    tela.blit(fundo, (0, 0))

    # Desenhar o chão
    pygame.draw.rect(
        tela, COR_CHAO, (0, 520, 800, 80)
    )

    # Grama na parte superior do chão
    pygame.draw.rect(
        tela, COR_GRAMA, (0, 510, 800, 10)
    )

    # Desenhar as plataformas usando as mesmas posições
    for plataforma in PLATAFORMAS:
        pygame.draw.rect(
            tela, COR_PLATAFORMA, plataforma
        )

        ## Contorno vermelho para testar a colisão
        #pygame.draw.rect(
        #    tela, (255, 0, 0), plataforma, 2
        #)


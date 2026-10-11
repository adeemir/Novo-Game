

import pygame


def desenhar_fase(tela, fundo):
    # Fundo azul para testar
    tela.fill((0, 0, 100))

    # Chão verde
    pygame.draw.rect(
        tela,
        (0, 255, 0),
        (0, 500, 800, 100)
    )

    # Plataforma vermelha
    pygame.draw.rect(
        tela,
        (255, 0, 0),
        (200, 400, 200, 25)
    )
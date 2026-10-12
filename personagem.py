import pygame


class Personagem:
    def __init__(self, x, y):
        # Carregar as imagens de animação
        self.sprite_idle = pygame.image.load(
            "assets/Player/Idle.png"
        ).convert_alpha()

        self.sprite_walk = pygame.image.load(
            "assets/Player/Walk.png"
        ).convert_alpha()

        self.sprite_jump = pygame.image.load(
            "assets/Player/Jump.png"
        ).convert_alpha()

        # Tamanho de cada quadro da sprite sheet
        self.largura_quadro = 32
        self.altura_quadro = 32

        # Tamanho do personagem na tela
        self.tamanho = (96, 96)

        # Criar os quadros das animações
        self.animacao_idle = self.carregar_quadros(
            self.sprite_idle
        )

        self.animacao_walk = self.carregar_quadros(
            self.sprite_walk
        )

        self.animacao_jump = self.carregar_quadros(
            self.sprite_jump
        )

        print("Tamanho do quadro:", self.animacao_idle[0].get_size())
        print(
            "Área visível do personagem:",
            self.animacao_idle[0].get_bounding_rect()
        )

        # Começar parado
        self.animacao_atual = self.animacao_idle
        self.indice_animacao = 0
        self.tempo_animacao = 0

        self.imagem = self.animacao_atual[0]

        # Posição e velocidade
        self.rect = self.imagem.get_rect(topleft=(x, y))
        self.velocidade = 6
        # Área de colisão do personagem
        self.colisao = pygame.Rect(
            x + 27,
            y + 24,
            39,
            72
        )

        # Área de colisão ajustada para o personagem
        self.colisao = pygame.Rect(
            x + 20, y + 10, 56, 86
        )

        # Pulo e gravidade
        self.velocidade_y = 0
        self.gravidade = 0.8
        self.forca_pulo = -15
        self.no_chao = True
        self.altura_chao = 510 - 96

    def carregar_quadros(self, sprite_sheet):
        quadros = []

        largura_total = sprite_sheet.get_width()
        quantidade = largura_total // self.largura_quadro

        for i in range(quantidade):
            quadro = sprite_sheet.subsurface(
                (
                    i * self.largura_quadro,
                    0,
                    self.largura_quadro,
                    self.altura_quadro
                )
            ).copy()

            quadro = pygame.transform.scale(
                quadro, self.tamanho
            )

            quadros.append(quadro)

        return quadros



    def atualizar(self, teclas, plataformas):
        andando = False

        # Guardar a posição anterior dos pés visíveis
        y_anterior = self.rect.y + 24 + 72

        # Movimento horizontal
        movimento_x = 0

        if teclas[pygame.K_RIGHT]:
            movimento_x = self.velocidade
            andando = True

        if teclas[pygame.K_LEFT]:
            movimento_x = -self.velocidade
            andando = True

        # Área de colisão baseada na parte visível do personagem
        colisao = pygame.Rect(
            self.rect.x + 27,
            self.rect.y + 24,
            39,
            72
        )

        # Verificar colisão lateral
        for plataforma in plataformas:
            sobreposto_verticalmente = (
                    colisao.bottom > plataforma.top
                    and colisao.top < plataforma.bottom
            )

            if not sobreposto_verticalmente:
                continue

            if movimento_x > 0:
                distancia = plataforma.left - colisao.right

                if 0 <= distancia < movimento_x:
                    movimento_x = distancia

            elif movimento_x < 0:
                distancia = plataforma.right - colisao.left

                if movimento_x < distancia <= 0:
                    movimento_x = distancia

        # Aplicar movimento horizontal
        self.rect.x += movimento_x

        # Limites da tela usando a imagem
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 800:
            self.rect.right = 800

        # Atualizar a área de colisão após o movimento
        colisao.x = self.rect.x + 27
        colisao.y = self.rect.y + 24

        # Pular com a tecla ESPAÇO
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

        # Guardar a posição anterior da cabeça
        topo_anterior = self.rect.y + 24

        # Aplicar gravidade
        self.velocidade_y += self.gravidade
        self.rect.y += int(self.velocidade_y)


        # Atualizar a área de colisão após o movimento vertical
        colisao.x = self.rect.x + 27
        colisao.y = self.rect.y + 24

        # Impedir atravessar a plataforma por baixo
        if self.velocidade_y < 0:
            for plataforma in plataformas:
                if (
                        topo_anterior >= plataforma.bottom
                        and colisao.top <= plataforma.bottom
                        and colisao.right > plataforma.left
                        and colisao.left < plataforma.right
                ):
                    self.rect.y = plataforma.bottom - 24
                    self.velocidade_y = 0
                    colisao.y = self.rect.y + 24
                    break


        # Atualizar a colisão vertical
        colisao.x = self.rect.x + 27
        colisao.y = self.rect.y + 24

        # Verificar pouso nas plataformas
        self.no_chao = False

        if self.velocidade_y >= 0:
            for plataforma in plataformas:
                if (
                        y_anterior <= plataforma.top
                        and colisao.bottom >= plataforma.top
                        and colisao.right > plataforma.left
                        and colisao.left < plataforma.right
                ):
                    self.rect.y = plataforma.top - 24 - 72
                    self.velocidade_y = 0
                    self.no_chao = True
                    break

        # Pousar no chão principal
        altura_pes = self.rect.y + 24 + 72

        if altura_pes >= 510:
            self.rect.y = 510 - 24 - 72
            self.velocidade_y = 0
            self.no_chao = True

        # Escolher a animação
        if not self.no_chao:
            nova_animacao = self.animacao_jump
        elif andando:
            nova_animacao = self.animacao_walk
        else:
            nova_animacao = self.animacao_idle

        # Reiniciar a animação quando ela mudar
        if nova_animacao != self.animacao_atual:
            self.animacao_atual = nova_animacao
            self.indice_animacao = 0
            self.tempo_animacao = 0

        # Avançar a animação
        self.tempo_animacao += 1

        if self.tempo_animacao >= 8:
            self.tempo_animacao = 0
            self.indice_animacao += 1

            if self.indice_animacao >= len(self.animacao_atual):
                self.indice_animacao = 0

        self.imagem = self.animacao_atual[self.indice_animacao]



    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


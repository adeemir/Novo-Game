
import pygame


class Inimigo:
    def __init__(self, x, y):
        self.animacoes = {
            "idle": self.carregar_animacao("assets/inimigo/idle.png"),
            "jump": self.carregar_animacao("assets/inimigo/jump.png"),
            "run": self.carregar_animacao("assets/inimigo/run.png"),
            "walk": self.carregar_animacao("assets/inimigo/walk.png")
        }

        self.animacao_atual = "idle"
        self.quadro_atual = 0
        self.tempo_animacao = 0
        self.velocidade_animacao = 150

        self.rect = pygame.Rect(x, y, 96, 96)
        self.colisao = pygame.Rect(
            x + 27,
            y + 24,
            39,
            72
        )
        self.rect_colisao = pygame.Rect(x + 20, y + 10, 56, 86)

        # Configuracoes da IA
        self.velocidade = 3
        self.distancia_perseguicao = 500
        self.distancia_parar = 20

        # Pulo e gravidade
        self.velocidade_y = 0
        self.gravidade = 0.6
        self.forca_pulo = -15
        self.no_chao = False

        # Direcao: 1 = direita; -1 = esquerda
        self.direcao = -1

    def carregar_animacao(self, caminho):
        imagem = pygame.image.load(caminho).convert_alpha()

        largura_quadro = 128
        altura_quadro = 128

        quadros = []

        for x in range(0, imagem.get_width(), largura_quadro):
            quadro = imagem.subsurface(
                (x, 0, largura_quadro, altura_quadro)
            )

            quadro = pygame.transform.scale(quadro, (96, 96))
            quadros.append(quadro)

        return quadros

    def atualizar(self, tempo, jogador, plataformas):
        # Incluir o chao da fase nas superficies de colisao
        chao = pygame.Rect(0, 510, 800, 90)
        superficies = list(plataformas) + [chao]

        # Calcular a distancia ate o jogador
        distancia = jogador.rect.centerx - self.rect.centerx

        # Decidir se persegue o jogador

        if abs(distancia) <= self.distancia_perseguicao:
            jogador_abaixo = jogador.rect.top > self.rect.bottom + 5

            if abs(distancia) > self.distancia_parar:
                self.direcao = 1 if distancia > 0 else -1

                if self.no_chao and jogador_abaixo:
                    # Procurar a plataforma onde o inimigo está
                    plataforma_atual = None

                    for plataforma in plataformas:
                        if (
                                abs(self.rect.bottom - plataforma.top) <= 2
                                and self.rect.right > plataforma.left
                                and self.rect.left < plataforma.right
                        ):
                            plataforma_atual = plataforma
                            break

                    if plataforma_atual:
                        # Andar até a borda na direção do jogador
                        if self.direcao == 1:
                            limite = plataforma_atual.right
                            if self.rect.right < limite:
                                self.rect.x = min(
                                    self.rect.x + round(self.velocidade),
                                    limite - self.rect.width
                                )
                        else:
                            limite = plataforma_atual.left
                            if self.rect.left > limite:
                                self.rect.x = max(
                                    self.rect.x - round(self.velocidade),
                                    limite
                                )
                        # Na borda, não bloquear a queda
                    else:
                        self.rect.x += round(self.velocidade) * self.direcao
                else:
                    self.rect.x += round(self.velocidade) * self.direcao

                if self.no_chao:
                    self.animacao_atual = "run"
            elif self.no_chao:
                self.animacao_atual = "idle"

        # Atualizar a área de colisão do inimigo
        self.colisao.x = self.rect.x + 27
        self.colisao.y = self.rect.y + 24

        # Guardar a posição anterior
        fundo_anterior = self.colisao.bottom
        topo_anterior = self.colisao.top

        # Aplicar gravidade
        self.velocidade_y += self.gravidade
        self.rect.y += round(self.velocidade_y)

        # Comecar considerando que esta no ar
        self.no_chao = False

        # Colisao ao subir: nao atravessar plataformas por baixo
        if self.velocidade_y < 0:
            for plataforma in superficies:
                if (
                    topo_anterior >= plataforma.bottom
                    and self.rect.top <= plataforma.bottom
                    and self.rect.right > plataforma.left
                    and self.rect.left < plataforma.right
                ):
                    self.rect.top = plataforma.bottom
                    self.velocidade_y = 0
                    break

        # Aterrissar nas plataformas e no chao
        if self.velocidade_y >= 0:
            for plataforma in superficies:
                if (
                        fundo_anterior <= plataforma.top
                        and self.rect.bottom >= plataforma.top
                        and self.rect.right > plataforma.left
                        and self.rect.left < plataforma.right
                ):
                    self.rect.bottom = plataforma.top
                    self.velocidade_y = 0
                    self.no_chao = True
                    break

        # Pular automaticamente quando o jogador estiver acima
        jogador_mais_alto = jogador.rect.bottom < self.rect.bottom - 30
        perto_horizontalmente = abs(distancia) < 300

        if jogador_mais_alto and perto_horizontalmente and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False
            self.animacao_atual = "jump"

        # Escolher animacao no ar
        if not self.no_chao:
            self.animacao_atual = "jump"

        # Atualizar os quadros da animacao
        self.tempo_animacao += tempo
        quadros = self.animacoes[self.animacao_atual]

        if self.quadro_atual >= len(quadros):
            self.quadro_atual = 0

        if self.tempo_animacao >= self.velocidade_animacao:
            self.tempo_animacao = 0
            self.quadro_atual += 1

            if self.quadro_atual >= len(quadros):
                self.quadro_atual = 0

    def desenhar(self, tela):
        imagem = self.animacoes[self.animacao_atual][self.quadro_atual]

        if self.direcao == 1:
            imagem = pygame.transform.flip(imagem, True, False)

        tela.blit(imagem, self.rect)
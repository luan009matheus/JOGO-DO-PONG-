import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong com Loja")

# FPS e Fonte
FPS = 60
FONTE = pygame.font.SysFont("Arial", 30)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Variáveis de customização
cor_raquete = BRANCO
tamanho_raquete = 100
estilo_bola = 'padrao'

# Sistema de pontos e loja
pontos = 0
itens_comprados = {
    "raquete_azul": False,
    "raquete_verde": False,
    "raquete_grande": False,
    "bola_futurista": False
}

# Raquete
class Raquete:
    def __init__(self, x):
        self.largura = 10
        self.altura = tamanho_raquete
        self.x = x
        self.y = ALTURA // 2 - self.altura // 2
        self.velocidade = 5

    def desenhar(self):
        pygame.draw.rect(TELA, cor_raquete, (self.x, self.y, self.largura, self.altura))

    def mover(self, cima, baixo):
        if cima and self.y > 0:
            self.y -= self.velocidade
        if baixo and self.y + self.altura < ALTURA:
            self.y += self.velocidade

# Bola
class Bola:
    def __init__(self):
        self.raio = 10
        self.resetar()

    def resetar(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.vx = 4
        self.vy = 4

    def mover(self):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.raio <= 0 or self.y + self.raio >= ALTURA:
            self.vy *= -1

        if self.x - self.raio <= 0:
            self.resetar()

        if self.x + self.raio >= LARGURA:
            global pontos
            pontos += 10
            self.resetar()

    def desenhar(self):
        cor = AZUL if estilo_bola == 'futurista' else BRANCO
        pygame.draw.circle(TELA, cor, (self.x, self.y), self.raio)

# Funções do jogo
def desenhar_tela(raquete_jogador, raquete_inimigo, bola):
    TELA.fill(PRETO)
    raquete_jogador.desenhar()
    raquete_inimigo.desenhar()
    bola.desenhar()

    texto_pontos = FONTE.render(f"Pontos: {pontos}", True, BRANCO)
    TELA.blit(texto_pontos, (10, 10))
    pygame.display.update()

def loja():
    global pontos, cor_raquete, tamanho_raquete, estilo_bola

    rodando = True
    while rodando:
        TELA.fill(PRETO)
        titulo = FONTE.render("LOJA - Pressione ESC para voltar", True, BRANCO)
        TELA.blit(titulo, (200, 20))

        opcoes = [
            ("1 - Raquete Azul (30 pts)", "raquete_azul", 30),
            ("2 - Raquete Verde (30 pts)", "raquete_verde", 30),
            ("3 - Raquete Grande (50 pts)", "raquete_grande", 50),
            ("4 - Bola Futurista (40 pts)", "bola_futurista", 40)
        ]

        for i, (texto, chave, custo) in enumerate(opcoes):
            cor = VERDE if itens_comprados[chave] else BRANCO
            TELA.blit(FONTE.render(texto, True, cor), (100, 100 + i * 40))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_1 and pontos >= 30:
                    pontos -= 30
                    cor_raquete = AZUL
                    itens_comprados["raquete_azul"] = True
                elif evento.key == pygame.K_2 and pontos >= 30:
                    pontos -= 30
                    cor_raquete = VERDE
                    itens_comprados["raquete_verde"] = True
                elif evento.key == pygame.K_3 and pontos >= 50:
                    pontos -= 50
                    tamanho_raquete = 150
                    itens_comprados["raquete_grande"] = True
                elif evento.key == pygame.K_4 and pontos >= 40:
                    pontos -= 40
                    estilo_bola = 'futurista'
                    itens_comprados["bola_futurista"] = True

# Loop principal
def main():
    global tamanho_raquete

    clock = pygame.time.Clock()
    raquete_jogador = Raquete(20)
    raquete_inimigo = Raquete(LARGURA - 30)
    bola = Bola()

    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_l:
                    loja()
                    # Atualizar tamanho das raquetes
                    raquete_jogador.altura = tamanho_raquete
                    raquete_inimigo.altura = tamanho_raquete

        teclas = pygame.key.get_pressed()
        raquete_jogador.mover(teclas[pygame.K_w], teclas[pygame.K_s])

        # Movimento inimigo automático
        if bola.y < raquete_inimigo.y:
            raquete_inimigo.y -= raquete_inimigo.velocidade
        elif bola.y > raquete_inimigo.y + raquete_inimigo.altura:
            raquete_inimigo.y += raquete_inimigo.velocidade

        bola.mover()

        # Colisão com raquetes
        if (bola.x - bola.raio <= raquete_jogador.x + raquete_jogador.largura and
            raquete_jogador.y <= bola.y <= raquete_jogador.y + raquete_jogador.altura):
            bola.vx *= -1

        if (bola.x + bola.raio >= raquete_inimigo.x and
            raquete_inimigo.y <= bola.y <= raquete_inimigo.y + raquete_inimigo.altura):
            bola.vx *= -1

        desenhar_tela(raquete_jogador, raquete_inimigo, bola)

if __name__ == "__main__":
    main()

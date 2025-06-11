import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
import json

pygame.init()
inicializarBancoDeDados()

# Tela e configurações iniciais
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
relogio = pygame.time.Clock()
pygame.display.set_caption("Espaço Sideral")
icone = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza = (200, 200, 200)

# Fontes
fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 120)
fonteBV = pygame.font.SysFont("arial", 40)
fonte_explicacao = pygame.font.SysFont("arial", 20)
fonte_mensagem = pygame.font.SysFont("arial", 50)  # Adicionada

# Imagens e sons
iron = pygame.transform.scale(pygame.image.load("assets/iron.png"), (100, 150))
fundoStart = pygame.transform.scale(pygame.image.load("assets/fundoStart.jpg"), (1000, 700))
fundoDead = pygame.transform.scale(pygame.image.load("assets/fundoDead.png"), (1000, 700))
missel = pygame.transform.scale(pygame.image.load("assets/missile.png"), (200, 200))
lua = pygame.transform.scale(pygame.image.load("assets/lua.png"), (200, 200))
missileSound = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
pygame.mixer.music.load("assets/ironsound.mp3")

# Nome global
global nome
nome = ""

def desenhar_texto_centralizado(texto, fonte, cor, superficie, y):  # Adicionada
    texto_renderizado = fonte.render(texto, True, cor)
    texto_rect = texto_renderizado.get_rect(center=(tamanho[0]//2, y))
    superficie.blit(texto_renderizado, texto_rect)

def jogar():
    global nome
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    larguraPersona = 90
    alturaPersona = 150
    larguraMissel = 180
    alturaMissel = 200
    pontos = 0
    pausado = False

    estrelas = [[random.randint(0, 1000), random.randint(0, 700)] for _ in range(100)]

    # Lua decorativa
    lua_x = random.randint(0, 900)
    lua_y = random.randint(0, 600)
    lua_dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
    lua_dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)

    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0

        if pausado:
            texto_pause = fonteMenu.render("Jogo Pausado", True, branco)
            tela.blit(texto_pause, (450, 350))
            pygame.display.update()
            relogio.tick(60)
            continue

        posicaoXPersona += movimentoXPersona
        posicaoXPersona = max(0, min(910, posicaoXPersona))

        tela.fill(preto)
        for estrela in estrelas:
            estrela[1] += 1
            if estrela[1] > 700:
                estrela[1] = 0
                estrela[0] = random.randint(0, 1000)
            pygame.draw.circle(tela, branco, estrela, 2)

        lua_x += lua_dx
        lua_y += lua_dy
        if lua_x <= 0 or lua_x + 100 >= 1000:
            lua_dx *= -1
        if lua_y <= 0 or lua_y + 100 >= 700:
            lua_dy *= -1

        tela.blit(lua, (int(lua_x), int(lua_y)))
        tela.blit(iron, (posicaoXPersona, posicaoYPersona))

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 700:
            posicaoYMissel = -240
            posicaoXMissel = random.randint(0, 800)
            velocidadeMissel += 1
            pontos += 1
            pygame.mixer.Sound.play(missileSound)

        tela.blit(missel, (posicaoXMissel, posicaoYMissel))
        texto = fonteMenu.render(f"Pontos: {pontos}   Press Space to Pause Game", True, branco)
        tela.blit(texto, (15, 15))

        if (posicaoXPersona < posicaoXMissel + larguraMissel and
            posicaoXPersona + larguraPersona > posicaoXMissel and
            posicaoYPersona < posicaoYMissel + alturaMissel and
            posicaoYPersona + alturaPersona > posicaoYMissel):
            escreverDados(nome, pontos)
            dead(pontos)  # Corrigido aqui

        pygame.display.update()
        relogio.tick(60)

def tela_bem_vindo(nome):
    imagem_apresentacao = pygame.transform.scale(pygame.image.load("assets/imagem_apresentacao.jpg"), (1000, 700))
    estrelas = [[random.randint(0, 1000), random.randint(0, 700)] for _ in range(100)]
    linhas = [
        "Em um futuro distante...",
        "A humanidade sonha em alcançar a Lua novamente.",
        "Mas há um problema...",
        "Cometas perigosos tomaram conta do espaço!",
        "Sua missão é desviar de todos eles...",
        "E chegar o mais longe possível!",
        "Boa sorte, comandante."
    ]

    for i, linha in enumerate(linhas):
        for _ in range(30):
            tela.fill(preto)
            for estrela in estrelas:
                estrela[1] += 1
                if estrela[1] > 700:
                    estrela[1] = 0
                    estrela[0] = random.randint(0, 1000)
                pygame.draw.circle(tela, branco, estrela, 2)
            for j in range(i):
                texto_ant = fonte_explicacao.render(linhas[j], True, branco)
                tela.blit(texto_ant, (50, 100 + j * 50))
            texto_parcial = fonte_explicacao.render(linha[:int(len(linha) * (_ / 30))], True, branco)
            tela.blit(texto_parcial, (50, 100 + i * 50))
            pygame.display.update()
            relogio.tick(60)

    botao_rect = pygame.Rect(400, 500, 200, 60)
    executando = True
    while executando:
        tela.fill(branco)
        tela.blit(imagem_apresentacao, (0, 0))
        texto_nome = fonteBV.render(f"Bem-vindo ao jogo, {nome}", True, preto)
        tela.blit(texto_nome, (300, 300))
        pygame.draw.rect(tela, cinza, botao_rect)
        texto_botao = fonteBV.render("Iniciar", True, preto)
        tela.blit(texto_botao, (botao_rect.x + 40, botao_rect.y + 10))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    executando = False
        pygame.display.update()
        relogio.tick(60)

    jogar()

def solicitar_nome():
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()
    root = tk.Tk()
    root.geometry("300x50")
    root.title("Informe seu nickname")
    entry_nome = tk.Entry(root)
    entry_nome.pack()
    tk.Button(root, text="Enviar", command=obter_nome).pack()
    root.mainloop()
    tela_bem_vindo(nome)

def dead(pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    tela.blit(fundoDead, (0, 0))
    desenhar_texto_centralizado("Sua nave explodiu", fonte_mensagem, branco, tela, tamanho[1]//2 - 50)
    desenhar_texto_centralizado(f"Pontos: {pontos}", fonte_mensagem, branco, tela, tamanho[1]//2 + 20)
    pygame.display.update()
    pygame.time.delay(3000)
    start()

def start():
    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    solicitar_nome()
                if quitButton.collidepoint(evento.pos):
                    quit()
        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        tela.blit(fonteMenu.render("Iniciar Game", True, preto), (25, 12))
        tela.blit(fonteMenu.render("Sair do Game", True, preto), (25, 62))
        pygame.display.update()
        relogio.tick(60)

start()

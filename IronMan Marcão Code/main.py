import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
from recursos.funcoes import (
    inicializarBancoDeDados,
    escreverDados,
    obterRanking,
    obterHistorico
)
import json
from datetime import datetime

# Inicialização do Pygame, TTS e banco de dados
pygame.init()
engine = pyttsx3.init()
inicializarBancoDeDados()

# Configurações de tela
TAMANHO = (1000, 700)
tela = pygame.display.set_mode(TAMANHO)
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
fonteExp = pygame.font.SysFont("arial", 20)
fonteMsg = pygame.font.SysFont("arial", 60)

# Imagens e sons
iron = pygame.transform.scale(pygame.image.load("assets/iron.png"), (100, 150))
fundoStart = pygame.transform.scale(pygame.image.load("assets/fundoStart.jpg"), (1000, 700))
fundoDead = pygame.transform.scale(pygame.image.load("assets/fundoDead.png"), (1000, 700))
missel = pygame.transform.scale(pygame.image.load("assets/missile.png"), (200, 200))
lua_img = pygame.transform.scale(pygame.image.load("assets/lua.png"), (200, 200))
missileSound = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
pygame.mixer.music.load("assets/ironsound.mp3")

# Variável global para nome do jogador
nome = ""

def desenhar_texto_centralizado(texto, fonte, cor, superficie, y):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=(TAMANHO[0] // 2, y))
    superficie.blit(render, rect)

# --- Funções de exibição de ranking e histórico ---
def mostrar_ranking():
    ranking = obterRanking()
    tela.fill(preto)
    desenhar_texto_centralizado("Top 5 Jogadores", fonteBV, branco, tela, 50)
    engine.say("Top 5 jogadores")
    for i, dado in enumerate(ranking):
        texto = fonteMenu.render(f"{i+1}. {dado['nome']} - {dado['pontos']} pts", True, branco)
        tela.blit(texto, (350, 120 + i * 40))
        engine.say(f"{i+1}. {dado['nome']} com {dado['pontos']} pontos")
    pygame.display.update()
    engine.runAndWait()
    pygame.time.delay(5000)

def mostrar_historico():
    historico = obterHistorico()
    tela.fill(preto)
    desenhar_texto_centralizado("Histórico de Partidas", fonteBV, branco, tela, 50)
    engine.say("Histórico de partidas")
    ultima = historico[-10:]
    for dado in ultima:
        engine.say(f"{dado['nome']} fez {dado['pontos']} pontos em {dado['data']} às {dado['hora']}")
        texto = fonteMenu.render(
            f"{dado['nome']} - {dado['pontos']} pts - {dado['data']} às {dado['hora']}", True, branco)
        tela.blit(texto, (200, 120 + ultima.index(dado) * 40))
    pygame.display.update()
    engine.runAndWait()
    pygame.time.delay(7000)

# --- Loop principal de jogo ---
def jogar():
    global nome
    x_player, y_player = 400, 300
    mov_x = 0
    x_missel, y_missel = 400, -240
    vel_missel = 1
    pontos = 0
    pausado = False
    estrelas = [[random.randint(0, 1000), random.randint(0, 700)] for _ in range(100)]
    lua_x = random.randint(0, 900)
    lua_y = random.randint(0, 600)
    lua_dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
    lua_dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)

    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)

    rodando = True
    while rodando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT: mov_x = 15
                if ev.key == pygame.K_LEFT: mov_x = -15
                if ev.key == pygame.K_SPACE: pausado = not pausado
            if ev.type == pygame.KEYUP:
                if ev.key in (pygame.K_RIGHT, pygame.K_LEFT): mov_x = 0

        if pausado:
            desenhar_texto_centralizado("Jogo Pausado", fonteMenu, branco, tela, 350)
            pygame.display.update()
            relogio.tick(60)
            continue

        x_player = max(0, min(910, x_player + mov_x))
        tela.fill(preto)
        for est in estrelas:
            est[1] += 1
            if est[1] > 700:
                est[1] = 0
                est[0] = random.randint(0, 1000)
            pygame.draw.circle(tela, branco, est, 2)

        lua_x += lua_dx; lua_y += lua_dy
        if lua_x <= 0 or lua_x + 100 >= 1000: lua_dx *= -1
        if lua_y <= 0 or lua_y + 100 >= 700: lua_dy *= -1
        tela.blit(lua_img, (int(lua_x), int(lua_y)))
        tela.blit(iron, (x_player, y_player))

        y_missel += vel_missel
        if y_missel > 700:
            y_missel = -240
            x_missel = random.randint(0, 800)
            vel_missel += 1
            pontos += 1
            pygame.mixer.Sound.play(missileSound)

        tela.blit(missel, (x_missel, y_missel))
        texto = fonteMenu.render(f"Pontos: {pontos}   Pressione ESPAÇO para pausar", True, branco)
        tela.blit(texto, (15, 15))

        # Colisão
        if (x_player < x_missel + 180 and x_player + 90 > x_missel and
            y_player < y_missel + 200 and y_player + 150 > y_missel):
            escreverDados(nome, pontos)
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(explosaoSound)
            tela.blit(fundoDead, (0, 0))
            desenhar_texto_centralizado("Sua nave explodiu!", fonteMorte, branco, tela, 250)
            desenhar_texto_centralizado(f"Pontos: {pontos}", fonteMsg, branco, tela, 350)
            pygame.display.update()
            engine.say(f"Sua nave explodiu. Você fez {pontos} pontos.")
            engine.runAndWait()
            pygame.time.delay(4000)
            rodando = False

        pygame.display.update()
        relogio.tick(60)

# --- Tela de boas-vindas e seleção por voz ou texto ---
def solicitar_nome():
    global nome
    def digitado():
        nonlocal entry
        n = entry.get().strip()
        if not n:
            messagebox.showwarning("Aviso", "Digite seu nome!")
        else:
            nome = n
            root.destroy()

    def por_voz():
        global nome
        r = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Fale agora", "Diga seu nome após clicar em OK.")
            try:
                audio = r.listen(source, timeout=5)
                nome = r.recognize_google(audio, language='pt-BR').strip()
                root.destroy()
            except sr.UnknownValueError:
                messagebox.showerror("Erro", "Não entendi. Tente novamente.")
            except sr.RequestError:
                messagebox.showerror("Erro", "Serviço indisponível.")

    root = tk.Tk()
    root.title("Informe seu nickname")
    root.geometry("350x150")
    tk.Label(root, text="Digite seu nome:").pack(pady=5)
    entry = tk.Entry(root)
    entry.pack()
    tk.Button(root, text="Enviar", command=digitado).pack(pady=5)
    tk.Button(root, text="Falar nome", command=por_voz).pack()
    root.mainloop()
    tela_bem_vindo()

# --- Tela de introdução com animação e narração ---
def tela_bem_vindo():
    global nome
    img = pygame.transform.scale(pygame.image.load("assets/imagem_apresentacao.jpg"), TAMANHO)
    estrelas = [[random.randint(0,1000), random.randint(0,700)] for _ in range(100)]
    linhas = [
        "Em um futuro distante...",
        "A humanidade sonha em alcançar a Lua novamente.",
        "Mas há um problema...",
        "Cometas perigosos tomaram conta do espaço!",
        "Sua missão é desviar de todos eles...",
        "E chegar o mais longe possível!",
        f"Boa sorte, comandante {nome}."
    ]
    
    # Primeiro: executar toda a narração antes de mostrar a animação
    engine = pyttsx3.init()
    for linha in linhas:
        engine.say(linha)
    engine.runAndWait()
    
    # Depois que a narração terminar, mostrar a animação
    for i, linha in enumerate(linhas):
        for j in range(30):
            tela.fill(preto)
            for est in estrelas:
                est[1] = (est[1]+1) % 700
                pygame.draw.circle(tela, branco, est, 2)
            for k in range(i):
                tela.blit(fonteExp.render(linhas[k], True, branco), (50,100+k*50))
            tela.blit(fonteExp.render(linha[:int(len(linha)*j/30)], True, branco), (50,100+i*50))
            pygame.display.update()
            relogio.tick(60)
    
    # Tela de boas-vindas com botão
    botao = pygame.Rect(400,500,200,60)
    running = True
    while running:
        tela.fill(branco)
        tela.blit(img, (0,0))
        
        # Texto de boas-vindas com o nome do jogador
        texto_bem_vindo = fonteBV.render(f"Bem-vindo, {nome}!", True, preto)
        rect_bem_vindo = texto_bem_vindo.get_rect(center=(TAMANHO[0]//2, 300))
        tela.blit(texto_bem_vindo, rect_bem_vindo)
        
        # Botão Iniciar
        pygame.draw.rect(tela, cinza, botao)
        texto_iniciar = fonteBV.render("Iniciar", True, preto)
        rect_iniciar = texto_iniciar.get_rect(center=botao.center)
        tela.blit(texto_iniciar, rect_iniciar)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and botao.collidepoint(ev.pos):
                running = False
        pygame.display.update()
        relogio.tick(60)
    jogar()

# --- Menu inicial com botões de voz, ranking e histórico ---
def start():
    largura, altura = 200, 40
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: exit()
            if ev.type == pygame.MOUSEBUTTONUP:
                if btn_start.collidepoint(ev.pos): solicitar_nome()
                if btn_quit.collidepoint(ev.pos): exit()
                if btn_rank.collidepoint(ev.pos): mostrar_ranking()
                if btn_hist.collidepoint(ev.pos): mostrar_historico()
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        btn_start = pygame.draw.rect(tela, branco, (10,10,largura,altura), border_radius=15)
        btn_quit  = pygame.draw.rect(tela, branco, (10,60,largura,altura), border_radius=15)
        btn_rank  = pygame.draw.rect(tela, branco, (10,110,largura,altura), border_radius=15)
        btn_hist  = pygame.draw.rect(tela, branco, (10,160,largura,altura), border_radius=15)
        tela.blit(fonteMenu.render("Iniciar Game", True, preto), (30,12))
        tela.blit(fonteMenu.render("Sair do Game", True, preto), (30,62))
        tela.blit(fonteMenu.render("Ver Ranking", True, preto), (30,112))
        tela.blit(fonteMenu.render("Ver Histórico", True, preto), (30,162))
        pygame.display.update()
        relogio.tick(60)

if __name__ == "__main__":
    start()
# 🚀 Espaço Sideral

Um jogo 2D desenvolvido em Python com Pygame para a disciplina de Pensamento Computacional.  
Você controla uma nave espacial que deve **desviar de cometas** e acumular pontos.  
O jogo inclui **narração**, **reconhecimento de voz**, **ranking**, **histórico**, **animações** e muito mais!

## 🧠 Desenvolvido por
**Eduarda Q. F. Bolner**  
**RA:** 1137825

---

## 🎮 Como Jogar

- Use as **setas ← →** para mover a nave.
- Pressione **ESPAÇO** para pausar/despausar o jogo.
- Evite ser atingido pelos mísseis!
- Seu desempenho será registrado com **data, hora e pontuação.**

---

## 🛠️ Tecnologias Utilizadas

### 🔤 Linguagem
- **Python** — Linguagem principal usada no projeto.

### 🕹️ Desenvolvimento de Jogos
- **Pygame** — Utilizado para renderização gráfica, controle de eventos, movimentação, colisões e animações.

### 🎤 Voz (Fala e Reconhecimento)
- **SpeechRecognition** — Captura o nome do jogador por **voz**.
- **pyttsx3** — Faz a **narração** de falas do jogo, como pontuação, boas-vindas e histórico.

### 💾 Armazenamento de Dados
- **SQLite (via sqlite3)** — Banco de dados usado para armazenar ranking e histórico.
- **JSON** — Usado para salvar logs e registros estruturados (ex: `log.dat`).

### 🪟 Interface Gráfica Temporária
- **Tkinter** — Utilizado para capturar o nome do jogador por texto (interface simples com botões e mensagens).

### 📚 Outras Bibliotecas
- `os`, `random`, `datetime` — Funções de sistema, aleatoriedade e data/hora.


## ✅ Funcionalidades Implementadas

- [x] Entrada de nome por **voz** ou **texto**
- [x] **Animação de boas-vindas**
- [x] Narração da história do jogo
- [x] Loop principal com movimentação, colisão e pontuação
- [x] Som de fundo e efeitos sonoros
- [x] **Pausa** com tecla ESPAÇO
- [x] Tela de **morte** com pontuação
- [x] Registro de **pontuação com data/hora**
- [x] Tela de **Ranking dos Top 5**
- [x] Tela de **Histórico das últimas 10 partidas**
- [x] Síntese de voz para feedback de ranking e histórico

---

## 🗂️ Organização

```
EspacoSideral/
│
├── main.py                   # Arquivo principal (esse que você está vendo)
├── recursos/
│   ├── funcoes.py            # Funções auxiliares para banco de dados
│   └── log.dat               # Registro de partidas (histórico em JSON)
│
├── assets/                   # Imagens e sons
│   ├── iron.png
│   ├── missile.png
│   ├── lua.png
│   ├── fundoStart.jpg
│   ├── fundoDead.png
│   ├── imagem_apresentacao.jpg
│   ├── ironsound.mp3
│   ├── missile.wav
│   └── explosao.wav
```

---

## 📌 Requisitos

- Python 3.8 ou superior
- Instalar as bibliotecas:
  ```bash
  pip install pygame pyttsx3 SpeechRecognition pyaudio
  ```

> ⚠️ Para o `SpeechRecognition`, você pode precisar instalar o `PyAudio`:
```bash
pip install pipwin
pipwin install pyaudio

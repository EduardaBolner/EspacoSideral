import os
import json
from datetime import datetime

ARQUIVO_DB = "dados_jogo.json"

def inicializarBancoDeDados():
    """Cria o arquivo JSON se não existir."""
    if not os.path.exists(ARQUIVO_DB):
        with open(ARQUIVO_DB, "w") as f:
            json.dump([], f)

def escreverDados(nome, pontos):
    """Salva os dados do jogador no JSON."""
    with open(ARQUIVO_DB, "r") as f:
        dados = json.load(f)

    novo = {
        "nome": nome,
        "pontos": pontos,
        "data": datetime.now().strftime("%d/%m/%Y"),
        "hora": datetime.now().strftime("%H:%M:%S")
    }
    dados.append(novo)

    with open(ARQUIVO_DB, "w") as f:
        json.dump(dados, f, indent=4)

def obterRanking():
    """Retorna os 5 melhores jogadores."""
    with open(ARQUIVO_DB, "r") as f:
        dados = json.load(f)

    ranking = sorted(dados, key=lambda x: x["pontos"], reverse=True)
    return ranking[:5]

def obterHistorico():
    """Retorna todo o histórico de partidas."""
    with open(ARQUIVO_DB, "r") as f:
        return json.load(f)

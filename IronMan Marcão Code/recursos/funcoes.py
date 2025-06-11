import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    print("dados",type(dados))
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo

import os
import json
from datetime import datetime

def inicializarBancoDeDados():
    if not os.path.exists("recursos"):
        os.makedirs("recursos")
    caminho = "recursos/logs.json"
    if not os.path.exists(caminho):
        with open(caminho, "w") as f:
            json.dump([], f)

def escreverDados(nome, pontos):
    dados = {
        "nome": nome,
        "pontos": pontos,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S")
    }
    caminho = "recursos/logs.json"
    with open(caminho, "r") as f:
        conteudo = json.load(f)
    conteudo.append(dados)
    with open(caminho, "w") as f:
        json.dump(conteudo, f, indent=4)

def obterRanking():
    caminho = "recursos/logs.json"
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r") as f:
        dados = json.load(f)
    dados.sort(key=lambda x: x["pontos"], reverse=True)
    return dados[:5]  # Top 5

def obterHistorico():
    caminho = "recursos/logs.json"
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r") as f:
        return json.load(f)

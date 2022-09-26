import random
import string
import time

import coloracao_baseline as cb
import coloracao_heuristica as ch
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def TransformaEntrada(entrada):
  reacoes = []
  vertices = []
  indice_reacoes = []
  df = pd.read_csv(entrada, sep=',', encoding='utf-8')
  elementos_quimicos = df['elementos_quimicos'].tolist()
  for i in elementos_quimicos:
    vertices.append(i.capitalize())

  for i in df['reacoes'].tolist():
    elementos = []
    for j in i.split(','):
      elementos.append(j.capitalize())
    reacoes.append(elementos)
    
  for i in reacoes:
    elementos = []
    for j in i:
      elementos.append(vertices.index(j))
    indice_reacoes.append(elementos)

  num_vertices = len(vertices)

  grafo = dict()
  for i in range(0, num_vertices):
      grafo[i] = indice_reacoes[i]

  return [grafo, vertices]

def GeraEntradas(n):
  dicionario = []
  for i in range(n):
        item = [i,[]]
        dicionario.append(item)
  vertices = []
  for i in range(n):
      aleatorio = random.randint(1, n-1)
      vertices.append(str(i))
      m=[]
      for j in range(aleatorio):
          adjascente = random.randint(1, aleatorio)
          if(adjascente != i):
                dicionario[adjascente][1].append(i)
                m.append(adjascente)
      dicionario[i][1].extend(m)

  for i in range(n):
      dicionario[i][1] = list(set(dicionario[i][1]))
      
  grafo = dict(dicionario)
  dados = [grafo,vertices]
  graus = [len(grafo[i]) for i in grafo]
  cor = np.zeros(shape=(len(vertices)))
  satur = np.zeros(shape=(len(vertices)))
  
  return [dados, graus, cor, satur]

def CoresParaOGrafo(solucao):
  lista_de_cores = ['red', 'green', 'blue', 'violet',
                    'yellow', 'pink', 'brown', 'black', 'white']
  cores = []
  for i in solucao[0]:
    cores.append(lista_de_cores[i])
  return cores

def ConverteVerticesEmDict(vertices):
  elemQuimicos = dict()
  for i in range(0, len(vertices)):
    elemQuimicos[i] = vertices[i]
  return elemQuimicos

def DefineResultado(solucao, vertices):
  mensagem = dict()
  sol = dict()
  for i in range(len(solucao[0])):
    sol[vertices[i]] = solucao[0][i]

  for i in range(0, len(set(solucao[0]))):
    lista_elem = []
    for j in sol.items():
      if i == j[1]:
        lista_elem.append(j[0])
        mensagem[i] = lista_elem

  return mensagem

def TransformaEmLetras(vertices):
  lista_alfabeto = string.ascii_uppercase
  vertices_letras = []
  for i in range(len(vertices)):
    vertices[i] = lista_alfabeto[i]
    vertices_letras.append(vertices[i])
  return vertices_letras

def time_milliseconds():
    tempo = time.time()*1000
    return tempo

def ColoreHeuristica(grafo, vertices, graus, cor, satur):
    inicio_ch = time_milliseconds()
    solucao_ch = ch.Dsatur(grafo,ch.ConverteMatrizAdj(grafo), cor, satur, len(vertices), graus)
    fim_ch = time_milliseconds()
    
    mensagem_ch = DefineResultado(solucao_ch, vertices)
    print('')
    print('Elementos químicos: {}'.format(vertices))
    print('Lista de cores: {}.'.format(solucao_ch[0]))
    print('Número cromático do grafo: {}.'.format(solucao_ch[1]))
    print('Tempo de execução: {} milissegundos.'.format(fim_ch-inicio_ch))
    print('')
    
    for i in mensagem_ch.items():
      print('Container {}, elementos químicos: {}'.format(i[0]+1,(i[1])))
      print('')
    grafo_colorido = nx.relabel_nodes(nx.from_dict_of_lists(grafo),
                         mapping=ConverteVerticesEmDict(vertices))
    nx.draw(grafo_colorido, node_color=CoresParaOGrafo(solucao_ch),
                         with_labels=True, node_size=1500)
    plt.show()
    
    return solucao_ch[1]
    
def ColoreBaseline(grafo, vertices):
    inicio_cb = time_milliseconds()
    solucao_cb = cb.VerificaSolucaoOtima(cb.ConverteMatrizAdj(grafo))
    fim_cb = time_milliseconds()
    
    mensagem_cb = DefineResultado(solucao_cb, vertices)
    print('')
    print('Elementos químicos: {}'.format(vertices))
    print('Lista de cores: {}.'.format(solucao_cb[0]))
    print('Número cromático do grafo: {}.'.format(solucao_cb[1]))
    print('Tempo de execução: {} milissegundos.'.format(fim_cb-inicio_cb))
    print('')
    for i in mensagem_cb.items():
      print('Container {}, elementos químicos: {}'.format(i[0]+1,(i[1])))
      print('')
    grafo_colorido = nx.relabel_nodes(nx.from_dict_of_lists(grafo),
                         mapping=ConverteVerticesEmDict(vertices))
    nx.draw(grafo_colorido, node_color=CoresParaOGrafo(solucao_cb),
                         with_labels=True, node_size=1500)
    plt.show()
    
def Main(n):
    dados, graus, cor, satur = GeraEntradas(n)
    #dados = TransformaEntrada('entrada.csv')
    grafo = dados[0]
    vertices = dados[1]
    try:
        vertices = TransformaEmLetras(vertices)
    except:
        pass
    ColoreBaseline(grafo, vertices)
    #graus = [len(grafo[i]) for i in grafo]
    #cor = np.zeros(shape=(len(vertices)))
    #satur = np.zeros(shape=(len(vertices)))
    ColoreHeuristica(grafo, vertices, graus, cor, satur)
    
Main(5)

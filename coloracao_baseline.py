from itertools import product

import numpy as np


def ConverteMatrizAdj(grafo):
  matriz = []
  for i in grafo.items():
      val = i[1]
      linha = np.zeros(shape=(len(grafo)))
      linha.put(val, 1)
      matriz.append(linha)
  return np.asarray(matriz)

def CriaAsCombinacoes(n_vertices):
  combinacoes = []
  max_combinacoes = product(list(range(0,n_vertices)), repeat=n_vertices)
  for combinacao in max_combinacoes:
      num_cores = len(set(combinacao))
      cores = list(range(0, num_cores))
      lista_cores = []
      for cor in cores:
        if cor in combinacao:
          lista_cores.append(cor)
      if len(lista_cores) == num_cores:
        combinacoes.append(combinacao)

  return combinacoes

def VerificaAsCombinacoes(matriz_adj, combinacoes):
  for i in range(len(matriz_adj)):
    for j in range(i+1, len(matriz_adj[i])):
      if (matriz_adj[i][j] != 0 and combinacoes[j] == combinacoes[i]):
          return False
  return True

def VerificaSolucaoOtima(matriz_adj):
    cores = CriaAsCombinacoes(len(matriz_adj))
    num_cores = len(matriz_adj)
    solucaoOtima = list(range(0, num_cores))
    for i in cores:
        combinacao_possivel = VerificaAsCombinacoes(matriz_adj, i)
        if combinacao_possivel == True:
          if num_cores > len(set(i)):
            num_cores = len(set(i))
            solucaoOtima = i
    return [solucaoOtima, num_cores]

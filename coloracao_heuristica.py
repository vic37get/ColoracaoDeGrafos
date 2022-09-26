import numpy as np


def ConverteMatrizAdj(grafo):
  matriz = []
  for i in grafo.items():
      val = i[1]
      linha = np.zeros(shape=(len(grafo)))
      linha.put(val, 1)
      matriz.append(linha)
  return np.asarray(matriz)

def VerificaCores(grafo, cor, indice_vertice, cores):
      for i in range(0, len(grafo[indice_vertice])):
            if (grafo[indice_vertice][i] != 0 and cor == cores[i]):
                  return False
            return True

def MaiorSaturacao(cor, len_satur, satur, graus):
      maior_saturação = -1
      indice_vertice = -1
      for j in range(0, len_satur):
            if(cor[j] == 0):
                  if(satur[j] > maior_saturação):
                        maior_saturação = satur[j]
                        indice_vertice = j
                  if(satur[j] == maior_saturação):
                        if(graus[j] >= graus[indice_vertice]):
                              indice_vertice = j
      return indice_vertice
  
def SaturacaoDoVertice(matriz_adj,cor,vertice):
    cores_saturacao = []
    for i in range(len(matriz_adj[vertice])):
          vertice_i = matriz_adj[vertice][i]
          if(vertice_i != 0):
                if(cor[int(i)] not in cores_saturacao and cor[int(i)] != 0):
                      cores_saturacao.append(cor[int(i)])
    return len(cores_saturacao)

def AtualizaSaturacao(grafo,cor,matriz_adj,ind,satur):
      for i in grafo[ind]:
            satur[i] = SaturacaoDoVertice(matriz_adj,cor,i)
            
def Dsatur (grafo, matriz_adj, cores, satur, n_vertices, graus):
      primeiro_vertice = graus.index(max(graus))
      cores[primeiro_vertice] = 1
      AtualizaSaturacao(grafo, cores, matriz_adj, primeiro_vertice, satur) #n
      for j in range(1, n_vertices): #n
            indice_vertice = MaiorSaturacao(cores, len(satur), satur,graus)#n
            indice_cor = 1
            while True: #n
                  if(VerificaCores(matriz_adj, indice_cor, indice_vertice, cores)):
                        cores[indice_vertice] = indice_cor
                        AtualizaSaturacao(grafo, cores,matriz_adj, indice_vertice, satur)
                        break
                  indice_cor += 1
      cores_dsatur = [tuple([int(j) for j in cores]),len(set(cores))]
      return cores_dsatur

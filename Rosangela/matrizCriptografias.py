# importando biblotecas 
# numpy para fazer operacoes com as matrizes
import numpy as np
# pra deixar um pouco mais interesante diferente do artiggo fornecido os indices sao aleatoris nesse codigo
import random

# Definição dos caracteres suportados
caracteres = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','.',',','_','¬',' ']

# Criando uma permutação aleatória dos índices
indices = random.sample(range(len(caracteres)), len(caracteres))
# fucao responsavel por capturar o index correspondente a cada caracter
def getIndex(Caracter):
    for caracter, index in zip(caracteres, indices):
        if Caracter == caracter:
            return index
    return None
# funcao responsavel por capturar o caracter responsavel por cada index
def getCaracter(Index):
    for caracter, index in zip(caracteres, indices):
        if Index == index:
            return caracter
    return None
# a mensagem e convertida em uma matriz correspondente aos indices criados acima
def criar_matriz(palavra):
    # o 'dicionario' esta em maiusculo...poderiamos criar um dicionario maior mas por via de simplicidade nao vem ao caso
    palavra = palavra.upper()
    # tam recebe a quamtidade de caracteres
    tam = len(palavra)
    tamanho_matriz = int(np.ceil(np.sqrt(tam)))  # Determina tamanho da matriz quadrada
    matriz = np.full((tamanho_matriz, tamanho_matriz), fill_value=' ')  # Preenche com espaços
    
    idx = 0
    for i in range(tamanho_matriz):
        for j in range(tamanho_matriz):
            if idx < tam:
                matriz[i][j] = palavra[idx]
                idx += 1
    return matriz

def criptografar(palavra):
    """ Converte a matriz da palavra em uma lista de índices criptografados """
    matriz = criar_matriz(palavra)
    matriz_indices = np.vectorize(getIndex)(matriz)  # Substitui caracteres pelos índices
    return matriz_indices.flatten().tolist()  # Retorna a matriz achatada

def descriptografar(codificada):
    """ Converte a lista de índices criptografados de volta para a palavra """
    tamanho_matriz = int(np.sqrt(len(codificada)))
    matriz = np.array(codificada).reshape((tamanho_matriz, tamanho_matriz))
    matriz_caracteres = np.vectorize(getCaracter)(matriz)  # Substitui índices pelos caracteres
    palavra = ''.join(matriz_caracteres.flatten())
    return palavra.strip().capitalize()

# Teste do código
mensagem = 'Mensagem a ser criptografada'
mensagem_codificada = criptografar(mensagem)
mensagem_decodificada = descriptografar(mensagem_codificada)

print(f'Índices de permutação: {indices}')
print(f'Mensagem original: {mensagem}')
print(f'Mensagem criptografada: {mensagem_codificada}')
print(f'Mensagem descriptografada: {mensagem_decodificada}')

'''
Instruções
Objetivos

 

·         Manipulação de Variáveis

·         Comando de Atribuição

·         Comando Condicional

·         Entrada e Saída de Dados

 

Introdução

 

A Páscoa é uma das festas móveis de várias religiões. Sua data varia a cada ano, e no mesmo ano de religião para religião. Por decreto do Concílio de Nicéis (ano 325), o dia da Páscoa deve ser celebrado no primeiro domingo depois da lua cheia que segue o equinócio de outono (21 de março). Todas as demais festas móveis do ano eclesiástico são estabelecidas a partir da fixação da data da Páscoa.

O algoritmo seguinte, do astrônomo Aloysius Lilius e do matemático Christopher Clavius, é usado para o cálculo da Páscoa de qualquer ano após 1582. Existem muitas indicações de que o cálculo da Páscoa foi a única aplicação importante da aritmética na Europa durante a Idade Média, razão do significado histórico deste algoritmo.

 

Definições

 

·         Equinócio: ponto da órbita da terra em que se registra uma igual duração do dia e da noite.

·         Epacta: número de dias que deve ser adicionado ao ano lunar para transformá-lo em ano solar.

 

Algoritmo

 

Seja Y o ano do qual se deseja a data da Páscoa.

Cálculo do Número Áureo (G): Seja G o resto da divisão inteira de Y por 19 acrescido de uma unidade.

Cálculo do Século (C): Seja C o quociente da divisão inteira de Y por 100 acrescido de 1.

Cálculo das Correções (X e Z): Seja X o quociente da divisão de 3*C por 4, menos 12 e Z o quociente da divisão de (8*C + 5) por 25, menos 5.

Cálculo do Epacta (E): Seja E o resto da divisão inteira de (11*G + 20 + Z - X) por 30. Se E = 25 e G > 11, ou se E = 24, então some 1 a E.

Cálculo da Lua Cheia: Seja N = 44 - E. Se N < 21, então faça N receber N + 30.

Cálculo do Domingo (D): Seja D o quociente da divisão inteira de 5*Y por 4, menos (X + 10). Faça N receber (N + 7) menos o resto da divisão de (D + N) por 7.

Cálculo do Mês: Se N > 31 a Páscoa será no dia (N - 31) de abril, caso contrário será em N de março.

 

Programa

 

Faça um programa para calcular a data da Páscoa de um ano fornecido pelo usuário.

O programa pode supor que o ano fornecido pelo usuário será sempre um inteiro maior que 1582. Ele deverá apenas imprimir a data da Páscoa, de acordo com o seguinte formato:

 

Pascoa: 23 de abril de 2000

 '''
#Ano escolhido esta na variavel Y
while True:
  Y = int(input("Digite o ano para calcular a data da pascoa(Esse ano deve ser superior a 1582:\n"))
  if Y > 1582:
    break
#G contem o numero Aureo 
G = (Y%19)+1
#C contem o Seculo
C = (Y//100)+1
#X e Z contem um calculo de correçoes 
X = ((3*C)/4)-12
Z = (8*C+5) / 25 - 5
#E contem empacta
E = (11*G+20+Z-X)%30
if (E==25 and G>11) or E==24:
  E+=1
#N contem a lua cheia  
N = 44-E
if N<21:
  N+=30
#D conte o domingo
D = (5*Y)//4-(X+10)

N = (N+7)-(D+N)%7
if N>31:
  dia = str(int(N-31))
  mes = "abril"
else:
  dia = str(int(N))
  mes = "Março"
#2016 tem que cair em 27 de março
print(f"Pascoa: {dia} de {mes} de {str(Y)}")


    
    
    
    
    

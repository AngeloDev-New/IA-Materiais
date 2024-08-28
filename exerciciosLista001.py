def getArea(frente,comprimento):
  return frente*comprimento

class Padaria():
  def __init__(self):
    lucro = int(input("Quantos paes franceses foram vendidos?"))*0.12+int(input("Quantas broas foram vendidas?"))*1.50
    self.lucro = f"{round(lucro,2)} reais"
    self.poupanca = f"{round(lucro*0.1,2)} reais"

class Pessoa():
  def __init__(self):
    self.nome = input("Qual o seu nome?").upper()
    self.dias_vida = int(input("Quantos anos voce tem?"))*365
class Exercicio5():
  def __init__(self):
    self.colete_dados()
    self.retorne()
  def colete_dados(self):
    self.valor_colocado = float(input("Quantos reais vai abastecer?").replace(",","."))
    self.valor_combustivel = float(input("Qual o valor do combustivel?").replace(",","."))
  def retorne(self):
    print(f"Serao colocados {str((self.valor_colocado/self.valor_combustivel).1f)} litros de combustivel")
if __name__ in "__main__":
  print("Exercicio 01")
  print("A area do terreno tem: ",getArea(float(input("Qual a frente do terreno?\n")),float(input("Qual o comprimento do terreno?\n"))))
  print("Exercicio 02")
  print("Voce vai precisar de ",int(input("Quantos cavalos ha no haras?:\n"))*4,"ferraduras para colocar em todos os cavalos")
  print("Exercicio 03")
  padaria = Padaria()
  print(f"O total em vendas foi {padaria.lucro}, e {padaria.poupanca} sera guardado")
  print("Exercicio 04")
  pessoa = Pessoa()
  print(f"{pessoa.nome} VOCE JA VIVEU {pessoa.dias_vida} DIAS")
  execicio5 = Exercicio5()
  





























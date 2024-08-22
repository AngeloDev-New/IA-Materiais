def getArea(frente,comprimento):
  return frente*comprimento

class Padaria():
  def __init__(self):
    lucro = int(imput("Quantos paes franceses foram vendidos?"))*0.12+int(imput("Quantas broas foram vendidas?"))*1.50
    self.lucro = f"{round(lucro,2)} reais"
    self.poupanca = f"{round(lucro*0.1,2)} reais"

if __name__ in "__main__":
  print("Exercicio 01")
  print("A area do terreno tem: ",getArea(float(imput("Qual a frente do terreno?\n")),float(imput("Qual o comprimento do terreno?\n"))))
  print("Exercicio 02")
  print("Voce vai precisar de ",int(imput("Quantos cavalos ha no haras?:\n))*4,"ferraduras para colocar em todos os cavalos")
  print("Exercicio 03")
  padaria = Padaria()
  print(f"O total em vendas foi {padaria.lucro}, e {padaria.poupanca} sera guardado")
  
  

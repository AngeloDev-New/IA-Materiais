# 1
def padrao1():
  for x in range(1,9):
    print("#"*x)
# 2
def padrao2():
  for x in range(8,0,-1):
    print("#"*x)
# 3
def padrao3():
  for y,x in enumerate(range(8,0,-1)):
    print(f"{' '*y}{'#'*x}")
  # 4
def padrao4():
  for x,y in enumerate(range(8,0,-1)):
    print(f"{' '*y}{'#'*x}")
def padrao5():
  for linha in range(8):
    for coluna in range(8):
      if linha == 0 or linha == 7 or linha == coluna:
        print("#",end="")
        continue
      else:
        print(" ",end="")
    print()
def padrao5():
  for linha in range(8):
    for coluna in range(8):
      if linha == 0 or linha == 7 or linha+coluna == 7:
        print("#",end="")
        continue
      else:
        print(" ",end="")
    print()
def padrao6():
  for linha in range(8):
    for coluna in range(8):
      if linha == 0 or linha == 7 or linha+coluna == 7 or linha == coluna:
        print("#",end="")
        continue
      else:
        print(" ",end="")
    print()
def padrao7():
  for linha in range(8):
    for coluna in range(8):
      if linha == 0 or linha == 7 or linha+coluna == 7 or linha == coluna or coluna == 0 or coluna == 7:
        print("#",end="")
        continue
      else:
        print(" ",end="")
    print()

import random
tabela_periodica = {
    "H": "Hidrogênio",
    "He": "Hélio",
    "Li": "Lítio",
    "Be": "Berílio",
    "B": "Boro",
    "C": "Carbono",
    "N": "Nitrogênio",
    "O": "Oxigênio",
    "F": "Flúor",
    "Ne": "Neônio",
    "Na": "Sódio",
    "Mg": "Magnésio",
    "Al": "Alumínio",
    "Si": "Silício",
    "P": "Fósforo",
    "S": "Enxofre",
    "Cl": "Cloro",
    "Ar": "Argônio",
    "K": "Potássio",
    "Ca": "Cálcio",
    "Sc": "Escândio",
    "Ti": "Titânio",
    "V": "Vanádio",
    "Cr": "Cromo",
    "Mn": "Manganês",
    "Fe": "Ferro",
    "Co": "Cobalto",
    "Ni": "Níquel",
    "Cu": "Cobre",
    "Zn": "Zinco",
    "Ga": "Gálio",
    "Ge": "Germânio",
    "As": "Arsênio",
    "Se": "Selênio",
    "Br": "Bromo",
    "Kr": "Criptônio",
    "Rb": "Rubídio",
    "Sr": "Estrôncio",
    "Y": "Ítrio",
    "Zr": "Zircônio",
    "Nb": "Nióbio",
    "Mo": "Molibdênio",
    "Tc": "Tecnécio",
    "Ru": "Rutênio",
    "Rh": "Ródio",
    "Pd": "Paládio",
    "Ag": "Prata",
    "Cd": "Cádmio",
    "In": "Índio",
    "Sn": "Estanho",
    "Sb": "Antimônio",
    "Te": "Telúrio",
    "I": "Iodo",
    "Xe": "Xenônio",
    "Cs": "Césio",
    "Ba": "Bário",
    "La": "Lantânio",
    "Ce": "Cério",
    "Pr": "Praseodímio",
    "Nd": "Neodímio",
    "Pm": "Promécio",
    "Sm": "Samário",
    "Eu": "Európio",
    "Gd": "Gadolínio",
    "Tb": "Térbio",
    "Dy": "Disprósio",
    "Ho": "Hólmio",
    "Er": "Érbio",
    "Tm": "Túlio",
    "Yb": "Itérbio",
    "Lu": "Lutécio",
    "Hf": "Háfnio",
    "Ta": "Tântalo",
    "W": "Tungstênio",
    "Re": "Rênio",
    "Os": "Ósmio",
    "Ir": "Irídio",
    "Pt": "Platina",
    "Au": "Ouro",
    "Hg": "Mercúrio",
    "Tl": "Tálio",
    "Pb": "Chumbo",
    "Bi": "Bismuto",
    "Po": "Polônio",
    "At": "Astato",
    "Rn": "Radônio",
    "Fr": "Frâncio",
    "Ra": "Rádio",
    "Ac": "Actínio",
    "Th": "Tório",
    "Pa": "Protactínio",
    "U": "Urânio",
    "Np": "Neptúnio",
    "Pu": "Plutônio",
    "Am": "Amerício",
    "Cm": "Cúrio",
    "Bk": "Berquélio",
    "Cf": "Califórnio",
    "Es": "Einstênio",
    "Fm": "Férmio",
    "Md": "Mendelévio",
    "No": "Nobélio",
    "Lr": "Laurêncio",
    "Rf": "Rutherfórdio",
    "Db": "Dúbnio",
    "Sg": "Seabórgio",
    "Bh": "Bóhrio",
    "Hs": "Hássio",
    "Mt": "Meitnério",
    "Ds": "Darmstádio",
    "Rg": "Roentgênio",
    "Cn": "Copernício",
    "Nh": "Nihônio",
    "Fl": "Fleróvio",
    "Mc": "Moscóvio",
    "Lv": "Livermório",
    "Ts": "Tenessino",
    "Og": "Oganessônio"
}
quantidade_elementos = len(tabela_periodica)
def QualNome():
  elemento = random.randint(0,quantidade_elementos)
  alternativaCerta = random.randint(0,4)
  elementos = list(tabela_periodica.items())
  alternativa = []
  for i in range(4):
    if i == alternativaCerta:
      alternativa.append(elemento)
      continue
    alternativa.append(random.randint(0,quantidade_elementos))


  print(f"Qual o nome do elemento {elementos[elemento][0]:}")
  print(f"A){elementos[alternativa[0]][1]}")
  print(f"B){elementos[alternativa[1]][1]}")
  print(f"C){elementos[alternativa[2]][1]}")
  print(f"D){elementos[alternativa[3]][1]}")
  resposta = input("R:").lower()
  match resposta:
    case 'a':
      if alternativaCerta == 0:
        return 1
      else:
        return 0
    case 'b':
      if alternativaCerta == 1:
        return 1
      else:
        return 0    
    case 'c':
      if alternativaCerta == 2:
        return 1
      else:
        return 0
    case 'd':
      if alternativaCerta == 3:
        return 1
      else:
        return 0

def QualCodigo():
  pass
contador = 0
while True:
  if QualNome():
    contador += 1
  else:
    break
print("Sua pontuacao e:",contador)




import random
descricoes_elementos = {
    "H": "O hidrogênio é o elemento mais abundante no universo, encontrado em estrelas e galáxias.",
    "He": "O hélio foi descoberto no Sol antes de ser encontrado na Terra e é usado em balões e dirigíveis.",
    "Li": "O lítio é extraído de salmoura em desertos como o Atacama e é amplamente usado em baterias.",
    "Be": "O berílio é extraído de minerais como berilo e crisoberilo, usado em ligas e dispositivos eletrônicos.",
    "B": "O boro é obtido de minerais como bórax e kernita, usado em vidros e detergentes.",
    "C": "O carbono existe em várias formas, como grafite e diamante, e é essencial para toda a vida.",
    "N": "O nitrogênio é extraído do ar e utilizado em fertilizantes, bem como em processos industriais.",
    "O": "O oxigênio é o segundo elemento mais abundante na atmosfera terrestre e essencial para a respiração.",
    "F": "O flúor é encontrado em minerais como fluorita e é utilizado em pastas de dentes e água fluoretada.",
    "Ne": "O neônio é extraído do ar e é famoso por seu uso em sinais luminosos.",
    "Na": "O sódio é obtido de sais como o sal-gema e é um elemento fundamental na química industrial.",
    "Mg": "O magnésio é extraído de minerais como dolomita e é utilizado em ligas leves para a aviação.",
    "Al": "O alumínio é obtido da bauxita e é o metal mais utilizado na indústria devido à sua leveza.",
    "Si": "O silício é extraído de areia e é a base para a fabricação de semicondutores e eletrônicos.",
    "P": "O fósforo é encontrado em depósitos de fosfatos e é utilizado em fertilizantes e produtos químicos.",
    "S": "O enxofre é extraído de depósitos vulcânicos e usado principalmente na fabricação de ácido sulfúrico.",
    "Cl": "O cloro é obtido por eletrólise de cloreto de sódio e é usado em purificação de água.",
    "Ar": "O argônio é obtido do ar e é usado em lâmpadas incandescentes e soldagem a gás inerte.",
    "K": "O potássio é extraído de sais potássicos e é utilizado em fertilizantes e produtos químicos.",
    "Ca": "O cálcio é encontrado em rochas como o calcário e é vital para ossos e dentes.",
    "Sc": "O escândio é um elemento raro encontrado em minerais na Escandinávia, utilizado em ligas leves.",
    "Ti": "O titânio é extraído de minerais como rutilo e é amplamente utilizado em ligas e implantes.",
    "V": "O vanádio é encontrado em minerais como vanadinita e é utilizado em ligas de alta resistência.",
    "Cr": "O cromo é extraído de cromita e é essencial para a fabricação de aço inoxidável.",
    "Mn": "O manganês é utilizado principalmente na produção de aço, extraído de minérios como pirolusita.",
    "Fe": "O ferro é o metal mais utilizado na Terra, extraído de hematita e magnetita.",
    "Co": "O cobalto é extraído como subproduto da mineração de cobre e níquel, e é usado em baterias.",
    "Ni": "O níquel é encontrado em depósitos de sulfetos, amplamente utilizado em ligas e moedas.",
    "Cu": "O cobre é extraído de minérios como calcopirita e é amplamente utilizado na eletrônica.",
    "Zn": "O zinco é extraído de esfalerita e é utilizado para galvanização do aço e em ligas metálicas.",
    "Ga": "O gálio é obtido como subproduto da mineração de alumínio e é usado em LEDs e dispositivos eletrônicos.",
    "Ge": "O germânio é extraído de minérios de zinco e é utilizado em semicondutores e fibras ópticas.",
    "As": "O arsênio é encontrado em minérios de cobre e é conhecido historicamente por ser tóxico.",
    "Se": "O selênio é um subproduto da mineração de cobre e é usado em células fotovoltaicas e vidros.",
    "Br": "O bromo é extraído de águas salgadas e é utilizado em retardantes de chama.",
    "Kr": "O criptônio é obtido do ar e é usado em lâmpadas fluorescentes e fotografia.",
    "Rb": "O rubídio é encontrado em minerais como lepidolita e é usado em pesquisa científica.",
    "Sr": "O estrôncio é extraído de celestita e é utilizado em fogos de artifício para criar cores vermelhas.",
    "Y": "O ítrio é encontrado em minérios de terras-raras e é utilizado em lasers e fósforos.",
    "Zr": "O zircônio é extraído de minerais como zircão e é utilizado em reatores nucleares.",
    "Nb": "O nióbio é extraído de minérios no Brasil e é utilizado em ligas de aço.",
    "Mo": "O molibdênio é extraído de molibdenita e é utilizado como endurecedor de aço.",
    "Tc": "O tecnécio foi o primeiro elemento produzido artificialmente e é utilizado em medicina nuclear.",
    "Ru": "O rutênio é encontrado em minérios de platina e é utilizado em contatos elétricos.",
    "Rh": "O ródio é extraído de minérios de platina e é utilizado em catalisadores automotivos.",
    "Pd": "O paládio é encontrado em depósitos de platina e é usado em eletrônica e na indústria automotiva.",
    "Ag": "A prata é extraída de minérios como argentita e é amplamente usada em joias e eletrônica.",
    "Cd": "O cádmio é um subproduto da mineração de zinco e é utilizado em baterias e pigmentos.",
    "In": "O índio é extraído como subproduto da mineração de zinco e é usado em telas de LCD.",
    "Sn": "O estanho é extraído de cassiterita e é usado para fabricar ligas como o bronze.",
    "Sb": "O antimônio é encontrado em estibinita e é utilizado em baterias e retardantes de chama.",
    "Te": "O telúrio é um subproduto da mineração de cobre e é utilizado em painéis solares.",
    "I": "O iodo é extraído de salmoura e é essencial para a produção de hormônios da tireoide.",
    "Xe": "O xenônio é obtido do ar e é utilizado em lâmpadas de alta intensidade e lasers.",
    "Cs": "O césio é extraído de minerais como pollucita e é utilizado em relógios atômicos.",
    "Ba": "O bário é extraído de barita e é usado em radiografias e na fabricação de fogos de artifício.",
    "La": "O lantânio é extraído de minérios de terras-raras e é utilizado em lentes de câmeras e catalisadores.",
    "Ce": "O cério é o mais abundante dos elementos de terras-raras e é utilizado em catalisadores e polidores.",
    "Pr": "O praseodímio é encontrado em minérios de terras-raras e é utilizado em imãs e vidros ópticos.",
    "Nd": "O neodímio é utilizado em imãs poderosos, principalmente em motores e eletrônicos.",
    "Pm": "O promécio é um elemento raro e radioativo utilizado em baterias nucleares.",
    "Sm": "O samário é encontrado em minérios de terras-raras e é utilizado em imãs e reatores nucleares.",
    "Eu": "O európio é utilizado em fósforos para televisores e lâmpadas fluorescentes.",
    "Gd": "O gadolínio é utilizado em materiais de contraste para exames de ressonância magnética.",
    "Tb": "O térbio é utilizado em fósforos de lâmpadas fluorescentes e tubos de raios catódicos.",
    "Dy": "O disprósio é utilizado em imãs e materiais de ressonância magnética.",
    "Ho": "O hólmio é utilizado em lasers e equipamentos médicos.",
    "Er": "O érbio é utilizado em fibras ópticas e lasers médicos.",
    "Tm": "O túlio é um elemento raro utilizado em dispositivos de raios-X portáteis.",
    "Yb": "O itérbio é utilizado em lasers e como dopante para fibras ópticas.",
    "Lu": "O lutécio é o elemento mais pesado das terras-raras e é utilizado em pesquisas nucleares.",
    "Hf": "O háfnio é utilizado em ligas resistentes ao calor e em reatores nucleares.",
    "Ta": "O tântalo é utilizado em capacitores eletrônicos e dispositivos médicos.",
    "W": "O tungstênio é conhecido por seu ponto de fusão alto e é utilizado em lâmpadas e ferramentas.",
    "Re": "O rênio é um elemento raro utilizado em ligas para motores de aviões.",
    "Os": "O ósmio é o metal mais denso e é utilizado em canetas e contatos elétricos.",
    "Ir": "O irídio é um metal denso utilizado em ligas para contatos elétricos e equipamentos médicos.",
    "Pt": "A platina é amplamente utilizada em joias, eletrônica e como catalisador.",
    "Au": "O ouro é um metal precioso utilizado em joias, eletrônica e como reserva de valor.",
    "Hg": "O mercúrio é o único metal líquido à temperatura ambiente e é utilizado em termômetros e lâmpadas.",
    "Tl": "O tálio é um elemento tóxico utilizado em eletrônica e vidros especiais.",
    "Pb": "O chumbo é utilizado em baterias, blindagem contra radiação e ligas metálicas.",
    "Bi": "O bismuto é um metal pesado não tóxico utilizado em medicamentos e cosméticos.",
    "Po": "O polônio é um elemento radioativo utilizado em dispositivos antiestáticos e pesquisa nuclear.",
    "At": "O astato é o elemento mais raro da Terra e é utilizado em pesquisas médicas e nucleares.",
    "Rn": "O radônio é um gás radioativo presente no solo, conhecido por seu risco à saúde.",
    "Fr": "O frâncio é um elemento extremamente raro e radioativo, com pouco uso prático.",
    "Ra": "O rádio foi usado em tratamentos médicos, mas sua radioatividade perigosa restringiu seu uso.",
    "Ac": "O actínio é utilizado em pesquisas nucleares e em tratamentos de câncer.",
    "Th": "O tório é utilizado em reatores nucleares e em ligas resistentes ao calor.",
    "Pa": "O protactínio é um elemento raro e radioativo, com usos limitados em pesquisa.",
    "U": "O urânio é o principal combustível para reatores nucleares e armas nucleares.",
    "Np": "O netúnio é um subproduto de reatores nucleares, utilizado em pesquisas e detecção de nêutrons.",
    "Pu": "O plutônio é utilizado em reatores nucleares e armas nucleares.",
    "Am": "O amerício é utilizado em detectores de fumaça e em radiografia.",
    "Cm": "O cúrio é utilizado em geradores termoelétricos de radioisótopos.",
    "Bk": "O berquélio é utilizado em pesquisas nucleares e na síntese de novos elementos.",
    "Cf": "O califórnio é utilizado em detectores de nêutrons e tratamentos de câncer.",
    "Es": "O einstênio é um elemento raro, utilizado em pesquisas científicas.",
    "Fm": "O férmio é um elemento altamente radioativo, com uso limitado em pesquisas nucleares.",
    "Md": "O mendelévio é utilizado em pesquisas sobre síntese de novos elementos.",
    "No": "O nobélio é um elemento radioativo, com usos limitados em pesquisa.",
    "Lr": "O laurêncio é um elemento sintético, com pouca aplicação prática.",
    "Rf": "O rutherfórdio é um elemento sintético e altamente radioativo, com aplicações limitadas à pesquisa científica, especialmente em estudos sobre a estrutura dos núcleos atômicos.",
    "Db": "O dúbnio é um elemento sintético, produzido pela primeira vez em Dubna, Rússia. Ele é utilizado em pesquisas sobre propriedades químicas e nucleares",
    "Sg": " Nomeado em homenagem ao cientista Glenn T. Seaborg, o seabórgio é um elemento sintético e radioativo, usado principalmente para pesquisas científicas em química nuclear.",
    "Bh": "Nomeado em homenagem a Niels Bohr, o bóhrio é um elemento altamente instável e radioativo. É utilizado exclusivamente em pesquisas científicas devido à sua vida extremamente curta",
    "Hs": "O hássio é um elemento sintético e altamente radioativo, produzido em aceleradores de partículas. Ele é utilizado para estudos sobre elementos superpesados e suas propriedades",
    "Mt": "O meitnério é um elemento sintético extremamente instável e radioativo, utilizado em pesquisas científicas. Foi nomeado em homenagem a Lise Meitner, uma pioneira na física nuclear",
    "Ds": "O darmstádio é um elemento sintético criado pela primeira vez na cidade de Darmstadt, Alemanha. Ele é radioativo e tem aplicações limitadas à pesquisa em química de elementos superpesados.",
    "Rg": "Nomeado em homenagem a Wilhelm Röntgen, o descobridor dos raios X, o roentgênio é um elemento sintético com uma vida extremamente curta, utilizado apenas em pesquisas científicas.",
    "Cn": "O copernício foi nomeado em homenagem a Nicolau Copérnico. É um elemento sintético e altamente instável, utilizado em pesquisas sobre as propriedades de elementos superpesados.",
    "Nh": "O nihônio é um elemento sintético, nomeado em homenagem ao Japão (Nihon em japonês). Ele é extremamente instável e utilizado apenas em pesquisas científicas.",
    "Fl": "O fleróvio é um elemento sintético, com nome em homenagem ao laboratório Flerov, na Rússia. Ele é altamente instável e utilizado em pesquisas sobre a química de elementos superpesados.",
    "Mc": "Nomeado em homenagem a Moscou, o moscóvio é um elemento sintético altamente radioativo, utilizado em pesquisas sobre elementos superpesados",
    "Lv": "O livermório é um elemento sintético, com nome em homenagem ao Laboratório Nacional Lawrence Livermore, nos EUA. Ele é utilizado em pesquisas sobre elementos superpesados",
    "Ts": "Nomeado em homenagem ao estado americano do Tennessee, o tenessino é um elemento sintético altamente instável, com aplicações limitadas a pesquisas científicas.",
    "Og": "Oganessônio, o elemento mais pesado conhecido, é nomeado em homenagem ao físico russo Yuri Oganessian. É altamente instável e existe apenas por frações de segundo, sendo utilizado exclusivamente em pesquisas nucleares."
}
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
  alternativaCerta = random.randint(0,3)
  elementos = list(tabela_periodica.items())
  alternativa = []
  for i in range(4):
    if i == alternativaCerta:
      alternativa.append(elemento)
      continue
    alternativa.append(random.randint(0,quantidade_elementos))


  print(f"Qual o nome do elemento {elementos[elemento][0]}")
  print(f"A){elementos[alternativa[0]][1]}")
  print(f"B){elementos[alternativa[1]][1]}")
  print(f"C){elementos[alternativa[2]][1]}")
  print(f"D){elementos[alternativa[3]][1]}")
  resposta = input("R:").lower()
  match resposta:
    case 'a':
      if alternativaCerta == 0:
        print(f"Correto, {descricoes_elementos[elementos[elemento][0]]}")
        return 1
      else:
        print(f"Errado, {descricoes_elementos[elementos[elemento][0]]}")
        
        return 0

    case 'b':
      if alternativaCerta == 1:
        print(f"Correto, {descricoes_elementos[elementos[elemento][0]]}")

        return 1
      else:
        print(f"Errado, {descricoes_elementos[elementos[elemento][0]]}")

        return 0    
    case 'c':
      if alternativaCerta == 2:
        print(f"Correto, {descricoes_elementos[elementos[elemento][0]]}")

        return 1
      else:
        print(f"Errado, {descricoes_elementos[elementos[elemento][0]]}")

        return 0
    case 'd':
      if alternativaCerta == 3:
        print(f"Correto, {descricoes_elementos[elementos[elemento][0]]}")

        return 1
      else:
        print(f"Errado, {descricoes_elementos[elementos[elemento][0]]}")

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



import scrapy
import requests
import csv
import time
import random

verde = '\033[92m'
amarelo = '\033[93m'
vermelho = '\033[91m'
azul = '\033[94m'
fim = '\033[0m'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/128.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
]

dados_coletados_geral = []

print(f'{azul}\n------------------Iniciado Imobiliária Maximize------------------{fim}')
contador_imoveis = 0
pagina = 1

while True:
    print(f"{azul}Coletando página: {pagina}{fim}")
    url_geral = f'https://www.maximizeimobiliaria.com.br/filtro2/list/locacao/todos/todas/todos/0-10000000/todos/{pagina}/ASC'
    random_user_agent = random.choice(user_agents)
    headers = {"User-Agent": random_user_agent}

    try:
        html_content = requests.get(url_geral, headers = headers, timeout=20).text
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        print(f"{amarelo}Erro de conexão/timeout na página {pagina}. Tentando novamente em 7 segundos...{fim}")
        time.sleep(7)
        continue

    time.sleep(random.uniform(2, 5))
    response = scrapy.http.HtmlResponse(url = url_geral, body = html_content, encoding = "utf-8")

    imoveis_na_pagina = response.css("div.card-property-exebicao.raw-exebicao.w-dyn-item")
    if len(imoveis_na_pagina) == 0:
        break

    for imovel in imoveis_na_pagina:
        contador_imoveis += 1

        titulo = imovel.css("h5.heading-2-exebicao::text").get()

        tipo = None
        if "Apartamento" or "Casa" or "Sobrado" in titulo:
            tipo = "Residencial"
        elif "Barracão" in titulo:
            tipo = "Barracão" 
        elif "Sala" in titulo:
            tipo = "Sala Comercial"
        else:
            tipo = "Não identificado"

        dados_coletados_geral.append({
            "Titulo do imóvel": titulo,
            "Tipo do imóvel": tipo,
            "Preço": None,
            "Valor Condomínio": None,
			"Bairro": imovel.css("div.card-property-description-exebicao>div::text").get(),
    		"Link para o anúncio": imovel.css("div.slide-exebicao.w-slide>a::attr(href)").get(),
            "Origem": 'Maximize Imobiliária',
            "Quartos": None,
            "Suítes": None,
            "Área do imóvel": None
        })
        print(f"{contador_imoveis}.{verde} Coletado:", titulo, f'{fim}')
        # time.sleep(0.5)
    time.sleep(1)
    pagina += 1
    break
time.sleep(2)

print(f'{azul}Coletados {contador_imoveis} imóveis da Imobiliária Maximize{fim}')

i = 0#contador_imoveis

while i <= len(dados_coletados_geral) - 1:
    imovel = dados_coletados_geral[i]

    url = imovel['Link para o anúncio']
    random_user_agent = random.choice(user_agents)
    headers = {"User-Agent": random_user_agent}

    try:
        html_content = requests.get(url, headers = headers, timeout=10).text
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        print(f"{amarelo}Erro de conexão/timeout no imóvel {i+1}. Tentando novamente em 5 segundos...{fim}")
        # time.sleep(5)
        continue

    time.sleep(random.uniform(1, 2.5))    
    response = scrapy.http.HtmlResponse(url = url, body = html_content, encoding = "utf-8")

    for dados in response.css("ul.details-list-item-grid-exebicao"):
        quartos = dados.xpath('./li/div[contains(text(), "Quarto(s)")]/strong/following-sibling::text()').get()
        if quartos != None:
            imovel["Quartos"] = quartos
        else:
            imovel["Quartos"] = 0

    for dados in response.css("ul.details-list-item-grid-exebicao"):
        suites = dados.xpath('./li/div[contains(text(), "Suíte(s)")]/strong/following-sibling::text()').get()
        if suites != None:
            imovel["Suítes"] = suites
        else:
            imovel["Suítes"] = 0
        
    for dados in response.css("ul.details-list-item-grid-exebicao"):
        area = dados.xpath('./li/div[contains(text(), "Área Total")]/strong/following-sibling::text()').get()
        if area != None:
            imovel["Área do imóvel"] = dados.xpath('./li/div[contains(text(), "Área Total")]/strong/following-sibling::text()').get()
    
    print(f"{i+1-contador_imoveis}/{contador_imoveis}{verde} Coletado dados específicos de", dados_coletados_geral[i]["Titulo do imóvel"], f'{fim}')
    i += 1
    # time.sleep(0.5)
# time.sleep(1)

print(f'\n{azul}------------------Finalizado Imobiliária Maximize------------------{fim}')

with open("dados_scraper.csv", "w", newline = "", encoding = "utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Titulo do imóvel", "Tipo", "Preço", 'Valor Condominio', "Quartos", "Suítes", 'Área Total', "Bairro", "Link para o anúncio", 'Origem'])
    for dado in dados_coletados_geral:
        writer.writerow([dado["Titulo do imóvel"], dado["Tipo do imóvel"], dado["Preço"], dado["Valor Condomínio"], dado["Quartos"], dado["Suítes"], dado["Área do imóvel"], dado["Bairro"], dado["Link para o anúncio"], dado['Origem']])
    print(f"{verde}Salvo em CSV!{fim}")

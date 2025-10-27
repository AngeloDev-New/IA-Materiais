import scrapy
import requests
import csv
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

verde = '\033[92m'
amarelo = '\033[93m'
vermelho = '\033[91m'
azul = '\033[94m'
fim = '\033[0m'

dados_coletados_geral = []

print(f'{azul}\n------------------Iniciado Imobiliária Giaretta------------------{fim}')

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/128.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
]

pagina = 1
contador_imoveis = 0

while True:
    url_geral = f'https://www.imobiliariagiaretta.com.br/locacao/todos/todas/todos/todos----todos/todos/todos---todos/lin/{pagina}?busca=1&exi=col&ord=asc&suites=0&'
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

    imoveis_na_pagina = response.css("div.div-block-71.lin")
    if len(imoveis_na_pagina) == 0:
        break

    print(f"{azul}Coletando página: {pagina}{fim}")

    for imovel in imoveis_na_pagina:
        contador_imoveis += 1

        bairro = imovel.css("div.text-block-5.fullcard::text").get().split()
        bairro = ' '.join(bairro[:-1]).lower()

        titulo = imovel.css("div.text-block-5.fullcard.titulo::text").get().split(",")[0]

        tipo = None
        if "Barracão" in titulo:
            tipo = "Barracão"
        elif "Terreno" in titulo:
            tipo = 'Terreno'
        elif "Comercial" in titulo:
            tipo = "Sala Comercial"
        elif "Casa" or "Sobrado" or "Apartamento" in titulo:
            tipo = "Residencial"
        else:
            tipo = "Não Identificado"

        dados_coletados_geral.append({
            "Titulo do imóvel": titulo,
            "Tipo do imóvel": tipo,
            "Preço": None,
            "Valor Condomínio": None,
			"Bairro": bairro,
    		"Link para o anúncio": imovel.css("a.link-imovel::attr(href)").get(), 
            "Origem": 'Giaretta',
            "Quartos": None,
            "Suítes": None,
            "Área do imóvel": None
        })
        print(f"{contador_imoveis}.{verde} Coletado:", titulo, f'{fim}')
        time.sleep(0.5)
    time.sleep(1)
    pagina += 1

print(f'{azul}Coletados {contador_imoveis} imóveis da Imobiliária Giaretta{fim}')

i = 0
while i <= len(dados_coletados_geral) - 1:
    imovel = dados_coletados_geral[i]

    url = imovel['Link para o anúncio']
    random_user_agent = random.choice(user_agents)

    try:
        html_content = requests.get(url, headers = headers, timeout=10).text
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        print(f"{amarelo}Erro de conexão/timeout no imóvel {i+1}. Tentando novamente em 5 segundos...{fim}")
        time.sleep(5)
        continue

    html_content= requests.get(url, headers = headers).text
    time.sleep(random.uniform(1, 2)) 
    response = scrapy.http.HtmlResponse(url = url, body = html_content, encoding = "utf-8")

    preco = None
    for dados in response.css("div.grid-soma"):
        preco = dados.xpath('.//div[contains(text(), "Locação:")]/following-sibling::div[1]/text()').get()
        if preco != None:
            preco = int(preco.split()[1].replace('.', '')[:-3])
            imovel["Preço"] = preco
            condominio = dados.xpath('.//div[contains(text(), "Condomínio")]/following-sibling::div[1]/text()').get()
            if condominio != None:
                condominio = int(condominio.split()[1].replace('.', '')[:-3])
                imovel["Valor Condomínio"] = condominio
                break
            else:
                imovel["Valor Condomínio"] = 0
                break
    if preco == None:
        for dados in response.css("div.camp-infos-vallue"):
            preco = dados.xpath('.//div[contains(text(), "R$")]/text()').get()
            if preco != None:
                preco = int(preco.split()[1].replace('.', '')[:-3])
                imovel["Preço"] = preco
                imovel["Valor Condomínio"] = 0
                break

    quartos = None
    for dados in response.css("div.w-col.w-col-6"):
        quartos = dados.xpath('.//div[contains(text(), "Quarto(s)")]/text()').get()
        if quartos != None:
            quartos = int(quartos.split()[0])
            imovel["Quartos"] = quartos
            break
    if quartos == None:  
        imovel["Quartos"] = 0
    
    suites = None
    for dados in response.css("div.w-col.w-col-6"):
        suites = dados.xpath('.//div[contains(text(), "Suíte(s)")]/text()').get()
        if suites != None:
            suites = int(suites.split()[0])
            imovel["Suítes"] = suites
            break
    if suites == None:
        imovel["Suítes"] = 0

    area_imovel = None
    for dados in response.css("div.w-col.w-col-6"):
        area_imovel = dados.xpath('.//div[contains(text(), "Total")]/text()').get()
        if area_imovel != None:
            area_imovel = float(area_imovel.split()[0].replace('.' , '').replace(',', '.'))
            imovel["Área do imóvel"] = area_imovel
            break
    if area_imovel == None:
        for dados in response.css("div.w-col.w-col-6"):
            area_imovel = dados.xpath('.//div[contains(text(), "(m²)")]/text()').get()
            if area_imovel != None:
                area_imovel = float(area_imovel.split()[0].replace('.' , '').replace(',', '.'))
                imovel["Área do imóvel"] = area_imovel
                break

    print(f"{i+1}/{contador_imoveis}{verde} Coletado dados específicos:", dados_coletados_geral[i]["Titulo do imóvel"], f'{fim}')
    time.sleep(0.5)
    i += 1

print(f'\n{azul}------------------Finalizado Imobiliária Giaretta------------------{fim}')

contador_imoveis = 0
pagina = 1

print(f'{azul}------------------Iniciado Imobiliária Aliança------------------{fim}\n')

while True:
    url_geral = f'https://www.imobiliariaaliancatoledo.com.br/filtro/locacao/todos/todas/todos/todos/1/{pagina}'
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

    imoveis_na_pagina = response.css("div.div-block-61.teste2")
    if len(imoveis_na_pagina) == 0:
        break

    print(f"{azul}Coletando página: {pagina}{fim}")

    for imovel in imoveis_na_pagina:
        contador_imoveis += 1

        tipo = imovel.css("div.text-block-35::text").get()

        if tipo == 'CASA' or tipo == "APARTAMENTO":
            tipo = "Residencial"
        elif tipo == "ÁREA INDUSTRIAL" or tipo == 'BARRACÃO':
            tipo = "Barracão"
        elif tipo == 'COMÉRCIO' or tipo == 'SALA COMERCIAL':
            tipo = 'Sala Comercial'
        elif tipo == 'TERRENO':
            tipo = 'Terreno'
        else:
            tipo = 'Não Identificado'

        dados_coletados_geral.append({
            "Titulo do imóvel": imovel.css("div.text-block-36::text").get(),
            "Tipo do imóvel": tipo,
            "Preço": None,
            "Valor Condomínio": None,
			"Bairro": None,
    		"Link para o anúncio": imovel.css("a.link-block-13.w-inline-block::attr(href)").get(), 
            "Origem": 'Aliança',
            "Quartos": None,
            "Suítes": None,
            "Área do imóvel": None
        })
        print(f"{contador_imoveis}.{verde} Coletado:", imovel.css("div.text-block-36::text").get(), f'{fim}')
        time.sleep(0.5)
    time.sleep(1)
    pagina += 1

print(f'{azul}Coletados {contador_imoveis} imóveis da Imobiliária Aliança{fim}')

i = len(dados_coletados_geral) - contador_imoveis
contador_atual = 1

while i <= len(dados_coletados_geral) - 1:
    imovel = dados_coletados_geral[i]

    url = imovel['Link para o anúncio']
    random_user_agent = random.choice(user_agents)
    headers = {"User-Agent": random_user_agent}
    
    try:
        html_content = requests.get(url, headers = headers, timeout=10).text
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        print(f"{amarelo}Erro de conexão/timeout no imóvel {i+1}. Tentando novamente em 5 segundos...{fim}")
        time.sleep(5)
        continue

    time.sleep(random.uniform(1, 2))
    response = scrapy.http.HtmlResponse(url = url, body = html_content, encoding = "utf-8")

    preco = None
    for dados in response.css("div.text-block-16"):
        preco = dados.xpath('./text()').getall()
        for a in preco:
            if '$' in a:
                preco = int(a.split('$')[1].split()[0].replace('.', '')[:-3])
                imovel["Preço"] = preco
                break

    valor_condominio = None
    for dados in response.css("div.text-block-16"):
        valor_condominio = dados.xpath('./div/text()').get()
        if valor_condominio != None:
            valor_condominio = int(valor_condominio.strip().split()[-1].replace('.', '')[:-3])
            if valor_condominio < preco:
                imovel["Valor Condomínio"] = valor_condominio
                break
    if valor_condominio == None:
        imovel["Valor Condomínio"] = 0

    for dados in response.css('div.div-block-29'):
        area = dados.xpath('.//div[contains(text(), "Terreno")]/preceding-sibling::div[1]/text()').get()
        if area != None:
            area = float(area.replace(',','.'))
            imovel["Área do imóvel"] = area
            break
        else:
            area = dados.xpath('.//div[contains(text(), "Útil")]/preceding-sibling::div[1]/text()').get()
            if area != None:
                area = float(area.replace(',','.'))
                imovel["Área do imóvel"] = area
                break
            else:
                area = dados.xpath('.//div[contains(text(), "(m²)")]/preceding-sibling::div[1]/text()').get()
                if area != None:
                    area = float(area.replace(',','.'))
                    imovel["Área do imóvel"] = area
                    break

    quartos = None
    for dados in response.css('div.div-block-29'):
        quartos = dados.xpath('.//div[contains(text(), "Quarto(s)")]/preceding-sibling::div[1]/text()').get()
        if quartos != None:
            quartos = int(quartos)
            imovel["Quartos"] = quartos
            break
    if quartos == None:
        imovel["Quartos"] = 0

    suites = None
    for dados in response.css('div.div-block-29'):
        suites = dados.xpath('.//div[contains(text(), "Suíte(s)")]/preceding-sibling::div[1]/text()').get()
        if suites != None:
            suites = int(suites)
            imovel["Suítes"] = suites
            break
    if suites == None:
        imovel["Suítes"] = 0

    for dados in response.css("div.text-block-19"):
        bairro = dados.xpath('./text()').get().lower()
        imovel["Bairro"] = bairro
        break 

    print(f"{contador_atual}/{contador_imoveis}{verde} Coletado dados específicos de", imovel["Titulo do imóvel"], f'{fim}')
    i += 1
    contador_atual += 1
    time.sleep(0.5)

print(f'\n{azul}------------------Finalizado Imobiliária Aliança------------------{fim}')

contador_imoveis = 0
pagina = 1

print(f'{azul}------------------Iniciado Imobiliária La Salle------------------{fim}\n')

while True:
    url_geral = f"https://www.imobiliarialasalle.com.br/filtro/locacao/todos/todas/todos/todos/todos/{pagina}"
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

    imoveis_na_pagina = response.css("div.div-block-61.teste2")
    if len(imoveis_na_pagina) == 0:
        break

    print(f"{azul}Coletando página: {pagina}{fim}")

    for imovel in response.css("div.div-block-61.teste2"):
        contador_imoveis += 1

        tipo = (imovel.css("div.text-block-update1::text").get() or "").upper()
        if "BARRACÃO" in tipo:
            tipo = "Barracão"
        elif "Terreno" in tipo:
            tipo = 'Terreno'
        elif "LOJA" or "SALA COMERCIAL" in tipo:
            tipo = "Sala Comercial"
        elif "CASA" or "SOBRADO" or "APARTAMENTO" in tipo:
            tipo = "Residencial"
        else:
            tipo = "Não Identificado"
    
        bairro = (imovel.css("div.text-block-2-update1::text").get() or "")

        preco = int(imovel.css("span.text-span-value::text").get().replace("R$", "").replace(".", "")[:-3])

        link = imovel.css("a.link-block-update1.w-inline-block::attr(href)").get()
        
        titulo_temp = link.split('/')[-2].replace('-', ' ')

        dados_coletados_geral.append({
            "Tipo do imóvel": tipo,
            "Bairro": bairro,
            "Preço": preco,
            "Link para o anúncio": link,
            "Titulo do imóvel": None,
            "Quartos": None,
            "Valor Condomínio": None,
            "Suíte": None,
            "Área do imóvel": None,
            "Origem": "La Salle"
        })

        print(f"{contador_imoveis}.{verde} Coletado: {titulo_temp}{fim}")
        time.sleep(0.5)
    time.sleep(1)
    pagina += 1

print(f'{azul}Coletados {contador_imoveis} imóveis da Imobiliária La Salle{fim}')

i = len(dados_coletados_geral) - contador_imoveis
contador_atual = 1

while i <= len(dados_coletados_geral) - 1:
    imovel = dados_coletados_geral[i]

    url = imovel['Link para o anúncio']
    random_user_agent = random.choice(user_agents)
    headers = {"User-Agent": random_user_agent}

    html = requests.get(url, headers = headers).text
    response = scrapy.http.HtmlResponse(url = url, body = html, encoding = "utf-8")

    try:
        html_content = requests.get(url, headers = headers, timeout=10).text
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        print(f"{amarelo}Erro de conexão/timeout no imóvel {i+1}. Tentando novamente em 5 segundos...{fim}")
        time.sleep(5)
        continue

    time.sleep(random.uniform(1, 2.5))
    response = scrapy.http.HtmlResponse(url = url, body = html_content, encoding = "utf-8")

    for dados in response.css("div.div-block-19.w-clearfix"):
        imovel["Titulo do imóvel"] = (dados.css("h1.heading-5::text").get() or "")

    for dados in response.css("div.div-block-28"):
        quarto = dados.xpath(".//div[contains(., 'Quarto') or contains (., 'Dormitório')]//text()").re_first(r'(\d+)\s*Quartos?|Dormitórios?') or "0"
        if quarto:
            imovel["Quartos"] = int(quarto)

        suite = dados.xpath(".//div[contains(., 'Suíte')]//text()").re_first(r'(\d+)\s*Suítes?') or "0"
        if suite:
            imovel["Suítes"] = int(suite)

    for dados in response.css("div.div-block-29, div.feature-wrap"):
        area_imovel = (dados.xpath(".//div[contains(., 'm²')]/b/text()").get() or "0").replace(",", ".")[:-2]
        if area_imovel:
            imovel["Área do imóvel"] = float(area_imovel)

    for dados in response.css("div.div-block-32, div.text-block-19"):
        condominio_trecho = dados.xpath(".//*[contains(., 'Valor do condomínio')]//text()").getall() or "0"
        for valor_condominio in condominio_trecho:
            valor = re.search(r'R\$\s*[\d.,]+', valor_condominio)
            if valor: 
                imovel["Valor Condomínio"] = valor.group(0).replace("R$", "")[:-3]

    print(f"{contador_atual}/{contador_imoveis}{verde} Coletado dados específicos de", imovel["Titulo do imóvel"], f'{fim}')
    i += 1
    contador_atual += 1
    time.sleep(0.5)

print(f'\n{azul}------------------Finalizado Imobiliária La Salle------------------{fim}')

print(f'{azul}------------------Iniciado Imobiliária Lokatell------------------{fim}\n')

driver = webdriver.Chrome()
url = "https://lokatell.com.br/aluguel/residencial_comercial/toledo/"
driver.get(url)
driver.maximize_window()

wait = WebDriverWait(driver, 15)
container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "clb-search-result-property")))

prev_count = 0
same_count_times = 0
contador_imoveis = 0
links_coletados = set()

while True:
    driver.execute_script("arguments[0].scrollTop += 400;", container)
    time.sleep(1)

    cards = driver.find_elements(By.CLASS_NAME, "imovel-box-single")
    current_count = len(cards)

    for card in cards:
        try:
            titulo = card.find_element(By.CLASS_NAME, "titulo-grid").text.strip()
        except:
            titulo = None

        try:
            link = card.find_element(By.XPATH, ".//div[@class='titulo-anuncio']/a").get_attribute('href')
        except:
            link = None

        if link in links_coletados:
            continue

        try:
            raw_address = card.find_element(By.CSS_SELECTOR, '[itemprop="streetAddress"]')
            address = raw_address.text.strip()

            if '-' in address:
                bairro, city_state = address.split('-', 1)
                bairro = bairro.strip()
            else:
                bairro = None
        except:
            bairro = None

        father = card.find_element(By.CLASS_NAME, 'property-amenities.amenities-main')
        blocks = father.find_elements(By.XPATH, './div')
        quartos = suites = area = 0

        try:
            for block in blocks:
                label = block.find_element(By.TAG_NAME, 'small').text.strip().lower()
                if 'suíte' in label or 'suítes' in label:
                    raw_suite= block.find_element(By.TAG_NAME, 'span').text.strip()
                    m = re.search(r'\d+', raw_suite)
                    suites = int(m.group(0)) if m else 0
                    break
        except:
            suites = 0

        try:
            for block in blocks:
                label = block.find_element(By.TAG_NAME, "small").text.strip().lower()
                if "quarto" in label or "quartos" in label:
                    raw_bedroom = block.find_element(By.TAG_NAME, "span").text.strip()
                    m = re.search(r'\d+', raw_bedroom)
                    quartos = int(m.group(0)) if m else 0
                    break
        except:
            quartos = 0

        try:
            for block in blocks:
                raw_area = block.find_element(By.TAG_NAME, "span").text.strip()
                if "m²" in raw_area:
                    m = re.search(r'[\d\.,]+', raw_area)
                    if m:
                        num_s = m.group(0).replace('.', '').replace(',', '.')
                        try:
                            area = float(num_s)
                        except:
                            area = 0
                    else:
                        area = 0
                    break
        except:
            area = 0

        try:
            raw_price = card.find_element(By.CSS_SELECTOR, '[itemprop="price"]').text.strip()
            m = re.search(r'[\d\.,]+', raw_price)
            if m:
                num_s = m.group(0).replace('.', '').replace(',', '.')
                try:
                    preco = float(num_s)
                except:
                    preco = 0
        except:
            preco = 0

        try:
            condominio = int(card.find_element(By.CLASS_NAME, "item-price-condominio").text.strip().split()[-1].split(',')[0])
        except:
            condominio = 0
        
        tipo = None
        if "Barracão" in titulo:
            tipo = "Barracão"
        elif "Terreno" in titulo:
            tipo = 'Terreno'
        elif "Casa" or "Sobrado" or "Apartamento" in titulo:
            tipo = "Residencial"
        elif "Loja" or "Sala Comercial" in titulo:
            tipo = "Sala Comercial"
        else:
            tipo = "Não Identificado"

        registro = {
            "Titulo do imóvel": titulo,
            "Bairro": bairro,
            "Valor Condomínio": condominio,
            "Quartos": quartos,
            "Suítes": suites,
            "Área do imóvel": area,
            "Preço": preco,
            "Tipo do imóvel": tipo, 
            "Link para o anúncio": link,
            "Origem": "Lokatell"
        }

        if registro not in dados_coletados_geral:
            dados_coletados_geral.append(registro)
            links_coletados.add(link)
            contador_imoveis += 1
            print(f"{contador_imoveis}.{verde} Coletado: {titulo}{fim}")

    # controle de fim da rolagem
    if current_count == prev_count:
        same_count_times += 1
    else:
        same_count_times = 0

    if same_count_times >= 8:
        print(f"{amarelo}Nenhum novo imóvel carregado, finalizando scroll.{fim}")
        break

    prev_count = current_count

print(f"{azul}Total de imóveis coletados: {contador_imoveis}{fim}\n")

print(f'\n{azul}------------------Finalizado Imobiliária Lokatell------------------{fim}')

print(f'{azul}------------------Iniciado Imobiliária Ativa------------------{fim}\n')

class_imovel = 'muda_card1.ms-lg-0.col-12.col-md-12.col-lg-6.col-xl-4.mt-4.d-flex.align-self-stretch.justify-content-center'

def getPage(n):
    return f'https://www.imobiliariaativa.com.br/pesquisa-de-imoveis/?locacao_venda=L&finalidade=&dormitorio=&garagem=&vmi=&vma=&ordem=6&&pag={n}'

def percorra(driver):
    have = True
    locs = 0
    pag = 0
    while have:
        try:
            pag += 1
            driver.get(getPage(pag))
            imoveis = driver.find_elements(By.CLASS_NAME, class_imovel)

            if locs >= int(driver.find_element(By.XPATH,'/html/body/main/section/div/h1').text.split(' ')[0]):
                return
            yield imoveis
        finally:
            pass

def calcularTipo(titulo):
    lTitle = titulo.lower()
    if 'casa' or 'sobrado' or 'apartamento' in lTitle:
        return 'Residencial'
    elif 'comercia' in lTitle:
        return 'Sala Comercial'
    elif 'barracão' in lTitle:
        return 'Barracão'
    elif 'Terreno' in lTitle:
        return 'Terreno'
    else:
        return 'Não Identificado'

def buscarCondominio(link, driver, bustarArea, area, tipo):
    driver.execute_script(f"window.open('{link}');")
    driver.switch_to.window(driver.window_handles[1])
    condominio = 'None'
    
    if tipo == 'Residencial':
        try:
            for i in range(2, 10):
                if driver.find_element(By.XPATH,f'//*[@id="valores_imovel"]/div[{i}]/div[1]').text ==  'Condomínio':
                    condominio = int(driver.find_element(By.XPATH,f'//*[@id="valores_imovel"]/div[{i}]/div[2]').text.split(',')[0])
                    break
                else:
                    condominio = 0
        except:
            print('', end = '')
            
    if bustarArea:
        area = [area for area in [e.text for e in driver.find_elements(By.CLASS_NAME,'fw-bold')] if ' m²' in area]
        if len(area) > 0:
            area = float(area[0].split()[0])
        else:
            descricao = driver.find_element(By.CLASS_NAME,'descricao-imovel').text
            if ' m²' in descricao:
                palavras = descricao.split()
                for i, palavra in enumerate(palavras):
                    if palavra == 'm²':
                        area = float(f'{palavras[i-1].replace(',','.')} {palavras[i]}'.split()[0])
                        
            else:
                area = None

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return (condominio, area)

def getAttrs(imovel, driver, contador):
    titulo = imovel.find_element(By.CLASS_NAME,'card-titulo.corta-card-titulo').text.replace(',','.')
    tipo = calcularTipo(titulo)
    link = imovel.find_element(By.CLASS_NAME,'carousel-cell.is-selected').get_attribute('href')
    buscarArea = False
    suites = ''
    quartos = ''
    area = ''
    condominio = 'None'
    try:
        extras  = imovel.find_element(By.CLASS_NAME,'imo-dad-compl')
        for extra in extras.find_elements(By.TAG_NAME,'div'):
            if 'dorm-ico' in extra.get_attribute('class').split():
                quartos = extra.find_elements(By.TAG_NAME,'span')[1].text
            else:
                quartos = 0
            if 'suites-ico' in extra.get_attribute('class').split():
                suites = extra.find_elements(By.TAG_NAME,'span')[1].text
            else:
                suites = 0
            if 'a-terr-ico' in extra.get_attribute('class').split():
                area = extra.find_elements(By.TAG_NAME,'span')[1].text
            elif 'a-const-ico' in extra.get_attribute('class').split():
                area = extra.find_elements(By.TAG_NAME,'span')[1].text
            elif 'a-util-ico' in extra.get_attribute('class').split():
                area = extra.find_elements(By.TAG_NAME,'span')[1].text
            elif 'a-total-ico' in extra.get_attribute('class').split():
                area = extra.find_elements(By.TAG_NAME,'span')[1].text
            else:
                buscarArea = True
    except:
        print(f'{vermelho}Não foi possível alguns dados do imóvel{fim}')

    try:
        valor = int(imovel.find_element(By.CLASS_NAME,'card-valores').text.split(',')[0].replace('.', '').split()[1])
    except:
        valor = 0
        
    condominio, area = buscarCondominio(link, driver, buscarArea, area, tipo)

    bairro = imovel.find_element(By.CLASS_NAME,'card-bairro-cidade-texto').text.split('-')[0][:-1]
    print(f"{contador}.{verde} Coletado:", titulo, f'{fim}')

    registro = {
    "Titulo do imóvel": titulo,
    "Bairro": bairro,
    "Valor Condomínio": condominio,
    "Quartos": quartos,
    "Suítes": suites,
    "Área do imóvel": area,
    "Preço": valor,
    "Tipo do imóvel": tipo,
    "Link para o anúncio": link,
    "Origem": "Ativa"
}

    return registro
    
driver = webdriver.Chrome()
driver.maximize_window()

contador_imoveis = 1
for imoveis in percorra(driver):
    for imovel in imoveis:
        registro = getAttrs(imovel, driver, contador_imoveis)
        contador_imoveis += 1
        dados_coletados_geral.append(registro)

driver.quit()

print(f'{azul}------------------Finalizado Imobiliária Ativa------------------{fim}')

print(f"Foram coletados ao todo {vermelho}{len(dados_coletados_geral)}{fim} imóveis")

print(f'{verde}Preparando salvamento...{fim}')

with open("dados_scraper.csv", "w", newline = "", encoding = "utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Titulo do imóvel", "Tipo", "Preço", 'Valor Condominio', "Quartos", "Suítes", 'Área Total', "Bairro", "Link para o anúncio", 'Origem'])
    for dado in dados_coletados_geral:
        writer.writerow([dado["Titulo do imóvel"], dado["Tipo do imóvel"], dado["Preço"], dado["Valor Condomínio"], dado["Quartos"], dado["Suítes"], dado["Área do imóvel"], dado["Bairro"], dado["Link para o anúncio"], dado['Origem']])
    print(f"{verde}Salvo em CSV!{fim}")

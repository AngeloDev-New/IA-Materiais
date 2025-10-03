import scrapy
import json
import requests 
import csv
dados_coletados = []
url = 'http://quotes.toscrape.com/'
print('baixando pagina')

html_content = requests.get(url).text

response = scrapy.http.HtmlResponse(url=url,body=html_content,encoding='utf-8')

print(' procurando citacoes')

for citacao in response.css('div.quote'):
    dados_coletados.append(
        {
            'texto':citacao.css('span.text::text').get(),
            'autor':citacao.css('small.autor::text').get(),
            'tags':citacao.css('div.tags a.tag::text').getall()
        }
    )
with open('simples.json','w',encoding='utf-8') as f:
    json.dump(dados_coletados,f,indent=2,ensure_ascii=False)
    print('Salvo simples.json')
with open('dados.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Texto','Autor','Tags'])
    for dado in dados_coletados:
        writer.writerow([dado['texto'],dado['autor'],', '.join(dado['tags'])])
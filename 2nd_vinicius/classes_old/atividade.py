import scrapy
import json
import requests 
import csv
dados_coletados = []
url = 'https://news.ycombinator.com/'
print('baixando pagina')
#\34 5017028 > td:nth-child(3) > span:nth-child(1) > a:nth-child(2)
html_content = requests.get(url).text

response = scrapy.http.HtmlResponse(url=url,body=html_content,encoding='utf-8')

print(' procurando citacoes')

for title in response.css('span.titleline'):
    dados_coletados.append(
        {
            'title':title.css('a::text').get(),
        }
    )
with open('atv.json','w',encoding='utf-8') as f:
    json.dump(dados_coletados,f,indent=2,ensure_ascii=False)
    print('Salvo simples.json')
with open('atv.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['titles'])
    for dado in dados_coletados:
        writer.writerow([dado['title'],', '.join(dado['title'])])
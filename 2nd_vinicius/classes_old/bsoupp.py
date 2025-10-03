# import requests
from bs4 import BeautifulSoup
with open('indezAula2.html', 'r',encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

noticias = soup.find_all('div', class_='Noticias')

for noticia in noticias:
    titulo = noticia.find('h2').text
    conteudo = noticia.find('p').text
    print(f'Titulo: {titulo}')
    print(f'Conteudo: {conteudo}')
    print('---'*10)
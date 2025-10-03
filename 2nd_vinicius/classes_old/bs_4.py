import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com/'

response = requests.get(url)

if response.status_code == 200:
    print("Request successful!")
    soup = BeautifulSoup(response.text,'html.parser')
    page_title = soup.title.string
    print(f"Page title: {page_title}")
    print("Extracting content...")
    # print (response.text)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")


box = soup.find_all('div', class_='quote')
for quote in box:

    if 'Albert Einstein' in quote.text:
        # print("Found a quote by Albert Einstein!")
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        
        print('-------'*20)
        print(f"Quote: {text}")
        print(f"Author: {author}")
        print(f"Tags: {', '.join(tags)}")
import requests
from bs4 import BeautifulSoup

url = 'https://www.wikipedia.org/'

response = requests.get(url)

if response.status_code == 200:
    print("Request successful!")
    soup = BeautifulSoup(response.text,'html.parser')
    page_title = soup.title.string
    print(f"Page title: {page_title}")
    print("Extracting content...")
    print (response.text)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
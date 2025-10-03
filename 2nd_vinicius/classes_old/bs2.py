import requests
url = 'https://www.google.com/'
response = requests.get(url)
if response.status_code == 200:
    print("Request successful!")
    html_content = response.text
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
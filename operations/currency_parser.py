from bs4 import BeautifulSoup
import requests


def get_currency(from_, to_):
    URL = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={from_}&To={to_}"
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
    }
    response = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod').text

    return items[0:6]


# get_currency('USD',"EUR")

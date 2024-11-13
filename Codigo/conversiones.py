import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse

def tipo_de_cambio_ars_usd(currency = 'USD', amount = 1):
    '''
    Consulta el valor actual del dolar online.
    '''
        
    #Acceso a la pagina
    content = requests.get(f"https://www.x-rates.com/table/?from={currency}&amount={amount}").content
    
    #Iniciar 'BeautifulSoup'.
    soup = bs(content, "html.parser")
    
    #Obtener precios actualizados
    price_datetime = parse(soup.find_all("span", attrs={"class": "ratesTimestamp"})[1].text)
    
    #Obtener tabla.
    exchange_tables = soup.find_all("table")
    exchange_rates = {}
    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            tds = tr.find_all("td")
            if tds:
                currency = tds[0].text
                exchange_rate = float(tds[1].text)
                exchange_rates[currency] = exchange_rate        
    
    ars_to_usd = exchange_rates['Argentine Peso']
    return price_datetime, ars_to_usd

if __name__ == "__main__":
    pass
import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class get_price:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Нельзя перевести валюту на саму себя {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать валюту {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        #total_base = int(json.loads(r.content)[keys[base]])*int(json.loads(r.content)[keys[amount]])
        total_base = json.loads(r.content)[keys[base]]

        return total_base


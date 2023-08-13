import requests
import json
from config import keys
class APIException(Exception):
    pass


class Convert:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            ticker_base = keys[base.lower()]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту {base}')

        try:
            ticker_quote = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту {quote}')

        if ticker_base == ticker_quote:
            raise APIException(f'Невозможно обработать запрос!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Невозможно обработать количество {amount}')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={ticker_base}&tsyms={ticker_quote}")
        resp = json.loads(r.content)
        new_price = resp[ticker_quote] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message


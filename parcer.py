import copy

import requests
from bs4 import BeautifulSoup


class EkParcer:
    _BASE_URL = 'https://ek.ua'
    _LOCALE = 'ua'
    _SOUP = None

    def __init__(self):
        # todo make flexible
        # мобільні телефони Apple
        # https://rozetka.com.ua/search/?text=мобільні+телефони+Apple
        # response = requests.get('https://ek.ua/ua/')
        response = requests.get(
            'https://ek.ua/ua/ek-list.php?katalog_=122&brand_=apple&sb_=%D0%BC%D0%BE%D0%B1%D1%96%D0%BB%D1%8C%D0%BD%D1%96+%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B8+Apple')
        html = response.text
        self._SOUP = BeautifulSoup(html, 'html.parser')

    def get_cards(self):
        cards = []
        for item in self._SOUP.find_all('table', class_='model-short-block'):
            card = {
                'title': item.find('span', class_='u').text,
                'price_range': item.find('div', class_='model-price-range').find('a').text.strip(),
                'details': item.find('div', class_='m-s-f2').find_all('div'),
                # **{ item[:item.find(':')]: item[item.find(':')+2:] for item in item.find('div', class_='m-s-f2').find_all('div', requrcive=False) }
            }

            det = {}
            card['det'] = det
            for item in item.find('div', class_='m-s-f2').find_all('div', recursive=False):
            #     if item.__
            #         print(item['title'])
            #     print(item[:item.find(':')],  item[item.find(':') + 2:])
                tmp = " ".join(item.text.split())
                # print(tmp[:tmp.find(':')], tmp[tmp.find(':')+1:])
                k, v = tmp[:tmp.find(':')], tmp[tmp.find(':')+1:]
                det[k] = v

            cards.append(card)

        for card in cards:
            print(f"{card.get('title'):30} {card.get('price_range'):30} {card.get('de-tails')}")
            print(f"{card.get('det')}")
        # return cards

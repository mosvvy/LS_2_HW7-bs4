import copy

import requests
from bs4 import BeautifulSoup

from db_connector import SQLiteConnector


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

    def __get_card(self, table):
        card = {
            'Назва': table.find('span', class_='u').text,
            'Ціна': 'від ' + table.find('div', class_='model-price-range').find('a').text.strip(),
            # 'details': table.find('div', class_='m-s-f2').find_all('div'),

            # "Екран":None,
            # "Камера":None,
            # "Відео":None,
            # "Пам'ять":None,
            # "Процесор":None,
            # "ОЗП":None,
            # "Акумулятор":None,
            # "Корпус":None,
        }

        det = {}
        # card['det'] = det
        for i in table.find('div', class_='m-s-f2').find_all('div', recursive=False):
            tmp = " ".join(i.text.split())
            k, v = tmp[:tmp.find(':')], tmp[tmp.find(':') + 1:].strip()
            det[k] = v
            card[k] = v

        return card

    def get_cards(self):
        cards = []
        for item in self._SOUP.find_all('table', class_='model-short-block'):
            card = self.__get_card(item)
            cards.append(card)
            # for variation in item.find('div', class_='m-c-f1-pl--button').find_all('a'):
            #     card = self.__get_card(item)
            #     cards.append(card)
        return cards

    @staticmethod
    def show_cards(cards):
        print()
        for card in cards:
            print(
                f"{card.get("Назва"):30}{card.get("Ціна"):25}{card.get("Екран"):60}{card.get("Камера"):50}{card.get("Відео"):60}{card.get("Пам'ять"):10}{card.get("Процесор"):20}{card.get("ОЗП"):10}{card.get("Акумулятор"):20}{card.get("Корпус"):20}")
            # print()
            # print(f"{card.get('title'):>30} {card.get('price_range'):30} {card.get('de-tails')}")
            # for k,v in card.get('det').items():
            # for k, v in card.items():
            #     print(f"{k:>30} {v}")

    @staticmethod
    def get_attr_name():
        # todo remove this construction...
        attrs = {
            "Назва": "title",
            "Ціна": "price_range",
            "Екран": "screen",
            "Камера": "camera",
            "Відео": "video",
            "Пам'ять": "space",
            "Процесор": "processor",
            "ОЗП": "ram",
            "Акумулятор": "battery",
            "Корпус": "corpus",
        }
        return list(attrs.values())

    @staticmethod
    def save_to_db(db: str, cards):
        # db.insert(cards)
        con = SQLiteConnector(db)
        # print(con)
        # try:
        for card in cards:
            con.cursor.execute(
                f"""SELECT id FROM phones WHERE title='{card.get("Назва")}' AND space='{card.get("Пам'ять")}' AND ram='{card.get("ОЗП")}'""")
            id = con.cursor.fetchall()
            print('====================id:', id)
            if id:
                id = id[0][0]
                print('================================id:', id)
                # print(f"""UPDATE phones
                #     SET price_range = '{card.get('Ціна')}',
                #         screen = '{card.get('Екран')}',
                #         camera = '{card.get('Камера')}',
                #         video = '{card.get('Відео')}',
                #         processor = '{card.get('Процесор')}',
                #         battery = '{card.get('Акумулятор')}',
                #         corpus = '{card.get('Корпус')}'
                #     WHERE id={id}""")
                con.cursor.execute(f"""UPDATE phones 
                    SET price_range = '{card.get('Ціна')}',
                        screen = '{card.get('Екран')}',
                        camera = '{card.get('Камера')}',
                        video = '{card.get('Відео')}',
                        processor = '{card.get('Процесор')}',
                        battery = '{card.get('Акумулятор')}',
                        corpus = '{card.get('Корпус')}'
                    WHERE id={id}""")
            else:
                con.cursor.execute(
                    f"""INSERT INTO phones ('{"', '".join(EkParcer.get_attr_name())}') VALUES('{"', '".join(list(card.values()))}')""")
            con.commit()

        # except:
        #     print(f'ERROR')

        del con

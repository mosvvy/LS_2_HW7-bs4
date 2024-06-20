import pytest
from types import SimpleNamespace
from unittest import mock

import requests


def mock_response_func():
    # return requests.get('https://ek.ua/ua/ek-list.php?katalog_=122&brand_=apple&sb_=%D0%BC%D0%BE%D0%B1%D1%96%D0%BB%D1%8C%D0%BD%D1%96+%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B8+Apple')
    with open('data/search-page.html', 'r', encoding='utf-8') as f:
        return f.read()


def test_tmp():
    mock_response = SimpleNamespace()
    mock_response.text = mock_response_func()

    with mock.patch('requests.get', return_value=mock_response):
        response = requests.get('https://ek.ua/ua/ek-list.php?katalog_=122&brand_=apple&sb_=%D0%BC%D0%BE%D0%B1%D1%96%D0%BB%D1%8C%D0%BD%D1%96+%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B8+Apple')
        print(response.text)



import pytest
from types import SimpleNamespace
from unittest import mock

from parcer import EkParcer


def mock_response_func():
    with open('data/search-page.html', 'r', encoding='utf-8') as f:
        return f.read()


def test_tmp():
    mock_response = SimpleNamespace()
    mock_response.text = mock_response_func()

    with mock.patch('requests.get', return_value=mock_response):
        p = EkParcer()

    cards = p.get_cards()

    print(list(cards[0].values()))


def test_db():
    mock_response = SimpleNamespace()
    mock_response.text = mock_response_func()

    with mock.patch('requests.get', return_value=mock_response):
        p = EkParcer()

    cards = p.get_cards()
    EkParcer.show_cards(cards)

    EkParcer.save_to_db('../db.db', cards)


@pytest.mark.skip
def test_db_without_mock():
    p = EkParcer()

    cards = p.get_cards()
    EkParcer.show_cards(cards)

    EkParcer.save_to_db('../db.db', cards)

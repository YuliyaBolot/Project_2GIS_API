from random import randint
import allure
import pytest
import requests
from constants import Urls, Message


class TestQueryParam:
    @allure.title('Поиск по названию региона - 3 символа')
    def test_query_param_with_three_symbols(self):
        response = requests.get(f'{Urls.url_regions}?q=рск')
        length_items = len(response.json()['items'])
        regions = response.json()['items'][randint(0, length_items - 1)]['name']
        assert response.status_code == 200 and 'рск' in regions

    @allure.title('Поиск по названию региона - знаки препинания в названии (4 символа)')
    def test_query_param_with_punctuation_marks(self):
        response = requests.get(f'{Urls.url_regions}?q=-Кам')
        length_items = len(response.json()['items'])
        regions = response.json()['items'][randint(0, length_items - 1)]['name']
        assert response.status_code == 200 and '-Кам' in regions

    @allure.title('Поиск по названию региона - разный регистр')
    def test_query_param_with_different_register(self):
        response = requests.get(f'{Urls.url_regions}?q=вЛаДи')
        length_items = len(response.json()['items'])
        regions = response.json()['items'][randint(0, length_items - 1)]['name']
        assert response.status_code == 200 and 'Влади' in regions

    @allure.issue('BUG: Код ответа = 200, а не 400. Как быть с городами, длина названия которых - 2 символа?')
        regions = response.json()
        message = Message.message_about_three_symbols_in_query_param
        assert response.status_code == 400 and message in regions['error']['message']

    @allure.title('Поиск по названию региона - цифры в названии')
    def test_query_param_with_digits(self):
        response = requests.get(f'{Urls.url_regions}?q=567432')
        regions = response.json()
        assert response.status_code == 200 and 'items' in regions

    @allure.title('Поиск по названию региона - параметр пуст')
    @allure.issue('BUG: Код ошибки = 500, а не 400.')
    def test_query_param_with_null(self):
        response = requests.get(f'{Urls.url_regions}?q=')
        regions = response.json()
        message = Message.message_about_three_symbols_in_query_param
        assert response.status_code == 400 and message in regions['error']['message']

    @allure.title('Поиск по названию региона - 30 и 29 символов')
    def test_query_param_with_thirty_and_twenty_nine_symbols(self, symbols):
        response = requests.get(f'{Urls.url_regions}?q={symbols}')
        regions = response.json()
        assert response.status_code == 200 and 'items' in regions

    @allure.title('Поиск по названию региона - более 30 символов')
    @allure.issue('BUG: Код ответа = 200, а не 400.')
    def test_query_param_with_more_than_thirty_symbols(self):
        regions = response.json()
        message = Message.message_about_thirty_symbols_in_query_param

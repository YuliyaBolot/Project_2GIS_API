import allure
import pytest
import requests
from constants import Urls, Message


class TestPageSize:
    @allure.title('Проверка значения параметра page_size по умолчанию')
    @allure.issue('BUG: Возвращается список из 10 регионов, а не 15.')
    def test_page_size_equals_fifteen(self):
        response = requests.get(Urls.url_regions)
        length_items = len(response.json()['items'])
        assert length_items == 15

    @allure.title('Проверка значений параметра page_size: 5, 10, 15')
    @pytest.mark.parametrize('page_size', [5, 10, 15])
    def test_page_size_equals_five_ten_fifteen(self, page_size):
        response = requests.get(f'{Urls.url_regions}?page_size={page_size}')
        length_items = len(response.json()['items'])
        assert length_items == page_size

    @allure.title('Проверка числовых значений параметра page_size, отличных от 5, 10, 15')
    @allure.issue('BUG: Код ответа = 200, а не 400.')
    @pytest.mark.parametrize('page_size', [0, -1, 1, 25])
    def test_page_size_different_digit(self, page_size):
        response = requests.get(f'{Urls.url_regions}?page_size={page_size}')
        regions = response.json()
        message = Message.message_about_acceptable_values_page_size
        assert message in regions['error']['message']

    @allure.title('Проверка НЕ числовых значений параметра page_size.')
    @allure.issue('BUG: Код ответа = 200, а не 400.')
    @pytest.mark.parametrize('page_size', ['ajdjfk', ' ', ''])
    def test_page_size_different_digit(self, page_size):
        response = requests.get(f'{Urls.url_regions}?page_size={page_size}')
        regions = response.json()
        message = Message.message_about_digit_page_size
        assert message in regions['error']['message']


from random import randint
import allure
import pytest
import requests
from constants import Urls, Message


class TestCountryCode:
    @allure.title('Поиск по коду страны: ru, cz, kz, kg')
    @allure.issue('BUG: При указании кода kz отображаются еще и регионы kg и наоборот')
    @pytest.mark.parametrize('country_code', ['ru', 'cz', 'kz', 'kg'])
    def test_country_code_ru_cz_kz_kg(self, country_code):
        response = requests.get(f'{Urls.url_regions}?country_code={country_code}')
        length_items = len(response.json()['items'])
        regions = response.json()['items'][randint(0, length_items-1)]['country']['code']
        assert response.status_code == 200 and country_code == regions

    @allure.title('Поиск по коду страны отличному от ru, cz, kz, kg')
    @allure.issue('BUG: Тест проходит при указании кода az. Код ответа = 200, а не 400. ')
    @pytest.mark.parametrize('country_code', ['rus', 'ру', 'az', 'au', '123', '0', ' ', '!;.'])
    def test_country_code_different_from_ru_cz_kz_kg(self, country_code):
        response = requests.get(f'{Urls.url_regions}?country_code={country_code}')
        regions = response.json()
        message = Message.message_about_country_code
        assert message in regions['error']['message']

    @allure.title('Поиск по коду страны - параметр пуст')
    @allure.issue('BUG: Код ответа = 200, а не 400.')
    def test_country_code_null(self):
        response = requests.get(f'{Urls.url_regions}?country_code=')
        regions = response.json()
        message = Message.message_about_country_code
        assert response.status_code == 400 and message in regions['error']['message']
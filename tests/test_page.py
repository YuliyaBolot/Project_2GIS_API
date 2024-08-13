import allure
import pytest
import requests
from constants import Urls, Message


class TestPage:
    @allure.title('Проверка значения параметра page по умолчанию')
    def test_page_equals_one(self):
        response = requests.get(Urls.url_regions)
        response_page_one = requests.get(f'{Urls.url_regions}?page={1}')
        regions = response.json()
        regions_page_one = response_page_one.json()
        assert regions == regions_page_one

    @allure.title('Проверка числовых значений параметра page')
    @pytest.mark.parametrize('page', [2, 999999999999999999999])
    def test_page_different_digits(self, page: int):
        response = requests.get(f'{Urls.url_regions}?page={page}')
        regions = response.json()
        assert response.status_code == 200 and 'items' in regions

    @allure.title('Проверка НЕ числовых значений параметра page')
    @allure.issue('BUG: Код ответа = 200, а не 400. Опечатка в тексте ошибки в слове должен')
    @pytest.mark.parametrize('page', ['asdffg!?', ' ', ''])
    def test_page_not_digits(self, page: int):
        response = requests.get(f'{Urls.url_regions}?page={page}')
        regions = response.json()
        message = Message.message_about_digit_page
        assert message in regions['error']['message']

    @allure.title('Проверка нулевого значения параметра page')
    @allure.issue('BUG: Код ответа = 500, а не 400.')
    def test_page_equals_zero(self):
        response = requests.get(f'{Urls.url_regions}?page={0}')
        regions = response.json()
        message = Message.message_page_should_be_more_zero
        assert response.status_code == 400 and message in regions['error']['message']

    @allure.title('Проверка отрицательного значения параметра page')
    @allure.issue('BUG: Код ответа = 200, а не 400.')
    def test_page_negative(self):
        response = requests.get(f'{Urls.url_regions}?page={-1}')
        regions = response.json()
        message = Message.message_page_should_be_more_zero
        assert message in regions['error']['message']


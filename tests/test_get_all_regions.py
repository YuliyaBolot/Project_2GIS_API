from random import randint
import allure
import requests
from constants import Urls


class TestGetAllRegions:
    @allure.title('Получение списка доступных регионов')
    def test_get_all_regions(self):
        response = requests.get(Urls.url_regions)
        regions = response.json()
        assert response.status_code == 200 and len(regions['items']) > 0

    @allure.title('Проверка приоритетности параметра query перед другими параметрами')
    def test_query_priority(self):
        response = requests.get(f'{Urls.url_regions}?q=рск&country_code=cz&page={4}&page_size={10}')
        length_items = len(response.json()['items'])
        regions_name = response.json()['items'][randint(0, length_items - 1)]['name']
        regions_code = response.json()['items'][randint(0, length_items - 1)]['country']['code']
        assert response.status_code == 200 and 'рск' in regions_name and regions_code != 'cz' and length_items != 10

    @allure.title('Проверка работы всех параметров без параметра query')
    def test_all_params_without_query(self):
        response = requests.get(f'{Urls.url_regions}?country_code=ru&page={2}&page_size={5}')
        length_items = len(response.json()['items'])
        regions_code = response.json()['items'][randint(0, length_items - 1)]['country']['code']
        assert response.status_code == 200 and regions_code == 'ru' and length_items == 5

    @allure.title('Проверка равенства значения total общему количеству регионов в items')
    @allure.issue('BUG: Количество регионов, указанных в total, не совпадает с количеством в списке items. '
                  'Количество в total и items неверно.')
    def test_total_equals_length_items(self):
        response_page_one = requests.get(f'{Urls.url_regions}?page={1}')
        response_page_two = requests.get(f'{Urls.url_regions}?page={2}')
        response_page_three = requests.get(f'{Urls.url_regions}?page={3}')
        length_items_page_one = len(response_page_one.json()['items'])
        length_items_page_two = len(response_page_two.json()['items'])
        length_items_page_three = len(response_page_three.json()['items'])
        all_length = length_items_page_one + length_items_page_two + length_items_page_three
        total = response_page_one.json()['total']
        assert total == all_length

    @allure.title('Отсутсвие повторений в списке items')
    @allure.issue('BUG: Последний город на одной странице равен первому городу на следующей странице.')
    def test_absence_reiterations_in_items(self):
        response_page_one = requests.get(f'{Urls.url_regions}?page={1}')
        response_page_two = requests.get(f'{Urls.url_regions}?page={2}')
        response_page_three = requests.get(f'{Urls.url_regions}?page={3}')
        last_region_name_page_one = response_page_one.json()['items'][-1]['name']
        first_region_name_page_two = response_page_two.json()['items'][0]['name']
        last_region_name_page_two = response_page_one.json()['items'][-1]['name']
        first_region_name_page_three = response_page_three.json()['items'][0]['name']
        assert (last_region_name_page_one != first_region_name_page_two and
                last_region_name_page_two != first_region_name_page_three)

    @allure.title('Проверка изменения значения total в зависимости от изменения количества регионов в items')
    @allure.issue('BUG: Значение total остается неизменным, не смотря на изменение количества регионов в списке items.')
    def test_change_total_if_change_items(self):
        response = requests.get(f'{Urls.url_regions}?country_code=cz')
        total = response.json()['total']
        length_items = len(response.json()['items'])
        assert total == length_items

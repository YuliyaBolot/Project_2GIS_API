import allure
import requests
from constants import Urls


class TestGetAllRegions:
    @allure.title('Получение списка доступных регионов')
    def test_get_all_regions(self):
        response = requests.get(Urls.url_regions)
        regions = response.json()
        assert response.status_code == 200 and len(regions['items']) > 0

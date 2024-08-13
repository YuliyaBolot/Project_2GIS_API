import json
from random import randint
import requests
from constants import Urls


class Draft:
    def get_regions(self):
        response = requests.get(Urls.url_regions)
        regions = response.json()
        print(len(regions['items']))


draft = Draft()
draft.get_regions()

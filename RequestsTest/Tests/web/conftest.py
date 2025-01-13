import pytest  
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function") # обязательная строка, которая объявляет функцией нашу фикстуру
def browser():
    """
    Basic fixture
    """  
    chrome_options = Options()
    chrome_options.add_argument("--nosandbox")
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extentions")
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless") 

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    yield driver #позволяет из нашей фикстуры вернуть обьект Driver для всех объектов
    driver.quit()



@pytest.fixture(scope="function")
def knockout():
    header = {'Content-Type':'application/json','trainer_token': '03fdaa534ce13ac9cf52b58a57559ecb'}
    pokemons = requests.get(url=f'https://api.pokemonbattle-stage.ru/v2/pokemons', params={"trainer_id": 1873},
                            headers=header, timeout=3)
    if 'data' in pokemons.json():
        for pokemon in pokemons.json()['data']:
            if pokemon['status'] != 0:
                requests.post(url=f'https://api.pokemonbattle-stage.ru/v2/pokemons/knockout', headers=header,
                              json={"pokemon_id": pokemon['id']}, timeout=3)
    
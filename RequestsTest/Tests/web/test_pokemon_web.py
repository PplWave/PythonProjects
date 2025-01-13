import pytest  
import requests


from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://pokemonbattle-stage.ru/'

def test_positive_login(browser):
 
    """
    TRP-1. Positive case
    """  

    browser.get(URL)
    
    email_input = browser.find_element(by=By.CSS_SELECTOR, value = '[class="auth__input k_form_f_email"]')
    email_input.click()
    email_input.send_keys('pada1one@mail.ru')
    
    password_input = browser.find_element(by=By.ID, value='password')
    password_input.click
    password_input.send_keys('1q2w3E')
    
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class="auth__button k_form_send_auth"]')
    button.click()

    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
    
    trainer_id = browser.find_element(by=By.CSS_SELECTOR, value='[class="header__id-texts"]')
    text_id = trainer_id.text.replace('\n', ' ')
    assert text_id == 'ID 1873', 'Unexpected tranier id'


CASES = [                   #список кортежей (списки фиксированной длины)
    ('1','pada1onemail.ru', '1q2w3E', ['Введите почту', ''] ), 
    ('2','pada1one@mail.ru', '1q2w3', ['', 'Неверные логин или пароль'] ),
    ('3','pada1onemail', '1q2w3E', ['Введите почту', ''] ),
    ('4','', '1q2w3E', ['Введите почту', ''] ),
    ('5','pada1one@mail.ru', '', ['', 'Введите пароль'] )
]

@pytest.mark.parametrize('case_number, email, password, alerts', CASES) #параметризируем наш автотест
def test_negative_login(case_number, email, password, alerts, browser): # наполняем параметры тестовой функции 
 
    """
    TRP-1. Negative cases
    """  
    logger.info(f'CASE : {case_number}')  #настраиваем логирование, внедряя в нашу стрингу - переменную
    browser.get(URL)
    
    email_input = browser.find_element(by=By.CSS_SELECTOR, value = '[class="auth__input k_form_f_email"]')
    email_input.click()
    email_input.send_keys(email)
    
    password_input = browser.find_element(by=By.ID, value='password')
    password_input.click
    password_input.send_keys(password)
    
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class="auth__button k_form_send_auth"]')
    button.click()

    alerts_messages = browser.find_elements(by=By.CSS_SELECTOR, value='[class*="auth__error"]') # добавляем * после class что бы выбирать все варианты ошибки 
    alerts_list = []
    for element  in alerts_messages:     # пишем цикл, перебираем входяще элементы входящие в список
        alerts_list.append(element.text) # добавляем в наш пустой список, новые значения 

    assert alerts_list == alerts,  'Unexpected  alerts in authentication form'


def test_check_api(browser, knockout):
    """
    POC-3. Check create pokemon by api request
    """
    browser.get(URL)

    email = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="f_email"]')))
    email.click()
    email.send_keys('pada1one@mail.ru')

    password = browser.find_element(by=By.CSS_SELECTOR, value='[class*="f_pass"]')
    password.click()
    password.send_keys('1q2w3E')

    enter = browser.find_element(by=By.CSS_SELECTOR, value='[class*="send_auth"]')
    enter.click()
    
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
    
    browser.find_element(by=By.CLASS_NAME, value='header__id-texts').click()
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be('https://pokemonbattle-stage.ru/trainer/1873'))

    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value='[class="pokemons-info"] [class*="total-count"]')
    count_before = int(pokemon_count_before.text)

    body_create = {
        "name": "generate",
        "photo_id": 1
    }
    header = {'Content-Type':'application/json','trainer_token': '03fdaa534ce13ac9cf52b58a57559ecb'}
    response_create = requests.post(url='https://api.pokemonbattle-stage.ru/v2/pokemons', headers=header, json=body_create, timeout=3)
    assert response_create.status_code == 201, 'Unexpected response status_code'

    browser.refresh()
    
    assert WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, '[class="pokemons-info"] [class*="total-count"]'), f'{count_before+1}')), \
            'Unexpected pokemons count'
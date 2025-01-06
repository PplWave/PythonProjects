import requests
import pytest

URL = 'https://api.pokemonbattle.ru/v2'
TOKEN = '92819947f31702de67774bd230967bc8'
HEADER = {'Content-Type': 'application/json', 'trainer_token': TOKEN}
TRAINER_ID = '11173'


def test_status_code():
    response = requests.get(url=f'{URL}/trainers', headers=HEADER, params={'trainer_id': TRAINER_ID})
    assert response.status_code == 200


def test_part_of_response():
    response_get = requests.get(url=f'{URL}/trainers', headers=HEADER, params={'trainer_id': TRAINER_ID})
    
   
    assert response_get.status_code == 200
    
   
    print(response_get.json())
    
   
    assert response_get.json()["data"][0]["trainer_name"] == 'Vision'

@pytest.mark.parametrize ('key, value', [('trainer_name', 'Vision'), ('id', TRAINER_ID)])
def test_parametrize(key, value):
     response_parametrize = requests.get(url =f'{URL}/trainers', headers=HEADER, params={'trainer_id' : TRAINER_ID})
     assert response_parametrize.json()["data"][0][key] == value
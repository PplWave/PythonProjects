import requests

URL = 'https://api.pokemonbattle.ru/v2'
TOKEN = '92819947f31702de67774bd230967bc8'
HEADER = {'Content-Type': 'application/json', 'trainer_token' : TOKEN}

body_craftpok = {
  "name": "generate",
   "photo_id": 778
   }
body_redpok = {"pokemon_id": "122503", "name": "generate", "photo_id": 11}

body_addp =  {
    "pokemon_id": "122503"
}

response = requests.post(url=f'{URL}/pokemons', headers= HEADER, json=body_craftpok)
print(response.text)

response_put = requests.put(url=f'{URL}/pokemons', headers= HEADER, json=body_redpok)
print(response_put.text)

response_addp = requests.post(url=f'{URL}/trainers/add_pokeball', headers= HEADER, json=body_addp)
print(response_addp.text)  
import requests
import json

url = 'http://pokeapi.co/api/v2/'
command = 'pokemon/'
pkmn = 'charmander'

r = requests.post(url + command + pkmn + '/')
if r.status_code == 200:
    result = r.json()
    print("Retrieved pokemon: " + result["name"])
    print("Pokedex#" + str(result["id"]))
    print("Image url: " + result["sprites"]["front_default"])

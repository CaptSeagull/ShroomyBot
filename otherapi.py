import requests
import json
from xml.etree import ElementTree
import urllib

def getPokemon(name):
    url = 'http://pokeapi.co/api/v2/'
    command = 'pokemon/'

    if not name:
        return "No pokemon entered."
    r = requests.post(url + command + name.lower() + "/")
    if r.status_code == 200:
        result = r.json()
        return "Pokedex#{0} - {1}\n{2}".format(str(result["id"]), result["name"], result["sprites"]["front_default"])
    elif r.status_code == 404:
        return "Could not find the pokemon requested."
    else:
        return "Something else happened. Error Code: " + str(r.status_code)

def getSpanishMiriamWebster(word, key_id = ""):
    url = 'https://www.dictionaryapi.com/api/v1/references/spanish/xml/'

    if not word or not key_id:
        return "No word or key_id entered."
    r = requests.post(url + word + "?key=" + key_id)
    if r.status_code == 200:
        result = ElementTree.fromstring(r.content)

        tree_branch = result.find('.//entry/def/dt/ref-link')

        if tree_branch is not None:
            return tree_branch.text   
                      
        return "Could not find the translated word."
    elif r.status_code == 404:
        return "Could not find the translated word."
    else:
        return "Something else happened. Error Code: " + str(r.status_code)

def getJishoPage(query):
    # Dict for our results
    wrapper = {
        'writing':"",
        'reading':"",
        'definitions':[],
        'speech_type':"",
        'error':""
        }

    # GET command
    url = 'http://jisho.org/api/v1/search/words'
    params = urllib.parse.urlencode(dict(keyword=query), quote_via=urllib.parse.quote)
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return parseJishoPage(r.json(), wrapper)
    elif r.status_code == 404:
        wrapper['error'] = "Could not find the word requested. Error Code: " + str(r.status_code)
    else:
        wrapper['error'] =  "Something else happened. Error Code: " + str(r.status_code)
    return wrapper

def parseJishoPage(json, wrapper, result_index = 0):
    if json['data']:
        if result_index > len( json['data'] ) - 1:
            result_index = len( json['data'] ) - 1
        # Retrieve the result based on the result_index
        data_list = json['data'][result_index]
        # Retrieve writing and reading
        if data_list['japanese']:
            jp_list = data_list['japanese'][0]
            if 'word' in jp_list:
                wrapper['writing'] = jp_list['word']
            if 'reading' in jp_list:
                wrapper['reading'] = jp_list['reading']
        if data_list['senses']:
            senses_list = data_list['senses'][0]
            # Retrieve english definitions
            if senses_list['english_definitions']:
                for eng_def in senses_list['english_definitions']:
                    wrapper['definitions'].append(eng_def)
            # Retrieve speech type
            if senses_list['parts_of_speech']:
                wrapper['speech_type'] = senses_list['parts_of_speech'][0]
        return wrapper

    wrapper['error'] = "Could not find the word requested."
    return wrapper

import requests
import json
from xml.etree import ElementTree
import urllib

# Personal Library
import commons

def getPokemon(query=""):
    '''Retrive requested pokemon info from json file. If none exists, retrive from getPokemonFromApi(...) '''
    # This is where we will store json results (from file or API)
    pkmn_json = {}

    # Retrieve relative path to the json file
    rel_path = "pkmn/"
    filename = "pkmn_names.json"

    # Read from the json file, create if needed
    json_file_result = commons.getJsonFromFile(rel_path,filename,True)
    has_file = json_file_result.get('success',False)
    filepath = json_file_result.get('filepath',"/")

    # If json file was read, retrieve contents to see if pkmn entry exists
    pkmn_json = json_file_result.get('json',{})
    pkmn_result = pkmn_json.get(query, "")
    if not pkmn_result:
        pkmn_result = getPokemonFromApi(query)
        # If there were issues earlier reading/creating the json file simply return the result
        # Otherwise, try to save the file if there was no error
        if not pkmn_result['error'] and has_file is True:
            commons.updateJsonFileContents(pkmn_result,query,filepath)
    return pkmn_result

def getPokemonFromApi(query=""):
    '''Retrieve pokemon info from PokeAPI '''
    site_url = "https://pokeapi.co/"
    url = 'http://pokeapi.co/api'
    version = 'v2'
    command = 'pokemon'

    # How many digits are needed for pkmn id's
    pkmn_digits = 3
    
    # Default MissingNo values
    default_id = 0
    default_name = "MissingNo"
    default_sprite = "" # To Do?
    default_types = ["None"]

    # Wrapper to return result
    pkmn_wrapper = {
        'pkmn_id':str( default_id ).zfill(pkmn_digits),
        'pkmn_name':default_name,
        'pkmn_sprite':default_sprite,
        'pkmn_types':default_types,
        'source':site_url,
        'error':""
        }

    # If query is not empty
    if query:
        r = requests.post("{0}/{1}/{2}/{3}/".format(url, version, command, str(query).lower()))
        # Debug. Uncomment if needed
        # print(r.url)

        # Success
        if r.status_code == 200:
            result_dict = r.json()

            # Retrieve needed values
            # Default to MissingNo values if needed
            pkmn_id = result_dict.get('id', default_id)
            pkmn_name = result_dict.get('name', default_name)
            pkmn_sprite = result_dict.get('sprites', dict(front_default="")).get('front_default',default_sprite)
            
            pkmn_types = []
            pkmn_types_list = result_dict.get('types', [])
            for pkmn_types_list_dict in pkmn_types_list:
                pkmn_types.append( pkmn_types_list_dict.get('type',{}).get('name',"none") )

            # Add results to dict
            pkmn_wrapper.update({
                'pkmn_id':str( pkmn_id, ).zfill(pkmn_digits),
                'pkmn_name':pkmn_name,
                'pkmn_sprite':pkmn_sprite,
                'pkmn_types':pkmn_types,
                })
            
        elif r.status_code == 404:
            pkmn_wrapper['error'] = "No pokemon found for {0}".format(str(query))
        else:
            pkmn_wrapper['error'] = "Something bad happened. Error Code: " + str(r.status_code)
    else:
        pkmn_wrapper['error'] = "No valid pkmn name entered. (e.g. Pikachu)"
        
    return pkmn_wrapper

def getRandomQuote():
    site_url = "https://forismatic.com/en/"
    url = 'https://api.forismatic.com/api'
    version = '1.0/'
    params = {'method':"getQuote",'format':"json",'lang':"en"}

    result_dict = dict(error="")
    r = requests.post("{0}/{1}/".format(url, version), params=params)
    if r.status_code == 200:
        result = r.json()
        result_dict = {
            'quote':result.get('quoteText',""),
            'author':result.get('quoteAuthor',""),
            'url':result.get('quoteLink',site_url),
            'error':""
            }
        return result_dict
    return dict(error="No quote found.")

'''
def getSpanishMiriamWebster(word, key_id=""):
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
    else:
        return "Something else happened. Error Code: " + str(r.status_code)
'''

def getJishoPage(query):
    # Dict for our results
    wrapper = {
        'writing':"",
        'reading':"",
        'definitions':[],
        'speech_type':[],
        'error':""
        }

    # GET command
    url = 'http://jisho.org/api'
    version = 'v1'
    command = 'search/words'
    
    params = urllib.parse.urlencode(dict(keyword=query))
    r = requests.get("{0}/{1}/{2}".format(url, version, command), params=params)
    if r.status_code == 200:
        return parseJishoPage(r.json(), wrapper)
    else:
        wrapper['error'] =  "Something else happened. Error Code: " + str(r.status_code)
    return wrapper

def parseJishoPage(json, wrapper, result_index=0):
    data_list = json.get('data', [])
    data_size = len( data_list )
    
    if data_list:
        if result_index > data_size - 1:
            result_index = data_size - 1
        # Retrieve the result based on the result_index
        data_dict = data_list[result_index]
        jp_list = data_dict.get('japanese', [])
        senses_list = data_dict.get('senses', [])
        
        if jp_list:
            jp_dict = jp_list[0] # Retrieve first item (should be only item)

            # Retrieve writing and reading
            wrapper['writing'] = jp_dict.get('word', "")
            wrapper['reading'] = jp_dict.get('reading', "")
            
        if senses_list:
            senses_dict = senses_list[0] # Retrieve first item (should be only item)
            eng_def_list = senses_dict.get('english_definitions', [])
            speech_type_list = senses_dict.get('parts_of_speech', [])

            # Retrieve english definitions
            for eng_def in eng_def_list:
                wrapper['definitions'].append(eng_def)
            # Retrieve speech type
            for speech in speech_type_list:
                wrapper['speech_type'].append(speech)
        return wrapper

    wrapper['error'] = "No results found for the word requested."
    return wrapper

# System imports
import urllib

# 3rd Party Imports
import requests

# Personal Library
import commons


def get_pokemon(query=""):
    # Retrieve requested pokemon info from json file. If none exists, retrieve from get_pokemon_from_api(...)
    query = str(query).lower()

    # Retrieve relative path to the json file
    rel_path = "pkmn/"
    filename = "pkmn_names.json"

    # Read from the json file, create if needed
    json_file_result = commons.get_json_from_file(rel_path, filename, True)
    has_file = json_file_result.get('success', False)
    filepath = json_file_result.get('filepath', "/")

    # If json file was read, retrieve contents to see if pkmn entry exists
    pkmn_result = json_file_result.get('json', {}).get(query, "")
    if not pkmn_result:
        pkmn_result = get_pokemon_from_api(query)
        # If there were issues earlier reading/creating the json file simply return the result
        # Otherwise, try to save the file if there was no error
        if not pkmn_result['error'] and has_file is True:
            commons.update_file_to_json_contents(pkmn_result, query, filepath)
    return pkmn_result


def get_pokemon_from_api(query=""):
    # Retrieve pokemon info from PokeAPI
    site_url = "https://pokeapi.co/"
    url = 'http://pokeapi.co/api'
    version = 'v2'
    command = 'pokemon'

    # How many digits are needed for pkmn id's
    pkmn_digits = 3
    
    # Default MissingNo values
    default_id = 0
    default_name = "MissingNo"
    default_sprite = ""  # To Do?
    default_types = ["None"]

    # Wrapper to return result
    pkmn_wrapper = {
        'pkmn_id': str(default_id).zfill(pkmn_digits),
        'pkmn_name': default_name,
        'pkmn_sprite': default_sprite,
        'pkmn_types': default_types,
        'source': site_url,
        'error': ""
        }

    # If query is not empty
    if query:
        # If query is missingno, return immediately
        if query == "missingno":
            return pkmn_wrapper
        
        r = requests.post("{0}/{1}/{2}/{3}/".format(
            url, version, command, query), timeout=30)
        # Debug. Uncomment if needed
        # print(r.url)

        # Success
        if r.status_code == 200:
            result_dict = r.json()

            # Retrieve needed values
            # Default to MissingNo values if needed
            pkmn_id = result_dict.get('id', default_id)
            pkmn_name = result_dict.get('name', default_name)
            pkmn_sprite_dict = result_dict.get('sprites', {})
            pkmn_sprite = pkmn_sprite_dict.get('front_default', default_sprite)
            pkmn_types_list = result_dict.get('types', [])
            pkmn_types = [pkmn_types.get('type', {}).get('name', "none")
                          for pkmn_types in pkmn_types_list]

            # Add results to dict
            pkmn_wrapper.update({
                'pkmn_id': str(pkmn_id).zfill(pkmn_digits),
                'pkmn_name': pkmn_name,
                'pkmn_sprite': pkmn_sprite,
                'pkmn_types': pkmn_types,
                })
            
        elif r.status_code == 404:
            pkmn_wrapper['error'] = "No pokemon found for {0}".format(str(query))
        else:
            pkmn_wrapper['error'] = "Something bad happened. Error Code: " + str(r.status_code)
    else:
        pkmn_wrapper['error'] = "No valid pkmn name entered. (e.g. Pikachu)"
        
    return pkmn_wrapper


def get_random_quote():
    site_url = "https://forismatic.com/en/"
    url = 'https://api.forismatic.com/api'
    version = '1.0/'
    params = {'method': "getQuote", 'format': "json", 'lang': "en"}

    r = requests.post("{0}/{1}/".format(url, version),
                      params=params,
                      timeout=30)
    if r.status_code == 200:
        result = r.json()
        result_dict = {
            'quote': result.get('quoteText', ""),
            'author': result.get('quoteAuthor', ""),
            'source': result.get('quoteLink', site_url),
            'error': ""
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


def get_jisho_page(query):
    # GET command
    url = 'http://jisho.org/api'
    version = 'v1'
    command = 'search/words'
    
    params = urllib.parse.urlencode(dict(keyword=query))
    r = requests.get("{0}/{1}/{2}".format(url, version, command),
                     params=params,
                     timeout=30)
    if r.status_code == 200:
        return parse_jisho_page(r.json())
    else:
        return dict(error=("Something else happened. Error Code: " + str(r.status_code)))


def parse_jisho_page(json, result_index=0):
    wrapper = {'source': "http://jisho.org"}
    
    data_list = json.get('data', [])
    data_size = len(data_list)
    
    if data_list:
        # Get requested index. If size is smaller than index, get last index of the list
        if result_index > data_size - 1:
            result_index = data_size - 1
        
        # Retrieve the result based on the result_index
        data_dict = data_list[result_index]
        jp_list = data_dict.get('japanese', [])
        senses_list = data_dict.get('senses', [])

        # Retrieve first item of jp_list (should be only item)        
        jp_dict = jp_list[0] if jp_list else {}
        # Retrieve writing and reading
        wrapper['writing'] = jp_dict.get('word', "")
        wrapper['reading'] = jp_dict.get('reading', "")

        # Retrieve first item of senses_list (should be only item)
        senses_dict = senses_list[0] if senses_list else {}
        eng_def_list = senses_dict.get('english_definitions', [])
        speech_type_list = senses_dict.get('parts_of_speech', [])
        
        # Retrieve english definitions and types of speech
        wrapper['definitions'] = (eng_def for eng_def in eng_def_list)
        wrapper['speech_type'] = (speech for speech in speech_type_list)
    else:
        wrapper['error'] = "No results found for the word requested."
    
    return wrapper


def get_random_uk_doge():
    doge_wrapper = {'source': "https://thedogapi.co.uk"}
    
    url = 'https://api.thedogapi.co.uk'
    version = 'v2'
    command = 'dog.php'
    params = dict(limit=1)

    r = requests.get(
        "{0}/{1}/{2}".format(url, version, command),
        params=params,
        timeout=30)
    if r.status_code == 200:
        result = r.json()
        result_list = result.get('data', [{}])[0]
        doge_wrapper['doge_url'] = result_list.get('url', "")
    else:
        doge_wrapper['error'] = "Couldn't woof :sob: Error Code: " + str(r.status_code)
    return doge_wrapper


def get_math_js(expr_list):
    # POST Command
    url = 'http://api.mathjs.org'
    version = 'v1'
    expr_dict = {'expr': [], 'precision': 4}
    # headers = {'content-type': 'application/json'}

    if type(expr_list) is not str:
        for expr in expr_list:
            expr_dict['expr'].append(expr)
    else:
        expr_dict['expr'].append(expr_list)

    expr_json = expr_dict
    print(expr_json)
    r = requests.post(
        "{0}/{1}/".format(url, version),
        json=expr_json,
        timeout=30)
    if r.status_code == 200:
        return r.json()
    return r.status_code


def get_dictionary(word: str="", app_id: str="", app_key: str=""):
    dict_wrapper = {'source': "https://www.oxforddictionaries.com"}
    language = 'en'

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()

    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key}, timeout=30)
    if r.status_code == 200:
        result = r.json()
        results = result.get('results', [{}])
        result_dict = results[0]

        # Now retrieve the Lexical Entries, currently only retrieve the first entry
        lexical_entries = result_dict.get('lexicalEntries', [{}])
        entries = lexical_entries[0]
        entries_list = entries.get('entries', [{}])
        entries_item = entries_list[0]

        # From the entries, retrieve its first entry
        dict_wrapper['etymology'] = (etymology for etymology in entries_item.get('etymologies', []))
        senses_list = entries_item.get('senses', [])
        dict_wrapper['definitions'] = (senses_item.get('definitions', [""])[0] for senses_item in senses_list)
    else:
        dict_wrapper['error'] = "Couldn't find my dictionary :sob: Error Code: " + str(r.status_code)
    return dict_wrapper




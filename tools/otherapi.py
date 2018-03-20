# System imports
import urllib
from html import unescape
from datetime import datetime
from io import BytesIO

# 3rd Party Imports
from json import JSONDecodeError
import praw
from PIL import Image
import requests
import requests.auth
from requests.exceptions import MissingSchema


# Personal Library
from tools import config
from tools.commons import get_random_int, get_suffled_list
from tools.postgres_handler import PokemonSearch, Token


def get_pokemon(query: str):
    # Retrieve requested pokemon info from json file. If none exists, retrieve from get_pokemon_from_api(...)
    number = None
    name = None
    if query is not None:
        if query.isdigit():
            number = query
        else:
            name = str(query).lower()

    url = 'http://pokeapi.co/api'

    """
    Commenting this out since using database instead of local file
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
    """

    # Check database if pokemon was queried before. No need to call API if so.
    pkmn = PokemonSearch()
    pkmn_result = pkmn.get_pkmn(name, number)
    if pkmn_result:
        pkmn_result['source'] = url
        return pkmn_result
    else:
        # Use API to retrieve pokemon
        pkmn_result = get_pokemon_from_api(str(query).lower())
        # Save the result to database if there was no error
        if not pkmn_result['error']:
            pkmn.save_pkmn_data(pkmn_result)
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
    default_types = ["???"]

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
        try:
            result = r.json()
            result_dict = {
                'quote': result.get('quoteText', ""),
                'author': result.get('quoteAuthor', ""),
                'source': result.get('quoteLink', site_url),
                'error': ""
                }
            return result_dict
        except JSONDecodeError as jsonex:
            print(r.text)
            return dict(error="Site gave me an error again. Error: " + str(jsonex))
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
    r = requests.post("{0}/{1}/".format(url, version), json=expr_json, timeout=30)
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
        dict_wrapper['definitions'] = (senses_item.get('definitions', [""])[0]
                                       for senses_item
                                       in senses_list
                                       if senses_item.get('definitions'))
    else:
        dict_wrapper['error'] = "Couldn't find the word in my dictionary :sob: Error Code: " + str(r.status_code)
    return dict_wrapper


def get_trivia_question(difficulty: str= None, question_type: str= None, category: int= 31):
    url = 'https://opentdb.com/'
    command_token = "api_token.php"
    command_request = "api.php"
    source = 'https://opentdb.com/'
    api_name = "open_trivia"

    # First retrieve a token id. If non exists, request one from the site
    token = Token()
    token_id, create_date = token.get_token(api_name)  # retrieve token from database
    request_token = True
    if token_id:
        date_lambda = (datetime.now() - create_date)
        hours = date_lambda.seconds//3600
        request_token = hours >= 6

    # If we require a new token
    if request_token:
        params = dict(command='request')
        r = requests.get(url + command_token, params=params, timeout=30)
        if r.status_code == 200:
            result = r.json()
            token_id = result.get('token', None)

        if token_id is None:
            return dict(error="Something bad happened in the backend. Please try again later.")
        else:
            token.update_token(api_name, token_id)  # update new token on the database

    # Actual query for the trivia
    params = dict(amount=1, category=category, token=token_id)
    if difficulty:
        params['difficulty'] = difficulty
    if question_type:
        params['type'] = question_type

    r = requests.get(url + command_request, params=params, timeout=30)
    if r.status_code == 200:
        result = r.json()

        response_code = result.get('response_code', 1)

        if response_code == 1:
            return dict(error="Couldn't find a question online whoops Error Code: " + str(response_code))
        elif response_code == 3:
            return dict(error="I shouldn't reach here. Call my dad pls. Error Code: " + str(response_code))
        elif response_code == 4:
            token.inactive_token(api_name)  # Set token to inactive
            return dict(error="Looks like you've answered all the questions friend. Questions will now repeat.")

        results = result.get('results', [{}])
        result_dict = results[0]

        # Randomly insert the correct answer with the wrong answers
        right_choice = unescape(result_dict.get('correct_answer', "???"))
        wrong_choices = get_suffled_list([unescape(choice) for choice in result_dict.get('incorrect_answers', [])])
        correct_index = get_random_int(len(wrong_choices) - 1) if wrong_choices else 0
        wrong_choices.insert(correct_index, right_choice)

        # Set required data
        return dict(
            type=result_dict.get('type'),
            difficulty=result_dict.get('difficulty', ""),
            question=unescape(result_dict.get('question')),
            correct=correct_index + 1,  # since choices start at (1)
            correct_answer=right_choice,
            choices=wrong_choices,
            source=source)
    else:
        return dict(error="Couldn't find a question online whoops Error Code: " + str(r.status_code))

'''
def get_thinking_image_url(subreddit: str='Thinking'):
    # Retrieve a token from reddit for OAuth2
    request_token, request_token_type = get_reddit_token()
    if not request_token:
        print("Error on Retrieving Reddit Token")
        return dict(error=":thinking:")

    # Get actual query if done
    url = "https://oauth.reddit.com/r/{0}/top/.json".format(subreddit)
    params = dict(sort="top", t="week", limit="30")
    headers = {'Authorization': "{0} {1}".format(request_token_type, request_token),
               'User-Agent': config.reddit_user_agent}

    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        result = r.json()
        result_data = result.get('data', {})
        image_url_list = []
        for children in result_data.get('children', []):
            data = children.get('data')
            if (not data
                    or data.get('post_hint') == "self"
                    or data.get('locked', "true") == "true"):
                continue
            thumbnail = data.get('thumbnail')
            image = data.get('url')
            image_url_list.append(image if image else thumbnail)
        return dict(img_list=image_url_list)
    print("Error while requesting reddit data " + str(r.status_code))
    return dict(error=":thinking:")


def get_reddit_token():
    url = "https://www.reddit.com/api/"
    version = "v1"
    command = "/access_token"
    client_auth = requests.auth.HTTPBasicAuth(config.reddit_client_id, config.reddit_secret_id)
    post_data = dict(grant_type="client_credentials")
    headers = {'User-Agent': config.reddit_user_agent}
    r = requests.post(url + version + command, auth=client_auth, data=post_data, headers=headers)
    result = r.json()
    return result.get('access_token'), result.get('token_type')
'''


def get_subreddit_image_list(subreddit: str='Thinking'):
    try:
        return dict(img_list=[submission.url
                              for submission
                              in get_praw().subreddit(subreddit).hot(limit=20)
                              if (hasattr(submission, 'post_hint')
                                  and submission.post_hint == 'image')])
    except Exception as e:
        return dict(error=str(e))


def get_praw():
    return praw.Reddit(client_id=config.reddit_client_id,
                       client_secret=config.reddit_secret_id,
                       user_agent=config.reddit_user_agent)
    #  print(reddit.auth.limits)
    #  if reddit.auth.limits.get('remaining', 0) < 59:
    #      raise PRAWException("Reddit called too fast. Try again in a minute.")


def paste_image_from_source(source: str, image: str="https://cdn.discordapp.com/emojis/401429201976295424.png"):
    try:
        resp = requests.get(source)
        if resp.status_code == 200 and resp.headers.get("content-type", "") in ("image/png", "image/jpeg"):
            with BytesIO(resp.content) as content:
                background = Image.open(content)
                resp2 = requests.get(image)
                if resp2.status_code == 200 and resp2.headers.get("content-type", "") in ("image/png", "image/jpeg"):
                    with BytesIO(resp2.content) as content2:
                        foreground = Image.open(content2)
                        background.paste(foreground, (0, background.height - foreground.height), foreground)
                        with BytesIO() as result:
                            background.save(result, format('PNG'))
                            return result.getvalue()
    except MissingSchema:
        return None
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print("NOTE: " + exc)
        pass
    return None

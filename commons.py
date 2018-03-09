from random import randint, shuffle
from decimal import Decimal
import os
import json


def to_lower(string: str):
    return string.lower()


def get_random_int(size: int):
    return randint(0, size)


def get_random_item(items):
    return items[get_random_int(len(items) - 1)] if items else items


def get_suffled_list(items):
    shuffle(items[:])
    return items


def get_random_math_question():
    operations = ("+", "-", "*", "/")

    f_num = get_random_int(100)
    l_num = get_random_int(100)

    if l_num == 0:
        l_num = 1 # prevent black hole

    action = get_random_item(operations)
    expression = "{0}{1}{2}".format(str(f_num), str(action), str(l_num))
    if action == "+":
        answer = f_num + l_num
    elif action == "-":
        answer = f_num - l_num
    elif action == "*":
        answer = f_num * l_num
    elif action == "/":
        answer = round(Decimal(f_num/l_num), 2)
        expression += " and round it to the nearest hundredths"
    return expression, answer


def get_json_from_file(directory: str= "/", filename: str= "", relative_dir: bool=False, filepath: str=None):
    result = {'success': True, 'json': {}, 'filepath': ""}

    # If filepath is not set, retrieve from directory and filename
    if not filepath:
        if relative_dir is True:
            relative_path = os.path.dirname(__file__)
            directory = os.path.join(relative_path, directory)
        # Directory location, we need to create directory if not exists
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                print("OSError: " + str(e))
                result['success'] = False
                return result
        # File's path, create a json file if not exists; otherwise, we parse the json file data
        abs_filename_path = os.path.join(directory, filename)
    else:
        abs_filename_path = filepath

    result['filepath'] = abs_filename_path
    if os.path.exists(abs_filename_path):
        # If file already exists, try to read the contents
        try:
            with open(abs_filename_path, "r") as f:
                result['json'] = json.load(f)
        except ValueError as e:
            print("ValueError: " + str(e))
    else:
        # If no file exists, try to create the file by dumping an empty json file
        try:
            with open(abs_filename_path, "w") as f:
                json.dump(result['json'], f)
        except Exception as e:
            print("Writing exception: " + str(e))
            result['success'] = False

    return result


def update_file_to_json_contents(result_dict: dict={}, key_to_update: str=None, filepath: str= ""):
    if not result_dict:
        return False

    # Create a copy so the original is intact
    result_copy = dict(result_dict)
    # Remove error key before saving
    result_copy.pop('error', None)

    # First if key_to_update exists, we need to retrieve the updated file (if file doesn't exist, create)
    if key_to_update:
        result_updated = get_json_from_file(filepath=filepath)
        success = result_updated.get('success', False)
        dict_to_save = result_updated.get('json', {})
        if success is True:
            dict_to_save[key_to_update] = result_copy
        else:
            return False
    # Otherwise we assume result_dict is the entire file
    else:
        dict_to_save = result_copy
        
    # Now to save
    try:
        with open(filepath, 'w') as f:
            json.dump(dict_to_save, f)
    except Exception as e:
        print("Exception when writing the file: " + str(e))
        return False
    return True

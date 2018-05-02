from apiai import ApiAI
from tools import dialogflow_id
import json
import logging


def talk_ai(query, session_id):
    """Send query to ApiAI API"""
    ai = ApiAI(dialogflow_id)
    request = ai.text_request()
    request.lang = 'de'  # default/'en'
    request.session_id = session_id
    request.query = query
    return get_fulfillment_speech(request.getresponse())


def get_fulfillment_speech(response):
    """Retrieve the default response from the apiai response"""
    result = json.load(response)
    return result.get('result', {}).get('fulfillment', {}).get('speech', "wut")

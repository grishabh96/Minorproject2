import os
import random
import ctypes
from templates.text import TextTemplate
import time
import requests
import config
from templates.generic import *
from templates.button import *
from templates.text import TextTemplate

ZODIAC_API_KEY = os.environ.get('ZODIAC_API_KEY', config.ZODIAC_API_KEY)


def process(input, entities=None):
    output = {}
    
    try:
        
       baseURL = "https://json.astrologyapi.com/v1/"
       resp = requests.post(url, auth=('601227', 'cf5463916fdd1cfa5b96889ec2590621'))
       print resp.json()

    except:
        error_message = 'There was some error while retrieving data from Crickbuzz.'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output

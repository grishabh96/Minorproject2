import json
import os
import sys

import requests
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import modules



import config
from src import *
from templates.text import TextTemplate
headers = {'Accept' : 'application/json', 'user_key': '1cbfdfcd7d180e9ec46ad63ed9efd3d5', 'User-Agent': 'curl/7.35.0'}

WIT_AI_ACCESS_TOKEN = os.environ.get('WIT_AI_ACCESS_TOKEN', config.WIT_AI_ACCESS_TOKEN)


def generate_postback(module):
    return {
        'intent': module,
        'entities': None
    }






def process_query(input):
    # For local testing, mock the response from Wit
    with open(config.WIT_LOCAL_DATA) as wit_file:
        wit_local_data = json.load(wit_file)
        if input in wit_local_data:
            return wit_local_data[input]['intent'], wit_local_data[input]['entities']
    try:
        r = requests.get('https://api.wit.ai/message?v=20160420&q=' + input, headers={
            'Authorization': 'Bearer %s' % WIT_AI_ACCESS_TOKEN
        })
       
        data = r.json()
        intent = data['outcomes'][0]['intent']
        entities = data['outcomes'][0]['entities']
        confidence = data['outcomes'][0]['confidence']
        if intent in src.__all__ and confidence > 0.5:
            return intent, entities
        else:
            return None, {}
    except:
        return None, {}


def search(input, sender=None, postback=False):
    x=input.split(' ')
    if x[0]=='mail' or x[0]=='solve':
        intent=x[0]
        entities=None
    elif postback:
        payload = json.loads(input)
        intent = payload['intent']
        entities = payload['entities']
    else:
        intent, entities = process_query(input)
        
    if intent is not None:
        if intent in src.__personalized__ and sender is not None:
            r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token': os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
            })
            if entities is None:
                entities = {}
            entities['sender'] = r.json()
        if intent=='mail' or intent=='solve' :
            if intent=='mail':
                sys.modules['modules.src.' + 'mail'].process(x[1],input)
                return TextTemplate('DATA SENT').get_message()
            else:
                k=sys.modules['modules.src.' + 'solve'].process(x[1])
                return TextTemplate(k).get_message()
        else:    
            data = sys.modules['modules.src.' +intent].process(intent,entities)
            if data['success']:
                return data['output']
            else:
                if 'error_msg' in data:
                    return data['error_msg']
                else:
                    return TextTemplate('Something didn\'t work as expected! I\'ll report this to my master.').get_message()
    else:
        return TextTemplate(
            'I\'m sorry; I\'m not sure I uncccderstand what you\'re trying to say.\nTry typing "help" or "request"').get_message()


def get_reviews(id):
    url = "https://developers.zomato.com/api/v2.1/reviews?res_id=%s&count=5" % (id)
    try:
        response = requests.get(url, headers=headers)
    except:
        return TextTemplate('I\'m facing some issues, try again later').get_message()
    if response.status_code == 200:
        data = response.json()
        count = data["reviews_count"]
        if count == 0:
            return TextTemplate('Sorry, no reviews are available').get_message()
        else:
            template_list = []
            for review in data['user_reviews']:
                template_list.append({'text': review["review"]['rating_text'] + ' - ' + str(review["review"]['rating']) + '/5' + '\n' +
                         review["review"]['review_text']})
            pprint(template_list)
            return template_list
    else:
        return TextTemplate('I\'m facing some issues, try again later').get_message()


def get_directions(id):
    url='https://developers.zomato.com/api/v2.1/restaurant?res_id='+id
    try:
        response = requests.get(url, headers=headers)
    except:
            return TextTemplate('I\'m facing some issues, try again later').get_message()
    if response.status_code == 200:
        data = response.json()
        lat = data['location']['latitude']
        lon = data['location']['longitude']
        location = 'http://www.google.com/maps/place/'+lat+','+lon
        return TextTemplate('Here you go! :)'+'\n\n'+location).get_message()
    else:
        return TextTemplate('I\'m facing some issues, try again later').get_message()


def ans(input, sender=None, postback=False):
    
    from chatterbot import ChatBot

    chatbot = ChatBot(
        "SQLMemoryTerminal",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'sorry guys didnt get it'
        },
            
        {
            
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter'
        }
        
        
    ],
    trainer='chatterbot.trainers.ListTrainer',
       
    )

    from chatterbot.trainers import ListTrainer

    conversation = [
        "Hello",
        "Hi there!",
        "How are you doing?",
        "I'm doing great..how are you?",
        "i am good",
        "this is good to hear ",
        "how can i help you?just type help",
        "thank you"
        "You're welcome."
    ]

    chatbot.set_trainer(ListTrainer)
    chatbot.train(conversation)

    chatbot.train([
        'what is you name',
        'my name is rishabh?  what about you',
        'i am jarvis bro',
        'cool can you help me?',
        'yes type help'
    ])
    conversation=({
        'hi jarvis! how are you?',
        'I am fine! what about you',
        'I am good too . Can you please help me?',
        'yestell me what help do you want'
        })

    chatbot.train(conversation)

    coversation=({
        'i am bored!'
        'you can watch videos..just type videos and your input'
        'ok jarvis'
        })
    chatbot.set_trainer(ListTrainer)
    chatbot.train(conversation)


        
    chatbot_input=chatbot.get_response(input)
    if chatbot_input=='sorry guys didnt get it':
        return search(input)
    else:
        return TextTemplate(str(chatbot_input)).get_message()

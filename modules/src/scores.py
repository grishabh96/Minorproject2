import os

import requests
import datetime

import config
from templates.button import *
from templates.text import TextTemplate

SCORES_API_KEY = os.environ.get('SCORES_API_KEY', config.SCORES_API_KEY)




def process(input, entities=None):
    output = {}
    source = 'cricketScore'  # Can add more sources in future
    try:
        
        r = requests.get('http://cricapi.com/api/matches/' + SCORES_API_KEY )
        data1 = r.json()
        assert (len(data1['matches']) > 0)
        now=datetime.datetime.now()
        p=now.isoformat()
        for match in data1['matches']:
            if p is match['date']:
                id=match['unique_id']
                team1=match['team-1']
                team2=match['team-2']
                template = TextTemplate()
                d = requests.get('http://cricapi.com/api/cricketScore?' + 'unique_id=' + id, params={
                'apikey': SCORES_API_KEY }) 
                data2 = d.json()
                count=0
                assert (len(data2['data']) > 0)
                for scores in data2['data']:
                     count=count+1
                     score=scores['score']
                     template.set_text('Here are the scores of match between' + team1 + ' and ' + team2 + ':\n' + score)
                     template.set_post_text('\n- Powered by MusiXmatch')
                     template.set_limit(TEXT_CHARACTER_LIMIT)

                     template = ButtonTemplate(template.get_text())
                     output['input'] = input
                     output['output'][count-1] = template.get_message()
                     output['success'] = True
    except:
        error_message = 'There was some error while retrieving data from NewsAPI.'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output

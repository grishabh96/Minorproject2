from pprint import pprint
import sys,os
import requests, json
from templates.button1 import *
from templates.generic1 import *
import geocoder

headers = {'Accept': 'application/json', 'user_key': '1cbfdfcd7d180e9ec46ad63ed9efd3d5', 'User-Agent': 'curl/7.35.0'}



def get_template(restaurants):
    template = GenericTemplate()
    for restaurant in restaurants:
        template.add_element(title=restaurant['name']+' | Rating : '+str(restaurant['rating'])+'/5', subtitle='Cost for 2 : '+str(restaurant['budget'])+' |  Locality: '+restaurant['locality'],item_url=restaurant['url'],
                             image_url=restaurant['image_url'],buttons=[
                        {
                           "type": "web_url",
                           "url": restaurant['url'],
                           "title": "Visit Website"
                       },
                       {
                           "type": "postback",
                           "title": "Get Reviews",
                           "payload": "get_reviews!"+restaurant['id']
                       },
                       {
                           "type": "postback",
                           "title": "Get Directions",
                           "payload": "get_directions!"+restaurant['id']
                       }])
    pprint(template)
    return template


def process(action,entities=None):
    output = {}
    g = geocoder.ip('me')
    lat=28.667
    lon=77
    print(g.latlng)
    url = 'https://developers.zomato.com/api/v2.1/search?count=10&sort=(Math.abs(location_lat-g.lat)+Math.abs(location_lon-g.lng))&order=asc' + '&lat=' + str(
        lat) + '&lon=' + str(lon)
    #if parameters['cuisines'] is not None:
        #url += "&cuisines=" + parameters['cuisines']
    try:
        r = requests.get(url, headers=headers)
        restaurants = []
        if r.status_code != 200:
            print "Api Issues"
            return
        if len(r.json()['restaurants']) <= 0:
            print "Api Issues"
            return
        for res in r.json()['restaurants']:
            rest = {'budget': res['restaurant']['currency'] + ' ' + str(res['restaurant']['average_cost_for_two']),
                    'id': res['restaurant']['id'], 'name': res['restaurant']['name'], 'url': res['restaurant']['url'],
                    'location_lat': res['restaurant']['location']['latitude'],
                    'location_lon': res['restaurant']['location']['longitude'],
                    'rating': res['restaurant']['user_rating']['aggregate_rating'],
                    'locality': res['restaurant']['location']['locality'], 'image_url': res['restaurant']['thumb']}
            restaurants.append(rest)
        # pprint(restaurants)
        template1 = get_template(restaurants)
        # pprint(template1.get_message())
        output['input'] = input
        output['output'] = template1.get_message()
        output['success'] = True
    except Exception as E:
        print E
        exc_type,exc_obj,exc_tb=sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print exc_type,fname,exc_tb.tb_lineno
        error_message = 'I couldn\'t find any Restaurant matching your query.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - Some restaurants in guwahati under 1000 Rs'
        error_message += '\n  - Any place to eat in Mumbai'
        error_message += '\n  - I\'m Hungry'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output




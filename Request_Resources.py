import requests
import json
from private import CAT_API_KEY, CAT_API_URL, DEFAULT_RESOURCE

class Request_Resources(object):
    def __init__(self):
        pass
    def obtein_cat_picture(self):
        raw_cat = requests.get(CAT_API_URL,  headers={"x-api-key":CAT_API_KEY})
        try:
            json_cat = json.loads(raw_cat.text)
            return json_cat[0]['url']
        except:
            return DEFAULT_RESOURCE
import requests
import json
from private import CAT_API_KEY, CAT_API_URL, DEFAULT_RESOURCE, AEMET_KEY

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
    def weather(self):
        pass

import requests

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/09059" # for burgos

querystring = {"api_key":AEMET_KEY}



response = requests.request("GET", url, headers={'cache-control': "no-cache"}, params=querystring)
json_response = json.loads(response.text)
print(json_response)
response = requests.request('GET', json_response['datos'])
json_response = json.loads(response.text)
for prov in json_response:
    # if prov['prediccion'][0] == "BURGOS":
    pass
print(  json.dumps(prov['prediccion']['dia'][0]['temperatura'], indent=4))
# print(response.text)

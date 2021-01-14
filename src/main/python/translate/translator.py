import uuid
from os import path

import requests

from preprocessing.common import remove_quotes


class Translator:
    """
    Translator based on azure translation service
    """

    def __init__(self):
        base_path = path.dirname(__file__)
        file_path = path.abspath(path.join(base_path, "..", "..", "resources", "azure.subscription.key"))
        f = open(file_path, "r")
        self.subscription_key = f.readline()
        self.endpoint = 'https://api.cognitive.microsofttranslator.com/'
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': 'westeurope',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def pl_to_en(self, text):
        path_ = '/translate?api-version=3.0'
        params = '&from=pl&to=en'
        constructed_url = self.endpoint + path_ + params
        body = [{
            'text': "'" + text + "'"
        }]
        response = requests.post(constructed_url, headers=self.headers, json=body)
        response = response.json()
        result = response[0]['translations'][0]['text']
        return remove_quotes(result)

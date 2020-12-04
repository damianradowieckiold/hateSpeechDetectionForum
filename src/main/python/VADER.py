# Based on examples from project https://github.com/cjhutto/vaderSentiment

import json

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentence=input("Wprowadz linie do oceny: ")
api_url = "http://mymemory.translated.net/api/get?q={}&langpair={}|{}".format(sentence, 'pl-PL', 'en-US')
hdrs = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
response = requests.get(api_url, headers=hdrs)
response_json = json.loads(response.text)
translation = response_json["responseData"]["translatedText"]

analyzer = SentimentIntensityAnalyzer()
print(translation)
print(analyzer.polarity_scores(translation))
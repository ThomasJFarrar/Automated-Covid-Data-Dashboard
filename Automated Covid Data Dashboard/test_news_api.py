import json
import os
import requests
from newsapi import NewsApiClient

with open(os.path.dirname(__file__) + "/config.json") as config_file:
    config = json.load(config_file)
    api_key = config["news"]["api_key"]
    country = config["news"]["country"]
    
newsapi = NewsApiClient(api_key)
top_headlines = newsapi.get_top_headlines(country)

def test_news_api_status() -> None:
    assert top_headlines['status'] == "ok"

def test_news_api_type() -> None:
    assert isinstance(top_headlines, dict)

def test_news_api_countryerror() -> None:
    language = "uk"
    newsapi = "https://newsapi.org/v2/top-headlines?country=%&sapiKey=%s" % (country, api_key)
    response = requests.get(newsapi)
    assert response.status_code == 400    

def test_news_api_noapikey() -> None:
    api_key = ""
    newsapi = "https://newsapi.org/v2/top-headlines?country=%s&apiKey=%s" % (country, api_key)
    response = requests.get(newsapi)
    assert response.status_code == 401
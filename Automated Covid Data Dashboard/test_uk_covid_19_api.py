import os
import json
import requests
from requests import get
from uk_covid19 import Cov19API

with open(os.path.dirname(__file__) + "/config.json") as config_file:
    config = json.load(config_file)
    location = config["covid_data"]["location"]
    location_type = config["covid_data"]["location_type"]

endpoint = "https://api.coronavirus.data.gov.uk/v1/data"
def test_covid_api_response():
    response = requests.get(endpoint)
    assert response.status_code == 200

test_parameters = {
    "date":"date",
    "areaName":"areaName",
    "areaCode":"areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeaths28DaysByPublishDate": "newDeaths28DaysByPublishDate",
    "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate"
}
test_location = ["areaType=" + location_type, "areaName=" + location]
def test_covid_api_type():
    results = Cov19API(filters = test_location, structure = test_parameters)
    data = results.get_json()
    assert isinstance(data, dict)


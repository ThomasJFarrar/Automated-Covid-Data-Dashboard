"""
This module is used with the covid_data_handler.py module to retrieve
up to date filtered news aticles, and schedule news updates.
"""

import json
import os
import logging
import requests

logging.basicConfig(filename = "Covid-19 Dashboard",
                    level = logging.DEBUG)

#Loading the config.json file
with open(os.path.dirname(__file__) + "/config.json",
            encoding = "utf-8") as config_file:
    config = json.load(config_file)
    country = config["news"]["country"]
    api_key = config["news"]["api_key"]
    covid_terms = config["news"]["filter_terms"]

#s = sched.scheduler(time.time, time.sleep)

def news_API_request(covid_terms:
                str = "Covid COVID-19 coronavirus") -> dict:
    """
    Retrieves the latest top news headlines for a given country,
    and filters the news articles with the given keywords.

    Keyword arguments:
    covid_terms - The keywords used to filter the news articles
    """
    base_url = "https://newsapi.org/v2/top-headlines?"
    covid_terms_list = list(covid_terms.split(" "))
    #Puts the Covid-19 filter terms into a list
    complete_url = (base_url + "country=" + country + "&apiKey=" +
                api_key + '&pageSize=100')
    response = (requests.get(complete_url)).json()
    articles = response["articles"]
    titles = [i["title"] for i in articles]
    filtered_titles = [] #Titles containing a keyword
    news = []
    for title in titles:
        if covid_terms_list[0] in title:
            filtered_titles.append(title)
        elif covid_terms_list[1] in title:
            filtered_titles.append(title)
        elif covid_terms_list[2] in title:
            filtered_titles.append(title)
    #Adding titles containing a keyword to list
    for filtered_title in filtered_titles:
        for entry in articles:
            if entry["title"] == filtered_title:
                news.append({"title": filtered_title,
                            "content": entry["description"]})
            #Finding the content of articles with matching title and
            # adding it to the news dictionary
    logging.info("News update request: filter terms: %s" , covid_terms)
    return news

def update_news(update_name: str) -> None:
    """Calls the News API request function."""
    news_API_request()

"""
This module is a program to integrate Covid-19 data into an
HTML template using Flask.

The features include:
    - Getting up to date local and national Covid-19 figures
    - Creating, modifying and removing scheduled updates
    - Getting up to date news on Covid-19
"""
import time
import os
import json
import sched
import logging
from flask import Flask, render_template, request, redirect
from uk_covid19 import Cov19API
from covid_news_handling import news_API_request, update_news

#Loading the config.json file
with open(os.path.dirname(__file__) + "/config.json", encoding = "utf-8") as config_file:
    config = json.load(config_file)
    location = config["covid_data"]["location"]
    location_type = config["covid_data"]["location_type"]

logging.basicConfig(filename = "Covid-19 Dashboard", encoding = "utf-8", level = logging.DEBUG)

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
scheduled_updates = []
displayed_updates = []
news = news_API_request()

def parse_csv_data(csv_filename: str) -> list:
    """
    Reading data from a given file, returning a list of strings for
    rows in the file.

    Keyword Arguments:
    csv_filename - Name of the csv file where data will be read from
    """
    with open(csv_filename, "r", encoding = "utf-8") as covid_csv_data:
        covid_csv_data.readlines()
    return covid_csv_data

def process_covid_csv_data(covid_csv_data: list) -> tuple:
    """
    Processing data, returning the relevant figures found within a
    list of strings.

    Keyword Arguments:
    covid_csv_data - The list of strings that will be processed
    """
    sorted_data = []
    for rows in covid_csv_data:
        row = rows.split(", ")
        for item in row:
            items = item.split(",")
        sorted_data.append(items)
        #Separates each string in the list and puts them into a new
        # sorted list of sublists
        last7days_cases = 0
        for i in range(7):
            last7days_cases += int(sorted_data[i + 3][6])
        #Summing the new cases by specimen date for the last 7 days,
        # ignoring the first entries as the data is imcomplete
        current_hospital_cases = int(sorted_data[1][5])
        #Indexing figure for current hospital cases.
        total_deaths = int(sorted_data[14][4])
        #Indexing figure for total deaths
        return last7days_cases, current_hospital_cases, total_deaths

def covid_API_request(location: str = "Exeter",
                    location_type: str = "ltla") -> dict:
    """
    Retrieves the latest Covid-19 figures for a given location,
    locally and nationally.

    Keyword arguments:
    location - The location of which area the data will be from
    location_type - The type of area that the data will be from
    """
    cases_and_deaths = {
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
    "hospitalCases": "hospitalCases"
    }
    local_only = ["areaType=" + location_type, "areaName=" + location]
    national_only = ["areaType=nation"]
    api = Cov19API(filters = local_only, structure = cases_and_deaths)
    local_data = api.get_json()
    api = Cov19API(filters = national_only, structure = cases_and_deaths)
    national_data = api.get_json()
    covid_data = {"local_data":local_data, "national_data":national_data}
    logging.info("Covid data update request: " + location + location_type)
    return covid_data

def process_covid_API_data(covid_data: dict) -> dict:
    """
    Processes the local and national Covid-19 data, returning the
    relevant figures.
    """
    local_data = covid_data["local_data"]
    national_data = covid_data["national_data"]
    cases_in_hospital = national_data["data"][0]["hospitalCases"]
    total_deaths = national_data["data"][0]["cumDeaths28DaysByPublishDate"]
    local_7_days_cases = 0
    for i in range(6):
        local_7_days_cases += (
            local_data["data"][i]["newCasesByPublishDate"])
    national_7_days_cases = 0
    for i in range(6):
        national_7_days_cases += (
            national_data["data"][i]["newCasesByPublishDate"])
    processed_covid_data = {
        "local7days_cases":local_7_days_cases,
        "national7days_cases":national_7_days_cases,
        "hospital_cases":cases_in_hospital,
        "deaths_total":total_deaths
        }
    return processed_covid_data

def schedule_covid_updates(update_interval: int, update_name: str) -> None:
    """
    Schedules an update by checking what the update needs to update and
    schedules it at the given time interval.

    Keyword arguments:
    update_interval - The number of seconds between the time the update
    was created to the time the update is set for.
    update_name - The name of the update that was set
    """
    for entry in scheduled_updates:
        if entry["update_name"] == update_name:
            if entry["with_covid_data"] == "covid-data":
                s.enter(update_interval, 1, covid_API_request)
                #Schedules a covid data update
            if entry["with_news"] == "news":
                s.enter(update_interval, 1,
                    update_news, (update_name, ))
                #Schedules a news update
            if entry["with_repeat"] == "repeat":
                s.enter(update_interval, 1,
                repeating_update, (update_name, ))
                #Schedules a repeat

def repeating_update(update_name: str) -> None:
    """
    Sets the update interval to 24 hours and calls the schedule covid
    update function to schedule another covid data update.

    Keyword arguments:
    update_name - The name of the update that was set
    """
    update_interval = 86400  # Number of seconds in 24 hours
    schedule_covid_updates(update_interval, update_name)


@app.route('/')
def redirect_to_index():
    """
    Redirects users who visit 127.0.0.1:5000/ to 127.0.0.1:5000/index.
    """
    return redirect('index')

@app.route('/index')
def index():
    """
    Formats and assembles functions to the HTML template.

    Adds the update title and description to a list of updates, which
    is displayed on the HTML template.
    Gets the user input from the HTML template and assigns them into
    functions.
    """
    s.run(blocking=False)  # Runs the sched module without blocking
    image = "image.png"  # Setting up the image in the HTML template
    favicon = "/static/favicon.ico" # Setting up the favicon in the HTML template
    title = "Covid Updates"  # Setting up the title in the HTML template
    update_name = request.args.get("two")
    with_repeat = request.args.get("repeat")
    with_covid_data = request.args.get("covid-data")
    with_news = request.args.get("news")
    remove_news = request.args.get("notif")
    remove_updates = request.args.get("update_item")
    if update_name:  # If the fields are submitted on the HTML template
        update_time = request.args.get("update")
        if update_time is None:
            #Checking to see if a time was entered
            logging.error("Update not created: Time not entered")
            return redirect('/index')
        for entry in scheduled_updates:
            if entry["update_name"] == update_name:
            #Checking to see if an update with the same name
            # already exists
                logging.error("Update not created: Update with "
                                "that name already existing")
                return redirect('/index')
        if with_covid_data is None and with_news is None:
        #Checking if the correct fields were entered
            logging.error("Update not created : Update Covid "
                            "data or Update news articles not selected")
            return redirect('/index')
        split_time = tuple(map(int, update_time.split(':')))
        #Splits the time the user set into hours and minutes
        update_interval = (abs(((split_time[0]
                            -int(time.gmtime().tm_hour)) * 60
                            +(split_time[1]
                            -int(time.gmtime().tm_min))) * 60))
        #Calculates the number of seconds between when the update
        # was created to when the update is set for
        scheduled_updates.append({
        "update_interval":update_interval,
        "update_name":update_name,
        "with_repeat":with_repeat,
        "with_covid_data":with_covid_data,
        "with_news":with_news
        })
        #Adding all the update details to a list
        schedule_covid_updates(update_interval,update_name)
        #Calling the schedule covid updates function to create
        # the update
        covid_data_content = ""
        news_content = ""
        repeat_content = ""
        if with_covid_data == "covid-data":
            covid_data_content = "Covid-19 data "
        if with_news == "news":
            news_content = "News "
        if with_repeat == "repeat":
            repeat_content = "Repeating "
        content = ("Your update is for " + str(update_time) +
                    " updating " + covid_data_content +
                    news_content + repeat_content+
                    "(Created at " +
                    str(time.strftime("%H:%M:%S", time.localtime())) +
                    ")")
        displayed_updates.append({
            "title":update_name,
            "content":content
        })
    if remove_updates:  # If an update is removed
        for entry in displayed_updates:
            if entry["title"] == remove_updates:
            #If the update name matches the one removed
                displayed_updates.remove(entry)
                #Removing the update from the Scheduled updates
                # column on the HTML template
                logging.info("Update removed : %s" , str(entry))
        for entry in scheduled_updates:
            if entry["update_name"] == remove_updates:
                scheduled_updates.remove(entry)
                #Removing the update from scheduled updates
    if remove_news: #If a news article is removed
        for entry in news:
            if entry["title"] == remove_news:
            #If the news article name matches the one removed
                news.remove(entry)  # Removes news article from list
                logging.info("News article removed : %s" , str(entry))
    return render_template(
        'index.html',
        image = image,
        favicon = favicon,
        title= title,
        location=location,
        nation_location="UK",
        local_7day_infections = local7days_cases,
        national_7day_infections = national7days_cases,
        hospital_cases = hospital_cases,
        deaths_total = deaths_total,
        news_articles=news,
        updates = displayed_updates
        )

if __name__ == '__main__':
    covid_data_processed = process_covid_API_data(covid_API_request())
    local7days_cases = covid_data_processed["local7days_cases"]
    national7days_cases = covid_data_processed["national7days_cases"]
    hospital_cases = covid_data_processed["hospital_cases"]
    deaths_total = covid_data_processed["deaths_total"]
    app.run()

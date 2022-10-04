
# Automated Covid-19 Data Dashboard
## Introduction
The automated Covid-19 data dashboard is developed for the Continous Assessment for the ECM1400 module.  It provides up to data local and national Covid-19 figures, up to date Covid-19 news, with the ability to create, modify and remove automated scheduled updates. 
## Prerequisites
**Python 3.7.4** was used for the development of the automated Covid-19 data dashboard. To run the program you will need a Python 3 interpreter. If you are a developer and would like to develop further on this project you will also need a text-editor or an Integrated Development Environment (IDE).

You will need an API key for the News API which you can get for free from https://newsapi.org/. Register, then copy your API key into the ```config.json``` file.

In the ```config.json``` file, under ```'news'```, the country can be changed to get Covid-19 news from your country. It is set to ```'gb'``` (Great Britain) as default.

In the ```config.json``` file, under ```'news'```, the new filter terms can be changed to filter news articles of your choice. It is set to ```'Covid COVID-19 coronavirus'``` as default.

In the ```config.json``` file under ```'covid_data'``` the location and location type can be changed to get Covid-19 figures from an area of your choice. They are set to ```'Exeter'``` and ```'ltla'``` as default.

### Replacing the Logo
The logo can be changed with a .png file which has square dimensions, by swapping the existing ```image.png``` with your own ```image.png``` under ```Automated Covid-19 Data Dashboard/static/images``` .
### Replacing the Favicon
The favicon can be changed with a .ico file which has a resolution of 16x16 px, by swapping the exiting ```favicon.ico``` with your own ```favicon.ico``` under ```Automated Covid-19 Data Dashboard/static``` .
## Installation
A few modules will need to be installed which can be done using the following commands in the command prompt/terminal:
1. Flask
    ```
    pip install Flask
    ```
2. uk_covid_19
    ```
    pip install uk-covid19
    ```
3. newsapi
    ```
    pip install newsapi-python
    ```
4. requests
    ```
    pip install requests
    ```
## Getting Started
To get started with the Automated Covid-19 Data Dashboard, run ```covid_data_handler.py```. Then connect to the URL http://127.0.0.1:5000/ in a browser. 

This will display the embedded HTML template with the news articles column on the right, the up to date covid data in the center, the fields to schedule an update below the center, and the scheduled updates on the left.
### Creating Updates
An update can be created using the form located at the bottom center of the page.
1. Fill in the ```time``` field with time you would like the update to happen

2. Fill in the ```Update label``` field for the name of the update

3. Tick the ```Repeat update``` field if you would like the update to repeat

4. Tick the ```Update Covid data``` field if you would like the Covid-19 data to refresh in the update

5. Tick the ```Update news articles``` field if you would like the news articles to refresh in the update

6. Click the ```Submit``` button to create the update
### Removing Updates and News Articles
Scheduled updates and news articles can be removed by clicking the 'x' on the desired update or article.
## Testing
Tests can be run in any of the test files provided, or in the terminal using the ```pytest``` command. If you do not have pytest installed you can type ```pip install pytest``` into the terminal to install it.
### Testing Covid Data Handler: ```test_covid_data_handler.py```
* ```test_parse_csv_data``` Tests whether the variable ```data```, which should be a list of strings for rows in the sample file, is equal to 639
* ```test_process_csv_data``` Tests whether the sample data has been processed correctly, checking three variables, if ```last7days_cases == 240_299```, ```current_hospital_cases == 7_019```, and ```total_deaths == 141_544```.
* ```test_covid_API_request``` Tests if the function returns a dictionary
* ```test_schedule_covid_updates``` Tests if the function schedules an update when called with the values ```update_interval=10``` and ```update_name='update test'``` passed into it.
### Testing News Data Handler: ```test_news_data_handling.py```
* ```test_news_API_request``` Tests whether the ```news_API_request``` can be called and whether calling it with the keywords ```'Covid COVID-19 coronavirus'``` is equal to calling it without the keywords.
* ```test_update_news``` Tests whether the function ```test_update_news``` can be called with ```update_news``` passed into it.
### Testing uk_covid19 API: ```test_uk_covid_19_api.py```
* ```test_covid_api_response``` Tests that the API returns the response code 200
* ```test_covid_api_type``` Tests that the API returns a dictionary
### Testing News API: ```test_news_api.py```
* ```test_news_api_status``` tests if when the API is called it returns status ```ok```
* ```test_news_api_type``` tests if the api returns a dictionary
* ```test_news_api_noapikey``` tests if when there is no API key it returns code 401 Unauthorized
* ```test_news_api_countryerror``` tests if when the country is invalid it returns code 400 Bad Request
## Authors
* **Thomas Farrar**
## License
This project is licensed under the MIT License - see ```LICENSE``` for more details.
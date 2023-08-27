# COVID-19 Dashboard

### Introduction
The COVID-19 Dashboard provides the latest local and national statistics on Covid-19 cases and provide relevant news articles relating to this topic. The user can also schedule when these updates happen.

### App Features
- Provides news articles and Covid-19 statistic updates.
- User can change local and national location to get updates from.
- User can plan and cancel scheduled updates at any time.
- User can choose to repeat scheduled updates and choose what to update (news articles and/or Covid-19 data).
- User can dismiss news articles and they won't show up again.

### Prerequisites
  - Python 3.7+
  - Stable internet connection
  - [https://newsapi.org/] API key
  - Some programming knowledge

### Installation
- Open the Command Prompt and type the following below:

To install flask, run:
$ pip install Flask

To install requests, run:
$ pip install requests

To install uk-covid19, run:
$ pip install uk-covid19

### Developer guide
- Move all provided files into a new directory.
- Create an API key from the news website (https://newsapi.org/) and replace the current API key in the config.json file.
- The location for Covid-19 data can also be changed in the same config.json file.
- The images(s) displayed on the dashboard can be changed in the config.json file and by placing the image files in the directory "\static\images".
- There are other options to customize the dashboard in the config.json file. To see what values are valid for some of the options, visit the developer's guide on their websites: 
	- News: https://newsapi.org/docs/endpoints/sources
	- Covid-19: https://coronavirus.data.gov.uk/details/developers-guide
- Source code is in "main.py" and in the "modules" folder, available to be edited.

### How to start program
- To start the program, run "main.py" (below is one method to run "main.py" in Windows).
	- Open the Command Prompt.
	- Change the current directory to the path of where "main.py" is located:
		Ex. cd C:\Users\Alex\Documents\COVID-19 Dashboard
	- Run:
		python3 main.py
- Follow the link that is given:
	Ex. http://127.0.0.1:5000/

### How to use
- User can click on the clock icon to set the time of a scheduled update. 
- The title of the scheduled update can be typed into the the textbox and is required to set an update.
- Tick boxes for repeat update, Covid data, and news articles are used to decided what is updated and can be toggled on/off.
- The X's for both the scheduled updates and news articles can be clicked to close/cancel them.
- The page can be manually refreshed to get the latest Covid data and news articles.

### Testing 
All the testing for the two modules (covid_data_handler and covid_news_handling) can be found in the "testing" folder.
Pytest can be used to run all these tests at once.
To learn how to install and use Pytest visit: https://docs.pytest.org/en/6.2.x/getting-started.html

### Links and Sources
- News API: https://newsapi.org/docs/endpoints/sources
- Covid-19 API: https://coronavirus.data.gov.uk/details/developers-guide
- Requests guide: https://realpython.com/python-requests/
- Flask guide: https://flask.palletsprojects.com/en/1.1.x/quickstart/

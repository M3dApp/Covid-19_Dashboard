from uk_covid19 import Cov19API
import pathlib
import json

config_path = str(pathlib.Path(__file__).parent.parent.resolve())+"\\config.json"
config = json.load(open(config_path, 'r'))

scheduler = None
del_sched = []
local_last7days_cases = 0
nation_last7days_cases = 0
nation_hosp_cases = 0
nation_deaths = 0

def parse_csv_data(csv_filename):
    """
    Opens and returns the lines from a csv file.
    
    Args:
        csv_filename (str): File path to csv file.
    
    Returns:
        lines (str[]): A list of the lines in the csv file.
    """
    lines = open(csv_filename, "r").readlines()
    return lines

def process_covid_csv_data(covid_csv_data):
    """
    Extracts and calculates the stats from the csv data.

    Args:
        covid_csv_data (str[]): A list of data to be processed.
    
    Returns:
        last7days_cases (int): Total cases in the last 7 days.
        current_hospital_cases (int): Total hospital cases.
        total_deaths (int): Total deaths.
    """
    last7days_cases = None
    current_hospital_cases = None
    total_deaths = None
    count = 0
    for line in covid_csv_data:
        if count > 0:
            data = line.split(',')
            if (data[6] != "None" and len(data[6].replace("\n", "")) > 0) and count <= 8:
                if count > 1:
                    last7days_cases = (last7days_cases != None and last7days_cases + int(data[6])) or int(data[6])
                count += 1
            if data[5] != "None" and current_hospital_cases == None and len(data[5]) > 0:
                current_hospital_cases = int(data[5])
            if data[4] != "None" and total_deaths == None and len(data[4]) > 0:
                total_deaths = int(data[4])
        else:
            count = 1
    return last7days_cases, current_hospital_cases, total_deaths

def covid_API_request(location = "Exeter", location_type = "ltla"):
    """
    Sends a request to the API to get the lastest covid data.

    Args:
        location (str): Location to obtain covid data from.
        location_type (str): Location type to obtain covid data from.
    
    Returns:
        json (json): The latest covid data from specified location.
    """
    get_data = {}
    filtering = {
        "areaName=" + location,
        "areaType=" + location_type,
    }
    for h in config["data_headers"].split(','):
        get_data[h] = h
    return Cov19API(filters = filtering, structure = get_data).get_json()

def format_to_csv_data(data):
    """
    Converts data into a format that's readable by the process_covid_csv_data function.

    Args:
        data (list): Covid data that isn't formatted yet.
    
    Returns:
        formatted_data (list): Formatted covid data.
    """
    formatted_data = [config["data_headers"]]
    for i in data:
        part = None
        for x in i:
            part = (part != None and part + "," + str(i[x])) or i[x]
        formatted_data.append(part)
    return formatted_data

def update_covid_data(upd_name = None):
    """
    Changes the variables for the interface.

    Args:
        upd_name (str): Title of update that triggered this function.
    
    Returns:
        None.
    """
    global del_sched, local_last7days_cases, nation_last7days_cases, nation_hosp_cases, nation_deaths
    if upd_name != None:
        del_sched.append(upd_name)
    local_last7days_cases, _, _ = process_covid_csv_data(format_to_csv_data(covid_API_request(config["local_location"], config["local_location_type"])["data"]))
    nation_last7days_cases, nation_hosp_cases, nation_deaths = process_covid_csv_data(format_to_csv_data(covid_API_request(config["national_location"], config["national_location_type"])["data"]))

def schedule_covid_updates(update_interval, update_name):
    """
    Enters a schedule into the scheduler to update covid data.

    Args:
        update_interval (int): Delay of when to trigger update.
        update_name (str): Title of update that will trigger the covid data update.
    
    Returns:
        None.
    """
    if scheduler:
        scheduler.enter(update_interval, 0, update_covid_data, (update_name,))

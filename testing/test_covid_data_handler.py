import pathlib
from sys import path
path.append("../modules")

from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import format_to_csv_data
from covid_data_handler import update_covid_data
from covid_data_handler import schedule_covid_updates

csv_file_path = str(pathlib.Path(__file__).parent.parent.resolve())+"\\docs\\nation_2021-10-28.csv"

def test_parse_csv_data():
    data = parse_csv_data(csv_file_path)
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data(csv_file_path))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data1 = covid_API_request()
    data2 = covid_API_request(location="Exeter", location_type="ltla")
    assert isinstance(data1, dict)
    assert data1 == data2

def test_format_to_csv_data():
    formatted_data = format_to_csv_data(covid_API_request()["data"])
    assert isinstance(formatted_data, list)

def test_update_covid_data():
    update_covid_data()
    update_covid_data("TEST")

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name="TEST @ 00:00")
